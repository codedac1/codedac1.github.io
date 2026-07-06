# CodeDAC 회사 홈페이지

CodeDAC는 **Clipboard+**, **AutoStart+** 등 스마트폰 유틸리티 앱을 만들고 배포하는 개발사입니다.
이 저장소는 순수 HTML / CSS / JavaScript로 만든 **국문·영문 지원** 회사 홈페이지로, 빌드 과정 없이 그대로 **GitHub Pages**에 배포할 수 있습니다.

## 구성

```
.
├── index.html          # 페이지 본문 (회사 소개 / 앱 소개 / 문의)
├── css/style.css       # 스타일 (색상은 상단 :root 변수에서 일괄 변경)
├── js/main.js          # i18n 사전 · APPS 데이터 · 앱 카드 렌더링 · 라이트박스 · 문의 폼
├── privacy.html        # 개인정보처리방침 (국/영문)
├── robots.txt          # 크롤러 안내
├── sitemap.xml         # 사이트맵 (Search Console에 제출)
├── images/icons/       # 앱 아이콘
├── images/shots/       # 앱 스크린샷 (앱당 최대 3장)
├── images/og-image.png # 소셜 공유(OG) 이미지 1200x630
└── scripts/            # 자산 생성/검증 도구 (배포에는 불필요)
    ├── build_assets.py       # C:\CodeDAC 각 앱의 아이콘·스크린샷을 변환·복사
    ├── make_og.py            # OG 공유 이미지 생성
    ├── gen_static_cards.js   # 앱 정적 카드(HTML) 생성 (SEO용)
    └── verify_render.js      # Puppeteer로 렌더링/오류 검증
```

## SEO 참고

- `index.html`의 `#appGrid`에는 검색엔진용 **정적 앱 목록**이 들어 있고, JS 로딩 시 인터랙티브 버전으로 교체됩니다. 앱을 바꾸면 `node scripts/gen_static_cards.js` 출력으로 이 목록을 갱신하세요.
- `sitemap.xml`은 **Google Search Console**에서 직접 제출해야 색인이 빨라집니다: `https://codedac1.github.io/codedac/sitemap.xml`
- GitHub 프로젝트 페이지 특성상 `robots.txt`는 도메인 루트(`codedac1.github.io/robots.txt`)에서만 크롤러가 참조하므로, 이 저장소의 `robots.txt`는 참고용입니다(크롤은 기본 허용).

## 앱 소개 섹션

- 16개 앱이 `js/main.js`의 `APPS` 배열에 정의돼 있으며, 카드가 자동 생성됩니다.
- 각 앱은 아이콘 + 이름 + 카테고리 + 한 줄 설명(국문·영문)으로 구성되고, 스크린샷 썸네일을 누르면 라이트박스로 크게 볼 수 있습니다.
- **Google Play 링크**: `APPS` 배열 각 앱의 `store: ''` 에 실제 주소를 넣으면 카드에 스토어 버튼이 표시됩니다.
- 앱 이미지를 다시 만들려면 `python scripts/build_assets.py` 실행.

## 국문 / 영문 지원

- 우측 상단 **KR / EN** 버튼으로 언어를 전환하며, 선택은 브라우저에 기억됩니다.
- 모든 문구는 `js/main.js`의 `I18N` 사전에 `ko` / `en` 두 벌로 들어 있습니다. 문구를 바꿀 때는 **두 언어를 함께** 수정하세요.

## 로컬에서 미리보기

브라우저로 `index.html`을 열면 바로 확인할 수 있습니다.
문의 폼까지 정확히 테스트하려면 간단한 로컬 서버 사용을 권장합니다.

```bash
# Python이 설치되어 있다면
python -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

## 내용 수정 방법

- **문구(국문·영문)**: `js/main.js`의 `I18N` 사전에서 `ko` / `en` 값 편집
- **앱 스토어 링크**: `index.html`에서 `▼ 스토어 링크로 수정하세요 ▼` 주석의 `href="#"` 를 실제 주소로 변경
- **색상 / 디자인**: `css/style.css` 최상단 `:root` 변수 값 변경
- **문의 받을 이메일**: `js/main.js`의 `CONTACT_EMAIL` 값 변경

## GitHub Pages 배포

1. 이 저장소를 GitHub에 push 합니다.
2. GitHub 저장소 → **Settings → Pages** 이동
3. **Source**를 `Deploy from a branch`로 두고, Branch를 `main` / 폴더를 `/ (root)`로 지정 후 **Save**
4. 잠시 후 `https://<사용자명>.github.io/codedac/` 주소로 공개됩니다.

> 커스텀 도메인(예: `codedac.com`)을 쓰려면 Settings → Pages의 **Custom domain**에 도메인을 입력하고, 도메인 업체에서 DNS를 GitHub Pages로 설정하면 됩니다.
