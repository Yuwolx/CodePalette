# CodePalette (CLI Prototype)

## 🗂️ 디렉토리 구조 예시

```
CodePalette/
│
├─ main.py               # 실행 진입점 (CLI or 추후 웹 연결 가능)
├─ comment_gen.py        # GPT를 이용한 자동 주석 생성 모듈
├─ converter.py          # 코드 → 이미지 생성 모듈 (Carbon API 등)
├─ config.py             # 설정값, API 키 로딩 등
├─ .env                  # OpenAI API 키 등 비밀 키
├─ requirements.txt      # 필요한 패키지 목록
└─ examples/
    └─ sample.py         # 예시 코드 테스트용
```

## 🧠 주요 기능 흐름

1. **코드 입력**: 예시 코드 또는 파일에서 코드 읽기
2. **GPT 주석 생성**: OpenAI API로 한 줄씩 주석 자동 생성
3. **코드 이미지화**: (Carbon API 등 활용) 주석 포함 코드 이미지를 생성
4. **확장성**: CLI → 웹(Flask/Streamlit) 확장 고려, 모듈화 구조

## 📝 예시 실행 흐름 (vive_cording_test.py 기준)

1. `generate_commented_code(code)`로 주석 생성
2. `code_to_image(commented, output_path)`로 이미지 저장
3. 결과물: `output.png` 생성 및 터미널 출력

## 💡 확장 아이디어
- Carbon API, html2image 등으로 실제 코드 이미지화 구현
- Web UI 연동 (Flask/Streamlit)
- 주석 스타일/언어 커스터마이징
- 다양한 언어 지원

## ⚙️ 환경 변수 및 패키지
- `.env` 파일에 `OPENAI_API_KEY` 저장
- `requirements.txt`: openai, python-dotenv, requests 등

---

**빠른 프로토타입 → 점진적 확장** 구조로 설계되어 있습니다.
