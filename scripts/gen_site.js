// =====================================================================
//  CodeDAC 다국어 사이트 생성기 (single source of truth)
//  - 데이터: scripts/apps_base.json (앱 기본정보) + i18n/<code>.json (언어별 문구)
//  - 출력:
//      /                         홈 (ko, 루트)
//      /apps/<slug>.html         앱 상세 (ko)
//      /<code>/                  홈 (ko 외 나머지 언어. LANGS 참고)
//      /<code>/apps/<slug>.html  앱 상세
//      sitemap.xml               (hreflang 대체 링크 포함)
//  - 모든 페이지에 hreflang 대체 링크가 들어가 시장별 SEO를 지원한다.
//  사용: node scripts/gen_site.js
// =====================================================================
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const BASE = 'https://codedac.com';
const V = '32'; // 자산 캐시 버전 (css/js). 자산 변경 시 올릴 것.
const LASTMOD = new Date().toISOString().slice(0, 10);

// GA4 측정 ID. 빈 문자열로 두면 모든 페이지에서 분석 스크립트가 빠진다.
const GA_ID = 'G-RVR49V8M2Z';

// 언어 정의 (표시 순서 = 스위처 순서). code=폴더/파일, hreflang=검색엔진용
// ogLocale: og:locale 값. 생략하면 hreflang의 '-'를 '_'로 바꿔 쓴다.
// dir: 쓰기 방향. 생략하면 'ltr'. css/style.css 가 논리 속성으로 반전을 처리한다.
const LANGS = [
  { code: 'ko', hreflang: 'ko', htmlLang: 'ko', native: '한국어' },
  { code: 'en', hreflang: 'en', htmlLang: 'en', native: 'English' },
  { code: 'ja', hreflang: 'ja', htmlLang: 'ja', native: '日本語' },
  { code: 'es', hreflang: 'es', htmlLang: 'es', native: 'Español' },
  { code: 'pt', hreflang: 'pt-BR', htmlLang: 'pt-BR', native: 'Português' },
  { code: 'de', hreflang: 'de', htmlLang: 'de', native: 'Deutsch' },
  { code: 'fr', hreflang: 'fr', htmlLang: 'fr', native: 'Français' },
  { code: 'id', hreflang: 'id', htmlLang: 'id', native: 'Bahasa Indonesia' },
  { code: 'hi', hreflang: 'hi', htmlLang: 'hi', native: 'हिन्दी' },
  { code: 'vi', hreflang: 'vi', htmlLang: 'vi', native: 'Tiếng Việt' },
  // 앱은 간체(values-zh)만 제공하므로 hreflang에도 Hans 스크립트를 명시한다.
  { code: 'zh', hreflang: 'zh-Hans', htmlLang: 'zh-Hans', ogLocale: 'zh_CN', native: '简体中文' },
  { code: 'ru', hreflang: 'ru', htmlLang: 'ru', native: 'Русский' },
  { code: 'tr', hreflang: 'tr', htmlLang: 'tr', native: 'Türkçe' },
  { code: 'it', hreflang: 'it', htmlLang: 'it', native: 'Italiano' },
  { code: 'pl', hreflang: 'pl', htmlLang: 'pl', native: 'Polski' },
  { code: 'th', hreflang: 'th', htmlLang: 'th', native: 'ไทย' },
  // hreflang은 ISO 639-1만 받으므로 'fil'이 아니라 타갈로그의 'tl'을 쓴다.
  { code: 'fil', hreflang: 'tl', htmlLang: 'fil', native: 'Filipino' },
  { code: 'ar', hreflang: 'ar', htmlLang: 'ar', dir: 'rtl', native: 'العربية' },
];
const XDEFAULT = 'en';

// 브라우저가 보내는 기본 언어 코드 → 사이트 폴더 코드.
// 안드로이드/iOS는 필리핀어를 'tl-PH'로도 'fil-PH'로도 보고한다.
const LANG_ALIAS = { tl: 'fil' };

// schema.org applicationCategory (slug 기준)
const APP_SCHEMA_CAT = {
  colorcards: 'EducationalApplication',
  wordcards: 'EducationalApplication',
  sleepbaby: 'LifestyleApplication',
};
const schemaCat = (slug) => APP_SCHEMA_CAT[slug] || 'UtilitiesApplication';

// --- 데이터 로드 ---
const APPS = require('./apps_base.json');

// Google Play 지표 (fetch_store_stats.js 산출물). 없으면 지표/평점 렌더를 생략한다.
let STATS = { aggregate: {}, apps: {} };
try {
  STATS = require('./store_stats.json');
} catch {
  console.warn('(경고) scripts/store_stats.json 없음 — 지표·평점 배지 생략. `npm run fetch-stats` 로 생성하세요.');
}
// 누적 다운로드 표기 (최소 설치수 합계를 1,000 단위로 내림 → "12,000+")
const DL_TOTAL = STATS.aggregate && STATS.aggregate.totalMinInstalls || 0;
const DL_DISPLAY = DL_TOTAL >= 1000 ? (Math.floor(DL_TOTAL / 1000) * 1000).toLocaleString('en-US') + '+' : (DL_TOTAL ? DL_TOTAL + '+' : null);

