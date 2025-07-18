import streamlit as st
from vive_cording_test import generate_commented_code, highlight_code, PALETTES

def main():
    st.title("🎨 CodePalette: Python 코드에 주석 달고 색상 팔레트로 하이라이팅!")
    st.write("파이썬 코드를 입력하고, 주석 스타일과 테마를 선택하세요. GPT가 자동으로 주석을 달아주고, HTML로 하이라이팅해줍니다!")

    # 1. 코드 입력
    code = st.text_area("파이썬 코드를 입력하세요", value="""def greet(name):\n    print('Hello', name)\n\ngreet('CodePalette')""", height=180)

    # 2. 스타일/테마 선택
    style = st.selectbox("주석 스타일", ["basic", "emoji", "block", "educational"], index=0)
    theme = st.selectbox("코드 테마", list(PALETTES.keys()), index=0)

    if st.button("주석 생성 및 하이라이팅!"):
        with st.spinner("GPT가 주석을 생성 중입니다..."):
            commented = generate_commented_code(code, style=style)
        st.subheader("🔎 자동 생성된 주석 코드")
        st.code(commented, language="python")

        # HTML 하이라이팅
        palette = PALETTES[theme]
        html = highlight_code(commented, palette)
        st.subheader("🎨 HTML 하이라이팅 결과")
        st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
