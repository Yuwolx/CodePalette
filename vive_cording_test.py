import openai
import os
import re
import streamlit as st
# API 키 설정
openai.api_key = st.secrets["openai"]["api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 팔레트 정의
PALETTES = {
    "sorairo": {
        "background": "#E0F2FF",
        "keyword": "#1D4ED8",
        "string": "#15803D",
        "comment": "#6B7280",
        "function": "#0F766E",
        "variable": "#E879F9",
        "number": "#FACC15",
        "operator": "#F472B6",
        "builtin": "#0EA5E9",
        "default": "#0F172A"
    },
    "midnight": {
        "background": "#121826",
        "keyword": "#93C5FD",
        "string": "#FACC15",
        "comment": "#64748B",
        "function": "#67E8F9",
        "variable": "#F472B6",
        "number": "#FDE68A",
        "operator": "#F472B6",
        "builtin": "#38BDF8",
        "default": "#F8FAFC"
    },
    "light": {
        "background": "#FFFFFF",
        "keyword": "#2563EB",
        "string": "#059669",
        "comment": "#9CA3AF",
        "function": "#0EA5E9",
        "variable": "#D946EF",
        "number": "#FBBF24",
        "operator": "#F472B6",
        "builtin": "#0EA5E9",
        "default": "#1E293B"
    },
    "dark": {
        "background": "#23272F",
        "keyword": "#60A5FA",
        "string": "#FBBF24",
        "comment": "#94A3B8",
        "function": "#38BDF8",
        "variable": "#F472B6",
        "number": "#FDE68A",
        "operator": "#F472B6",
        "builtin": "#38BDF8",
        "default": "#F1F5F9"
    }
}

# 코드 하이라이팅
def highlight_code(code: str, palette: dict) -> str:
    # 패턴 정의
    keywords = r'\b(def|return|if|else|elif|for|while|import|from|as|with|class|try|except|finally|in|is|and|or|not|break|continue|pass|lambda|yield|global|nonlocal|assert|raise|del)\b'
    builtins = r'\b(print|input|len|range|str|int|float|list|dict|set|tuple|open|enumerate|zip|map|filter|sum|min|max|abs|type|isinstance|dir|help|id|sorted|reversed|any|all|chr|ord|hex|bin|oct|bool|super)\b'
    def_func = r'def (\w+)'
    str_pat = r'(\'[^\']*\'|\"[^\"]*\")'
    comment_pat = r'(#.*$)'
    number_pat = r'\b(\d+(?:\.\d+)?)\b'
    operator_pat = r'([+\-*/%=<>!&|^~]+)'
    variable_pat = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'

    # 함수명 강조
    def repl_func(m):
        return f'<span style="color:{palette["keyword"]}">def</span> <span style="color:{palette["function"]}">{m.group(1)}</span>'

    html = code
    html = re.sub(def_func, repl_func, html)
    html = re.sub(builtins, lambda m: f'<span style="color:{palette["builtin"]}">{m.group(0)}</span>', html)
    html = re.sub(keywords, lambda m: f'<span style="color:{palette["keyword"]}">{m.group(0)}</span>', html)
    html = re.sub(str_pat, lambda m: f'<span style="color:{palette["string"]}">{m.group(0)}</span>', html)
    html = re.sub(comment_pat, lambda m: f'<span style="color:{palette["comment"]}">{m.group(0)}</span>', html, flags=re.MULTILINE)
    html = re.sub(number_pat, lambda m: f'<span style="color:{palette["number"]}">{m.group(0)}</span>', html)
    html = re.sub(operator_pat, lambda m: f'<span style="color:{palette["operator"]}">{m.group(0)}</span>', html)
    # 변수: 이미 함수명/키워드/내장함수/문자열/숫자/연산자/주석 제외 후 남은 식별자
    def repl_var(m):
        word = m.group(1)
        # 이미 다른 태그로 감싸진 경우 제외
        if re.search(r'<span', word):
            return word
        return f'<span style="color:{palette["variable"]}">{word}</span>'
    # 변수는 마지막에 적용 (이미 태그 처리된 부분은 제외)
    html = re.sub(variable_pat, repl_var, html)
    # 줄바꿈 및 배경
    html = html.replace("\n", "<br>")

    # 범례(legend) 추가
    legend = f'''
    <div style="margin-top:16px;padding:8px 12px;border-radius:6px;background:#fffbe7;border:1px solid #facc15;font-size:15px;">
        <b>색상 범례:</b><br>
        <span style="color:{palette['keyword']};font-weight:bold;">🟦 키워드</span> (조건문, 반복문, def 등),
        <span style="color:{palette['function']};font-weight:bold;">🟪 함수명</span>,
        <span style="color:{palette['variable']};font-weight:bold;">🟣 변수</span>,
        <span style="color:{palette['string']};font-weight:bold;">🟩 문자열</span>,
        <span style="color:{palette['number']};font-weight:bold;">🟨 숫자</span>,
        <span style="color:{palette['operator']};font-weight:bold;">🟥 연산자</span>,
        <span style="color:{palette['builtin']};font-weight:bold;">🟦 내장함수</span>,
        <span style="color:{palette['comment']};font-weight:bold;">💬 주석</span>
    </div>
    '''
    return f'<div style="background:{palette["background"]};padding:12px;border-radius:8px;font-family:monospace;font-size:16px;color:{palette["default"]}">{html}{legend}</div>'

# GPT 주석 생성 함수
def generate_commented_code(code: str, style: str = "basic") -> str:
    style_prompt = {
        "basic": "한 줄씩 주석을 달아줘.",
        "emoji": "각 줄에 주석을 달되, 이모지를 포함해줘.",
        "block": "전체를 블록 주석으로 요약해줘.",
        "educational": "각 줄의 코드가 어떤 기능을 수행하는지 초보자도 이해할 수 있도록 최대한 친절하고 구체적으로 한글로 주석을 달아줘. 용어도 쉽게 풀어서 설명해줘."
    }
    prompt = f"""다음 파이썬 코드에 대해 {style_prompt.get(style, style_prompt['basic'])}\n\n```python\n{code}\n```"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=900,
    )
    return response.choices[0].message.content

# 실행부
if __name__ == "__main__":
    print("💡 CodePalette: 코드 주석 + 색상 하이라이팅\n" + "-" * 40)
    code = """
def greet(name):
    # 이름을 받아 인사합니다
    print("Hello", name)

greet("CodePalette")
"""
    comment_style = input("주석 스타일 선택 (basic / emoji / block): ").strip() or "basic"
    theme = input("테마 선택 (dark / light / sorairo / midnight): ").strip() or "sorairo"

    print("\n🚧 GPT 주석 생성 중...")
    commented = generate_commented_code(code, style=comment_style)
    print("\n✅ [자동 생성된 주석 코드]\n")
    print(commented)

    print("\n🎨 [HTML 하이라이팅 결과]\n")
    palette = PALETTES.get(theme, PALETTES["sorairo"])
    html = highlight_code(commented, palette)
    print(html)