// 앱별 지원 언어 수 (scan_app_langs.js 산출물). 없으면 언어 배지 생략.
let APP_LANGS = {};
try {
  APP_LANGS = require('./app_langs.json');
} catch {
  console.warn('(경고) scripts/app_langs.json 없음 — 앱 언어 배지 생략. `node scripts/scan_app_langs.js` 로 생성하세요.');
}
const langCountOf = (slug) => (APP_LANGS[slug] && APP_LANGS[slug].count) || 0;

// 사용자 후기 (reviews.json — 손수 큐레이션한 5★ Google Play 리뷰). 없으면 섹션 생략.
let REVIEWS_BY_APP = {};
try {
  REVIEWS_BY_APP = require('./reviews.json').byApp || {};
} catch {
  console.warn('(경고) scripts/reviews.json 없음 — 후기 섹션 생략.');
}
const reviewsFor = (slug) => (REVIEWS_BY_APP[slug] || []).map((r) => ({ ...r, slug }));
const HAS_REVIEWS = Object.values(REVIEWS_BY_APP).some((a) => a && a.length);
// 홈 후기: 앱별로 번갈아 뽑되 같은 리뷰어는 한 번만, 최대 6개
function featuredReviews() {
  const lists = APPS.map((app) => reviewsFor(app.slug)).filter((l) => l.length);
  const out = [];
  const seen = new Set();
  for (let i = 0; out.length < 6 && lists.some((l) => l[i]); i++) {
    for (const l of lists) {
      const r = l[i];
      if (!r || seen.has(r.name) || out.length >= 6) continue;
      seen.add(r.name); out.push(r);
    }
  }
  return out;
}

// 앱들이 통틀어 지원하는 언어 수(합집합) → "50+" (10 단위로 내림). 지표 스트립용.
const APP_LANG_UNION = new Set();
for (const v of Object.values(APP_LANGS)) (v.codes || []).forEach((c) => APP_LANG_UNION.add(c));
const APP_LANG_DISPLAY = APP_LANG_UNION.size ? (Math.floor(APP_LANG_UNION.size / 10) * 10) + '+' : null;
const L = {};
for (const lang of LANGS) {
  const p = path.join(ROOT, 'i18n', `${lang.code}.json`);
  if (!fs.existsSync(p)) { console.warn(`(경고) i18n/${lang.code}.json 없음 — 이 언어는 건너뜀`); continue; }
  L[lang.code] = require(p);
}
const ACTIVE = LANGS.filter((l) => L[l.code]);

// 개인정보처리방침 (언어별 별도 파일)
const PRIV = {};
for (const lang of LANGS) {
  const p = path.join(ROOT, 'i18n', 'privacy', `${lang.code}.json`);
  if (fs.existsSync(p)) PRIV[lang.code] = require(p);
}
const PRIV_ACTIVE = ACTIVE.filter((l) => PRIV[l.code]);

// --- 유틸 ---
const escText = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');

// 앱 이름은 'VolumeBooster+' 처럼 '+' 로 끝난다. RTL 문서에서 이 '+' 는 앞뒤 어느 쪽도
// 강한 방향성을 주지 않아 중립 문자로 해석되고, 문단 방향(RTL)을 따라 이름 왼쪽으로
// 밀려나 '+VolumeBooster' 로 보인다. <bdi> 로 감싸 방향을 격리한다.
// bdi 는 LTR 문서에서는 아무 효과가 없으므로 언어별 분기가 필요 없다.
const bdiName = (s) => `<bdi>${escText(s)}</bdi>`;

// 내부 링크(루트 절대경로) — 사용자 사이트(codedac1.github.io)라 / 로 시작 가능
function pathFor(code, kind, slug) {
  const dir = code === 'ko' ? '/' : `/${code}/`;
  if (kind === 'home') return dir;
  if (kind === 'privacy') return `${dir}privacy.html`;
  return `${dir}apps/${slug}.html`;
}
// 절대 URL (canonical/hreflang/OG)
function urlFor(code, kind, slug) {
  return BASE + pathFor(code, kind, slug);
}
// 출력 파일 경로
function fileFor(code, kind, slug) {
  const dir = code === 'ko' ? '' : `${code}/`;
  if (kind === 'home') return `${dir}index.html`;
  if (kind === 'privacy') return `${dir}privacy.html`;
  return `${dir}apps/${slug}.html`;
}

// hreflang 대체 링크 블록 (langSet: 이 페이지가 존재하는 언어들)
function hreflangLinks(kind, slug, langSet) {
  const set = langSet || ACTIVE;
  const links = set.map((l) =>
    `  <link rel="alternate" hreflang="${l.hreflang}" href="${urlFor(l.code, kind, slug)}" />`
  );
  const xd = set.find((l) => l.code === XDEFAULT) || set[0];
  links.push(`  <link rel="alternate" hreflang="x-default" href="${urlFor(xd.code, kind, slug)}" />`);
  return links.join('\n');
}

