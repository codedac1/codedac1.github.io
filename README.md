# CodeDAC 회사 홈페이지

CodeDAC는 **Clipboard+**, **AutoStart+** 등 스마트폰 유틸리티 앱을 만들고 배포하는 개발사입니다.
이 저장소는 순수 HTML / CSS / JavaScript로 만든 **10개 언어 지원** 회사 홈페이지로, **GitHub Pages**(사용자 사이트 `codedac1.github.io`) 루트에 그대로 배포됩니다.

> 지원 언어: 한국어(ko, 루트) · English(en) · 日本語(ja) · Español(es) · Português(pt-BR) · Deutsch(de) · Français(fr) · Bahasa Indonesia(id) · हिन्दी(hi) · Tiếng Việt(vi)

## 구성

```
.
├── index.html            # 홈 (한국어, 루트) — 생성물
├── apps/<slug>.html      # 앱 상세 (한국어) — 생성물
├── <lang>/index.html     # 홈 (en, ja, es, pt, de, fr, id, hi, vi) — 생성물
├── <lang>/apps/<slug>.html  # 앱 상세 (언어별) — 생성물
├── privacy.html          # 개인정보처리방침 (국/영문, 별도 관리)
├── sitemap.xml           # 사이트맵 (hreflang 대체 링크 포함) — 생성물
├── robots.txt            # 크롤러 안내
├── css/style.css         # 스타일 (색상은 상단 :root 변수에서 일괄 변경)
├── js/site.js            # 공용 스크립트 (언어 드롭다운 · 모바일 메뉴 · 라이트박스)
├── images/icons/         # 앱 아이콘
├── images/shots/         # 앱 스크린샷 (앱당 최대 3장)
├── images/og-image.png   # 소셜 공유(OG) 이미지 1200x630
├── i18n/                 # ★ 콘텐츠 원본 (언어별 1파일) — 여기를 편집
│   ├── ko.json  en.json  ja.json  es.json  pt.json
│   └── de.json  fr.json  id.json  hi.json  vi.json
└── scripts/
    ├── apps_base.json    # 앱 기본정보(slug·스크린샷 수·스토어 링크) — 비언어 데이터
    ├── gen_site.js       # ★ 사이트 생성기 (140개 페이지 + sitemap 전부 생성)
    ├── build_assets.py   # C:\CodeDAC 각 앱의 아이콘·스크린샷 변환·복사
    └── make_og.py        # OG 공유 이미지 생성
```

`index.html`, `apps/`, `<lang>/`, `sitemap.xml` 은 **모두 생성물**입니다. 직접 편집하지 말고 `i18n/*.json` · `scripts/apps_base.json` 을 고친 뒤 생성기를 다시 돌리세요.

## 데이터 모델 (단일 소스)

- **앱 기본정보** — `scripts/apps_base.json`: `slug`, `name`, `shots`(스크린샷 수), `store`(Google Play 주소, 없으면 `""`). 언어와 무관.
- **언어별 문구** — `i18n/<lang>.json`: `ui`(사이트 UI 문구)와 `apps`(앱별 `tag`·`desc`·`tagline`·`long`·`features[6]`·`faq[3]`). 각 언어 파일은 **키 구조가 동일**해야 합니다(기준: `en.json`).

## 사이트 빌드

콘텐츠(`i18n/*.json`)나 앱 기본정보(`apps_base.json`)를 바꾼 뒤:

```bash
node scripts/gen_site.js     # 10개 언어 × (홈 + 앱상세 13) = 140개 페이지 + sitemap.xml 생성
```

- 자산(아이콘/스크린샷)을 바꾸면 `scripts/gen_site.js`의 `const V`(캐시 버전)를 올리세요.
- 로컬 미리보기(루트 절대경로 때문에 **HTTP 서버 필요**):
  ```bash
  python -m http.server 8000   # http://localhost:8000  (언어별: /ja/, /es/apps/floatcalc.html …)
  ```

## 다국어 SEO

- **언어별 URL** — 한국어는 루트(`/`, `/apps/…`), 그 외는 `/<lang>/…`. 각 페이지는 해당 언어 본문이 **정적으로** 렌더링돼 크롤러가 바로 읽습니다.
- **hreflang** — 모든 페이지가 서로의 언어 버전을 `<link rel="alternate" hreflang="…">`(+ `x-default`)로 가리켜, 구글이 시장별로 올바른 언어를 노출합니다.
- **구조화 데이터(JSON-LD)** — 홈은 `Organization`, 앱 상세는 `SoftwareApplication` · `BreadcrumbList` · `FAQPage`.
- **사이트맵 제출** — Google Search Console / 네이버 서치어드바이저에 `https://codedac1.github.io/sitemap.xml` 제출. 사이트맵에 언어 대체 링크가 포함돼 있습니다.
- 언어 전환은 우측 상단 **드롭다운**(같은 페이지의 다른 언어 URL로 이동).

## 새 언어 추가하기

1. `i18n/en.json`을 복사해 `i18n/<code>.json`을 만들고 값만 번역(키 구조 유지, `features` 6개·`faq` 3개, 브랜드/앱 이름·기술 용어는 원문 유지).
2. `scripts/gen_site.js`의 `LANGS` 배열에 `{ code, hreflang, htmlLang, native }` 한 줄 추가.
3. `node scripts/gen_site.js` 실행.

## 앱 추가·수정

1. 아이콘/스크린샷을 `images/`에 추가(필요 시 `python scripts/build_assets.py`).
2. `scripts/apps_base.json`에 앱 항목 추가(`slug`·`name`·`shots`·`store`).
3. **모든** `i18n/<lang>.json`의 `apps`에 해당 slug 콘텐츠 추가(언어별).
4. `node scripts/gen_site.js` 실행.

## 색상 / 디자인

`css/style.css` 최상단 `:root` 변수 값만 바꾸면 전체 색상이 일괄 변경됩니다.

## GitHub Pages 배포

이 저장소는 사용자 사이트(`codedac1.github.io`)라 `main` 브랜치 루트가 곧 `https://codedac1.github.io/` 로 공개됩니다. push 하면 1~2분 뒤 반영됩니다.

> 커스텀 도메인을 쓰려면 Settings → Pages의 **Custom domain**에 도메인을 입력하고 DNS를 GitHub Pages로 설정하세요.