// 언어 스위처 (드롭다운)
function langSwitcher(curCode, kind, slug) {
  const cur = LANGS.find((l) => l.code === curCode);
  const items = ACTIVE.map((l) => {
    const active = l.code === curCode ? ' is-active' : '';
    // data-lang 은 폴더 코드. hreflang 에서 코드를 되짚으면 안 된다 —
    // 필리핀어의 hreflang 은 'tl' 이고 zh 는 'zh-Hans' 라, 폴더명과 어긋난다.
    return `        <a class="lang-item${active}" data-lang="${l.code}" href="${pathFor(l.code, kind, slug)}" hreflang="${l.hreflang}" lang="${l.htmlLang}">${l.native}</a>`;
  }).join('\n');
  return `<div class="lang-switch">
        <button type="button" class="lang-btn" id="langBtn" aria-haspopup="true" aria-expanded="false">${cur.native} <span class="caret">▾</span></button>
        <div class="lang-menu" id="langMenu" role="menu">
${items}
        </div>
      </div>`;
}

const FAVICON = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect rx='22' width='100' height='100' fill='%232F3B59'/%3E%3Ctext x='50' y='72' font-size='64' font-family='Arial,sans-serif' font-weight='bold' fill='white' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E`;

// 저장된 언어 선택에 따른 리다이렉트 (ko=루트 페이지에만 삽입).
//
// 브라우저 언어만 보고 첫 방문자를 옮기지 않는다. 구글은 추정 언어에 기반한 자동
// 리다이렉트를 피하라고 권고하는데, Googlebot 은 JS 를 실행하고 렌더링 환경의 언어가
// 영어라서, 그렇게 하면 루트의 한국어 본문이 크롤러에게 한 번도 보이지 않는다.
// 대신 처음 온 방문자에게는 배너로 다른 언어를 제안한다(langBanner, js/site.js).
//
// 여기서 옮기는 대상은 '이전에 스스로 언어를 고른' 방문자뿐이다. 이 규칙은 사람과
// 크롤러에 똑같이 적용된다 — User-Agent 를 보지 않으므로 클로킹이 아니다.
// 크롤러는 localStorage 가 늘 비어 있어 자연히 한국어 본문을 받는다.
//
// 저장값은 반드시 지원 목록과 대조한다. 언어를 빼거나 코드를 바꾸면 그 언어를
// 골라둔 사용자의 저장값이 없는 경로를 가리키게 되고, 그대로 이동하면 매 방문마다
// 404 로 보내진다. 별칭도 함께 태워, 예전 코드로 저장된 값을 현재 폴더로 옮긴다.
//
// rest: 목적지 언어에서의 동일 페이지 경로 접미사(home='' · privacy='privacy.html' · detail='apps/<slug>.html')
function storedLangRedirect(code, kind, slug) {
  if (code !== 'ko') return '';
  const rest = kind === 'home' ? '' : kind === 'privacy' ? 'privacy.html' : `apps/${slug}.html`;
  const codes = ACTIVE.filter((l) => l.code !== 'ko').map((l) => l.code);
  const map = Object.fromEntries(codes.map((c) => [c, c]));
  for (const [from, to] of Object.entries(LANG_ALIAS)) if (codes.includes(to)) map[from] = to;
  const supObj = JSON.stringify(map);
  // g(): 지원 목록 조회. typeof 검사로 'constructor' 같은 프로토타입 키가 걸리지 않게 한다.
  return `
  <script>(function(){try{var s=localStorage.getItem('lang'),sup=${supObj},g=function(k){return typeof sup[k]==='string'?sup[k]:0;},p=g(s);if(p)location.replace('/'+p+'/'+${JSON.stringify(rest)});}catch(e){}})();</script>`;
}

// 언어 제안 배너용 데이터. 이 페이지가 존재하는 언어들의 (문구, 경로)를 인라인으로 넘긴다.
// 배너는 방문자가 읽을 수 있는 언어, 즉 '이동할 대상 언어'로 표시되므로
// 현재 페이지 언어가 아니라 모든 언어의 문구가 필요하다.
//
// 현재 언어(cur)도 반드시 목록에 넣는다. 빼면 브라우저 1순위 언어가 이 페이지의 언어일 때
// 조회에 실패해 2순위(대개 영어)로 밀려나, 일본어 사용자가 일본어 페이지에서
// 영어 배너를 보게 된다. 목록에 넣어두고 cur 와 같으면 배너를 띄우지 않는다.
function bannerData(code, kind, slug, langSet) {
  const set = langSet || ACTIVE;
  if (set.length < 2) return '';
  const langs = {};
  for (const l of set) {
    const ui = L[l.code].ui;
    langs[l.code] = { t: ui['banner.text'], c: ui['banner.cta'], d: ui['banner.dismiss'], u: pathFor(l.code, kind, slug), r: l.dir || 'ltr' };
  }
  const payload = JSON.stringify({ cur: code, alias: LANG_ALIAS, langs });
  // </script> 가 문자열 안에서 조기 종료를 일으키지 않도록 '<' 를 이스케이프한다.
  return `  <script>window.__LANG_BANNER=${payload.replace(/</g, '\\u003c')};</script>\n`;
}

// GDPR/UK GDPR/nFADP 적용 지역. 이 지역에서만 분석 쿠키를 기본 거부한다.
// EU 27개국 + EEA(IS·LI·NO) + 영국(GB) + 스위스(CH).
const CONSENT_DENY_REGIONS = [
  'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE',
  'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE',
  'IS', 'LI', 'NO', 'GB', 'CH',
];

// Google Analytics 4 + Consent Mode v2.
//
// 동의 배너 없이 운영하므로 gtag('consent','default')로만 권한을 선언한다.
//  - CONSENT_DENY_REGIONS: analytics_storage 거부 → 쿠키 없는 익명 핑만 전송.
//  - 그 외 지역: analytics_storage 허용 → 정상적인 사용자·세션 집계.
// region이 붙은 선언이 더 구체적이므로 전역 선언보다 우선한다(둘 다 'default').
//
// 광고 신호(ad_*)는 웹사이트에 광고가 없으므로 전 지역에서 거부한다.
//
// 주의: 전 지역을 denied로 두면 GA4는 쿠키리스 핑을 '행동 모델링' 재료로만 쓰는데,
// 모델링은 analytics_storage='granted' 사용자가 하루 1,000명 이상이어야 학습된다.
// 따라서 전역 denied 상태에서는 보고서가 영구히 비어 있게 된다.
//
// gtag('consent','default')는 반드시 gtag.js 로더보다 먼저 실행되어야 한다.
// storedLangRedirect() 뒤에 두어, 리디렉션되는 루트 페이지에서 중복 조회가 잡히지 않게 한다.
function gaSnippet() {
  if (!GA_ID) return '';
  const denied = "ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'";
  const regions = JSON.stringify(CONSENT_DENY_REGIONS).replace(/"/g, "'");
  return `
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('consent','default',{${denied},analytics_storage:'denied',functionality_storage:'denied',personalization_storage:'denied',security_storage:'granted',region:${regions}});gtag('consent','default',{${denied},analytics_storage:'granted',functionality_storage:'granted',personalization_storage:'granted',security_storage:'granted'});gtag('js',new Date());gtag('config',${JSON.stringify(GA_ID)});</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_ID)}"></script>`;
}

function headCommon(lang, { title, desc, canonical, ogImage, kind, slug, keywords, langSet }) {
  return `  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />${storedLangRedirect(lang.code, kind, slug)}${gaSnippet()}
  <script>(function(){try{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>
  <meta name="google-site-verification" content="EEOUsUwfv3SoTVMdi2dL1EePYJ9cLNKexZgbojtycc0" />
  <meta name="naver-site-verification" content="109d8df332a90f3aa9a8623c76a0876131746416" />
  <title>${escText(title)}</title>
  <meta name="description" content="${escAttr(desc)}" />
  <meta name="keywords" content="${escAttr(keywords)}" />
  <meta name="author" content="CodeDAC" />
  <meta name="robots" content="index, follow" />
  <meta name="theme-color" content="#2F3B59" />
  <link rel="canonical" href="${canonical}" />
${hreflangLinks(kind, slug, langSet)}

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CodeDAC" />
  <meta property="og:locale" content="${lang.ogLocale || lang.hreflang.replace('-', '_')}" />
  <meta property="og:title" content="${escAttr(title)}" />
  <meta property="og:description" content="${escAttr(desc)}" />
  <meta property="og:url" content="${canonical}" />
  <meta property="og:image" content="${ogImage}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${escAttr(title)}" />
  <meta name="twitter:description" content="${escAttr(desc)}" />
  <meta name="twitter:image" content="${ogImage}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet" />
  <link rel="icon" href="${FAVICON}" />
  <link rel="stylesheet" href="/css/style.css?v=${V}" />`;
}

function header(code, kind, slug, ui) {
  return `  <header class="site-header" id="top">
    <div class="container nav-wrap">
      <a href="${pathFor(code, 'home')}" class="logo">Code<span>DAC</span></a>
      <nav class="nav" id="nav">
        <a href="${pathFor(code, 'home')}#about">${escText(ui['nav.about'])}</a>
        <a href="${pathFor(code, 'home')}#services">${escText(ui['nav.services'])}</a>
        <a href="${pathFor(code, 'home')}#apps">${escText(ui['nav.apps'])}</a>${HAS_REVIEWS ? `
        <a href="${pathFor(code, 'home')}#reviews">${escText(ui['nav.reviews'])}</a>` : ''}
      </nav>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="${escAttr(ui['theme.toggle'])}" title="${escAttr(ui['theme.toggle'])}">
          <span class="ti-dark" aria-hidden="true">🌙</span><span class="ti-light" aria-hidden="true">☀️</span>
        </button>
      ${langSwitcher(code, kind, slug)}
        <button class="nav-toggle" id="navToggle" aria-label="menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>`;
}

function footer(code, ui) {
  return `  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <span class="logo small">Code<span>DAC</span></span>
        <span class="footer-based">${escText(ui['footer.based'])}</span>
      </div>
      <div class="footer-right">
        <a class="footer-email" href="mailto:codedac1@gmail.com">codedac1@gmail.com</a>
        <a class="footer-email" href="${pathFor(code, 'privacy')}">${escText(ui['footer.privacy'])}</a>
        <p>&copy; <span id="year">${new Date().getFullYear()}</span> CodeDAC. All rights reserved.</p>
      </div>
    </div>
  </footer>`;
}


// 히어로 지표 스트립 (출시 앱 수 · 누적 다운로드 · 지원 언어 수)
function statStrip(ui) {
  const items = [
    { num: String(APPS.length), label: ui['stats.apps'] },
    DL_DISPLAY ? { num: DL_DISPLAY, label: ui['stats.downloads'] } : null,
    { num: APP_LANG_DISPLAY || String(ACTIVE.length), label: ui['stats.languages'] },
  ].filter(Boolean);
  // 숫자는 어느 언어에서나 왼쪽에서 오른쪽으로 읽는다. RTL 문서에서 dir 을 명시하지 않으면
  // "12,000+" 의 후행 '+' 가 중립 문자로 취급돼 숫자 왼쪽으로 밀려 "+12,000" 이 된다.
  return `      <ul class="hero-stats">
${items.map((it) => `        <li class="hstat"><span class="hstat-num" dir="ltr">${escText(it.num)}</span><span class="hstat-label">${escText(it.label)}</span></li>`).join('\n')}
      </ul>`;
}

// 후기 카드 1장 (showApp: 어느 앱 리뷰인지 표기 — 홈처럼 여러 앱이 섞일 때 true)
function reviewCard(r, code, showApp) {
  const d = L[code];
  const appName = (d.apps[r.slug] && d.apps[r.slug].name) || r.slug;
  const stars = '★'.repeat(Math.max(1, Math.min(5, r.score || 5)));
  const source = showApp ? `${bdiName(appName)} · Google Play` : 'Google Play';
  return `        <figure class="review-card">
          <div class="review-stars" aria-label="${r.score || 5} / 5">${stars}</div>
          <blockquote class="review-text">${escText(r.text)}</blockquote>
          <figcaption class="review-meta"><span class="review-name">${escText(r.name)}</span><span class="review-app">${source}</span></figcaption>
        </figure>`;
}

// 후기 섹션 (홈=여러 앱 섞음 / 상세=해당 앱만). 목록이 비면 렌더 안 함.
function reviewsSection(code, ui, list, { alt = true, showApp = true } = {}) {
  if (!list.length) return '';
  const cards = list.map((r) => reviewCard(r, code, showApp)).join('\n');
  return `
  <section class="section${alt ? ' section-alt' : ''}" id="reviews">
    <div class="container">
      <p class="section-label">REVIEWS</p>
      <h2 class="section-title">${escText(ui['reviews.title'])}</h2>
      <p class="section-lead">${escText(ui['reviews.lead'])}</p>
      <div class="reviews-grid">
${cards}
      </div>
    </div>
  </section>
`;
}

// 앱 카드 지원 언어 배지 ("🌐 51개 언어") — 언어 데이터가 있는 앱만
function langBadge(slug, ui) {
  const n = langCountOf(slug);
  if (!n) return '';
  const label = String(ui['app.langs']).replace('{n}', n);
  return `<span class="app-langs" aria-label="${escAttr(label)}"><span class="globe" aria-hidden="true">🌐</span>${escText(label)}</span>`;
}

// ---------- 홈 페이지 ----------
function buildHome(lang) {
  const code = lang.code;
  const d = L[code];
  const ui = d.ui;
  const canonical = urlFor(code, 'home');

  const cards = APPS.map((app) => {
    const a = d.apps[app.slug];
    const cardShots = Math.min(app.shots, 3); // 홈 카드는 3장까지만(상세 페이지는 전량)
    const shotsHtml = cardShots ? `
        <div class="app-shots">
${Array.from({ length: cardShots }, (_, i) =>
      `          <img class="shot" src="/images/shots/${app.slug}-${i + 1}.jpg?v=${V}" alt="${escAttr(a.name)} ${escAttr(ui['screenshots'])} ${i + 1}" loading="lazy" data-idx="${i}" />`).join('\n')}
        </div>` : '';
    const store = app.store
      ? `<a class="app-link" href="${escAttr(app.store)}" target="_blank" rel="noopener">${escText(ui['store'])}</a>`
      : '';
    return `        <article class="app-card">
          <div class="app-head">
            <img class="app-icon" src="/images/icons/${app.slug}.png?v=${V}" alt="${escAttr(a.name)} icon" loading="lazy" width="56" height="56" />
            <div class="app-meta"><h3><a href="${pathFor(code, 'detail', app.slug)}">${bdiName(a.name)}</a></h3><span class="app-meta-row"><span class="app-tag">${escText(a.tag)}</span>${langBadge(app.slug, ui)}</span></div>
          </div>
          <p class="app-desc">${escText(a.desc)}</p>${shotsHtml}
          <div class="app-links"><a class="app-more" href="${pathFor(code, 'detail', app.slug)}">${escText(ui['card.detail'])}</a>${store}</div>
        </article>`;
  }).join('\n');

  const orgLd = {
    '@context': 'https://schema.org', '@type': 'Organization',
    name: 'CodeDAC', alternateName: '코드댁', url: `${BASE}/`,
    logo: `${BASE}/images/og-image.png`, image: `${BASE}/images/og-image.png`,
    email: 'codedac1@gmail.com', slogan: 'Code-based Development And Consulting',
    description: String(ui['meta.desc']).replace(/<[^>]+>/g, ''),
    contactPoint: { '@type': 'ContactPoint', email: 'codedac1@gmail.com', contactType: 'customer support' },
  };

  const keywords = `CodeDAC, 코드댁, ${APPS.map((a) => a.name).join(', ')}`;

  return `<!DOCTYPE html>
<html lang="${lang.htmlLang}"${lang.dir ? ` dir="${lang.dir}"` : ''}>
<head>
${headCommon(lang, { title: ui['meta.title'], desc: String(ui['meta.desc']).replace(/<[^>]+>/g, ''), canonical, ogImage: `${BASE}/images/og-image.png`, kind: 'home', keywords })}
  <script type="application/ld+json">
${JSON.stringify(orgLd, null, 2)}
  </script>
</head>
<body>
${header(code, 'home', undefined, ui)}

  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">${ui['hero.eyebrow']}</p>
      <h1>${ui['hero.title']}</h1>
      <p class="hero-sub">${ui['hero.sub']}</p>
      <div class="hero-actions">
        <a href="#apps" class="btn btn-primary">${escText(ui['hero.cta1'])}</a>
        <a href="mailto:codedac1@gmail.com" class="btn btn-ghost">${escText(ui['hero.cta2'])}</a>
      </div>
${statStrip(ui)}
    </div>
  </section>

  <section class="section" id="about">
    <div class="container">
      <p class="section-label">ABOUT</p>
      <h2 class="section-title">${escText(ui['about.title'])}</h2>
      <p class="name-meaning">
        <span class="nm-brand">Code<span>DAC</span></span>
        <span class="nm-eq">=</span>
        <span class="nm-expand">${ui['about.meaning']}</span>
      </p>
      <p class="section-lead">${escText(ui['about.lead'])}</p>
      <div class="grid grid-3">
        <div class="card"><div class="card-icon">🎯</div><h3>${escText(ui['about.c1.t'])}</h3><p>${escText(ui['about.c1.d'])}</p></div>
        <div class="card"><div class="card-icon">🔒</div><h3>${escText(ui['about.c2.t'])}</h3><p>${escText(ui['about.c2.d'])}</p></div>
        <div class="card"><div class="card-icon">🚀</div><h3>${escText(ui['about.c3.t'])}</h3><p>${escText(ui['about.c3.d'])}</p></div>
      </div>
    </div>
  </section>

  <section class="section section-alt" id="services">
    <div class="container">
      <p class="section-label">SERVICES</p>
      <h2 class="section-title">${escText(ui['services.title'])}</h2>
      <p class="section-lead">${escText(ui['services.lead'])}</p>
      <div class="services-grid">
        <div class="card"><div class="card-icon">📱</div><h3>${escText(ui['services.s1.t'])}</h3><p>${escText(ui['services.s1.d'])}</p></div>
        <div class="card"><div class="card-icon">🌐</div><h3>${escText(ui['services.s2.t'])}</h3><p>${escText(ui['services.s2.d'])}</p></div>
        <div class="card"><div class="card-icon">🧭</div><h3>${escText(ui['services.s3.t'])}</h3><p>${escText(ui['services.s3.d'])}</p></div>
        <div class="card"><div class="card-icon">🛠️</div><h3>${escText(ui['services.s4.t'])}</h3><p>${escText(ui['services.s4.d'])}</p></div>
      </div>
      <div class="services-cta">
        <a href="mailto:codedac1@gmail.com?subject=%5BCodeDAC%5D%20Project%20inquiry" class="btn btn-primary">${escText(ui['services.cta'])}</a>
      </div>
    </div>
  </section>

  <section class="section" id="apps">
    <div class="container">
      <p class="section-label">OUR APPS</p>
      <h2 class="section-title">${escText(ui['apps.title'])}</h2>
      <p class="section-lead">${escText(ui['apps.lead'])}</p>
      <div class="app-grid" id="appGrid">
${cards}
      </div>
    </div>
  </section>
${reviewsSection(code, ui, featuredReviews(), { alt: true, showApp: true })}
${footer(code, ui)}

  <div class="lightbox" id="lightbox" aria-hidden="true">
    <button class="lb-close" id="lbClose" aria-label="close">&times;</button>
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="previous">&#8249;</button>
    <img class="lb-img" id="lbImg" alt="" />
    <button class="lb-nav lb-next" id="lbNext" aria-label="next">&#8250;</button>
  </div>

${bannerData(code, 'home', null, ACTIVE)}  <script src="/js/site.js?v=${V}"></script>
</body>
</html>
`;
}

// ---------- 앱 상세 페이지 ----------
function buildDetail(lang, app) {
  const code = lang.code;
  const d = L[code];
  const ui = d.ui;
  const a = d.apps[app.slug];
  const canonical = urlFor(code, 'detail', app.slug);
  const iconAbs = `${BASE}/images/icons/${app.slug}.png`;
  const isWindows = app.slug === 'clipboardwin';
  const os = isWindows ? 'Windows' : 'Android';

  const shotAbs = [];
  for (let i = 1; i <= app.shots; i++) shotAbs.push(`${BASE}/images/shots/${app.slug}-${i}.jpg`);

  const ldApp = {
    '@context': 'https://schema.org', '@type': 'SoftwareApplication',
    name: a.name, operatingSystem: os, applicationCategory: schemaCat(app.slug),
    description: a.long, image: iconAbs, url: canonical,
    inLanguage: lang.hreflang,
    author: { '@type': 'Organization', name: 'CodeDAC', url: `${BASE}/` },
    publisher: { '@type': 'Organization', name: 'CodeDAC', url: `${BASE}/` },
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
  };
  if (shotAbs.length) ldApp.screenshot = shotAbs;
  if (app.store) ldApp.installUrl = app.store;

  const ldBreadcrumb = {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'CodeDAC', item: urlFor(code, 'home') },
      { '@type': 'ListItem', position: 2, name: ui['bc.apps'], item: `${urlFor(code, 'home')}#apps` },
      { '@type': 'ListItem', position: 3, name: a.name, item: canonical },
    ],
  };
  const ldFaq = {
    '@context': 'https://schema.org', '@type': 'FAQPage',
    mainEntity: a.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })),
  };

  const featuresHtml = a.features.map((f) => `        <li>${escText(f)}</li>`).join('\n');
  const faqHtml = a.faq.map((f) =>
    `        <div class="faq-item"><p class="faq-q">${escText(f.q)}</p><p class="faq-a">${escText(f.a)}</p></div>`).join('\n');

  const shotsSection = app.shots ? `
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title">${escText(ui['screenshots'])}</h2>
      <p class="section-lead" style="margin-bottom:22px">${escText(ui['shotsHint'])}</p>
      <div class="detail-shots" id="d-shots">
${Array.from({ length: app.shots }, (_, i) =>
    `        <img class="shot" src="/images/shots/${app.slug}-${i + 1}.jpg?v=${V}" alt="${escAttr(a.name)} ${escAttr(ui['screenshots'])} ${i + 1}" loading="lazy" data-idx="${i}" />`).join('\n')}
      </div>
    </div>
  </section>` : '';

  // 플랫폼(app.platform)과 출시 여부(app.store 유무)는 서로 독립적이다.
  // 넷 중 어떤 조합이든 성립한다:
  //   Android + 출시    → 스토어 버튼
  //   Android + 미출시  → '출시 준비 중'
  //   Windows + 출시    → 다운로드 버튼 + 'Windows 데스크톱 앱'
  //   Windows + 미출시  → 'Windows 데스크톱 앱 · 출시 준비 중'
  const notes = [];
  if (app.platform === 'windows') notes.push(ui['platform.windows']);
  if (!app.store) notes.push(ui['platform.soon']);
  const noteHtml = notes.length
    ? `<span class="app-platform-note">${escText(notes.join(' · '))}</span>`
    : '';
  const storeBtn = app.store
    ? `<a href="${escAttr(app.store)}" class="btn btn-primary" target="_blank" rel="noopener">${escText(ui['store'])}</a>`
    : '';
  const heroAction = `${storeBtn}${noteHtml}`;

  const lightbox = app.shots ? `
  <div class="lightbox" id="lightbox" aria-hidden="true">
    <button class="lb-close" id="lbClose" aria-label="close">&times;</button>
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="previous">&#8249;</button>
    <img class="lb-img" id="lbImg" alt="" />
    <button class="lb-nav lb-next" id="lbNext" aria-label="next">&#8250;</button>
  </div>` : '';

  const title = `${a.name} — ${a.tag} | CodeDAC`;
  const metaDesc = `${a.tagline} — CodeDAC ${a.name}.`;
  const keywords = `${a.name}, ${a.tag}, CodeDAC, 코드댁`;

  return `<!DOCTYPE html>
<html lang="${lang.htmlLang}"${lang.dir ? ` dir="${lang.dir}"` : ''}>
<head>
${headCommon(lang, { title, desc: metaDesc, canonical, ogImage: shotAbs[0] || iconAbs, kind: 'detail', slug: app.slug, keywords })}
  <script type="application/ld+json">
${JSON.stringify(ldApp, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(ldBreadcrumb, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(ldFaq, null, 2)}
  </script>
</head>
<body>
${header(code, 'detail', app.slug, ui)}

  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="${pathFor(code, 'home')}">${escText(ui['bc.home'])}</a>
      <span class="sep">/</span>
      <a href="${pathFor(code, 'home')}#apps">${escText(ui['bc.apps'])}</a>
      <span class="sep">/</span>
      <span class="current">${bdiName(a.name)}</span>
    </nav>
  </div>

  <section class="app-hero-d">
    <div class="container app-hero-inner">
      <img class="app-icon-lg" src="/images/icons/${app.slug}.png?v=${V}" alt="${escAttr(a.name)} icon" width="96" height="96" />
      <div class="app-hero-text">
        <span class="app-meta-row"><span class="app-tag">${escText(a.tag)}</span>${langBadge(app.slug, ui)}</span>
        <h1>${bdiName(a.name)}</h1>
        <p class="app-tagline">${escText(a.tagline)}</p>
        <div class="app-hero-actions">
          ${heroAction}
          <a href="mailto:codedac1@gmail.com" class="btn btn-ghost">${escText(ui['contact'])}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title">${escText(ui['overview'])}</h2>
      <p class="detail-long">${escText(a.long)}</p>
    </div>
  </section>

  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title">${escText(ui['features'])}</h2>
      <ul class="feature-list">
${featuresHtml}
      </ul>
    </div>
  </section>
${shotsSection}
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title">${escText(ui['faq'])}</h2>
      <div class="faq-list">
${faqHtml}
      </div>
    </div>
  </section>
${reviewsFor(app.slug).length ? `
  <section class="detail-section" id="reviews">
    <div class="container">
      <h2 class="detail-title">${escText(ui['reviews.title'])}</h2>
      <p class="section-lead" style="margin-bottom:22px">${escText(ui['reviews.lead'])}</p>
      <div class="reviews-grid">
${reviewsFor(app.slug).map((r) => reviewCard(r, code, false)).join('\n')}
      </div>
    </div>
  </section>` : ''}

  <div class="detail-cta">
    <a href="${pathFor(code, 'home')}#apps" class="btn btn-primary">${escText(ui['otherApps'])}</a>
  </div>

${footer(code, ui)}
${lightbox}
${bannerData(code, 'detail', app.slug, ACTIVE)}  <script src="/js/site.js?v=${V}"></script>
</body>
</html>
`;
}

// ---------- 개인정보처리방침 ----------
function buildPrivacy(lang) {
  const code = lang.code;
  const ui = L[code].ui;
  const pv = PRIV[code];
  const canonical = urlFor(code, 'privacy');
  return `<!DOCTYPE html>
<html lang="${lang.htmlLang}"${lang.dir ? ` dir="${lang.dir}"` : ''}>
<head>
${headCommon(lang, { title: pv.metaTitle, desc: pv.metaDesc, canonical, ogImage: `${BASE}/images/og-image.png`, kind: 'privacy', keywords: `CodeDAC, ${pv.title}`, langSet: PRIV_ACTIVE })}
</head>
<body>
${header(code, 'privacy', undefined, ui)}

  <main class="legal">
    <a href="${pathFor(code, 'home')}" class="back">${escText(pv.back)}</a>
    <h1>${escText(pv.title)}</h1>
    <p class="eff">${escText(pv.effective)}</p>
${pv.bodyHtml}
  </main>

${footer(code, ui)}
${bannerData(code, 'privacy', null, PRIV_ACTIVE)}  <script src="/js/site.js?v=${V}"></script>
</body>
</html>
`;
}

// --- 파일 쓰기 헬퍼 ---
function writeOut(rel, content) {
  const full = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, 'utf8');
}

// --- 생성 ---
let pages = 0;
for (const lang of ACTIVE) {
  writeOut(fileFor(lang.code, 'home'), buildHome(lang));
  pages++;
  for (const app of APPS) {
    writeOut(fileFor(lang.code, 'detail', app.slug), buildDetail(lang, app));
    pages++;
  }
  if (PRIV[lang.code]) { writeOut(fileFor(lang.code, 'privacy'), buildPrivacy(lang)); pages++; }
}

// --- sitemap.xml (언어별 대체 링크 포함) ---
function sitemapUrl(kind, slug, langSet) {
  const set = langSet || ACTIVE;
  const alts = set.map((l) =>
    `    <xhtml:link rel="alternate" hreflang="${l.hreflang}" href="${urlFor(l.code, kind, slug)}" />`
  );
  const xd = set.find((l) => l.code === XDEFAULT) || set[0];
  alts.push(`    <xhtml:link rel="alternate" hreflang="x-default" href="${urlFor(xd.code, kind, slug)}" />`);
  const priority = kind === 'home' ? '1.0' : (kind === 'privacy' ? '0.3' : '0.7');
  const changefreq = kind === 'privacy' ? 'yearly' : 'monthly';
  // 각 언어 버전마다 <url> 하나씩, 대체 링크는 공통
  return set.map((l) => `  <url>
    <loc>${urlFor(l.code, kind, slug)}</loc>
${alts.join('\n')}
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`).join('\n');
}
const urls = [sitemapUrl('home')];
for (const app of APPS) urls.push(sitemapUrl('detail', app.slug));
urls.push(sitemapUrl('privacy', undefined, PRIV_ACTIVE));
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls.join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemap, 'utf8');

console.log(`생성 완료: ${ACTIVE.length}개 언어, ${pages}개 페이지, sitemap.xml`);
console.log(`언어: ${ACTIVE.map((l) => l.code).join(', ')}`);
