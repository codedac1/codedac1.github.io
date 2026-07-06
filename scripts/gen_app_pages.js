// =====================================================================
//  앱 상세 페이지 생성기
//  - 데이터 소스: js/main.js 의 APPS(기본 정보) + scripts/apps_content.json(상세 콘텐츠)
//  - 출력: apps/<slug>.html (검색엔진용 한국어 정적 본문 + KR/EN 토글 데이터 섬)
//         및 sitemap.xml 재생성
//  사용: node scripts/gen_app_pages.js
// =====================================================================
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const BASE = 'https://codedac1.github.io';
const OUT_DIR = path.join(ROOT, 'apps');
const LASTMOD = new Date().toISOString().slice(0, 10);

// --- js/main.js 에서 APPS 배열과 캐시 버전 V 추출 ---
const mainSrc = fs.readFileSync(path.join(ROOT, 'js', 'main.js'), 'utf8');
const aStart = mainSrc.indexOf('const APPS = [');
const aEnd = mainSrc.indexOf('\n];', aStart) + 3;
const APPS = eval(mainSrc.slice(aStart + 'const APPS = '.length, aEnd - 1));
const V = (mainSrc.match(/const V = '(\d+)'/) || [, '14'])[1];

const CONTENT = require('./apps_content.json');

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');
const escText = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// <script type="application/json"> 안에 안전하게 넣기 위해 '<' 이스케이프
const jsonIsland = (obj) => JSON.stringify(obj).replace(/</g, '\\u003c');

// applicationCategory (schema.org) 매핑
const APP_CATEGORY = {
  'Kids': 'EducationalApplication',
  'Parenting': 'LifestyleApplication',
};
const categoryFor = (en) => APP_CATEGORY[en] || 'UtilitiesApplication';

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR);

const sitemapUrls = [
  { loc: `${BASE}/`, priority: '1.0', changefreq: 'monthly' },
];

function buildPage(app) {
  const c = CONTENT[app.slug];
  if (!c) throw new Error(`apps_content.json 에 '${app.slug}' 항목이 없습니다.`);

  const url = `${BASE}/apps/${app.slug}.html`;
  const iconAbs = `${BASE}/images/icons/${app.slug}.png`;
  const isWindows = c.category.en === 'Windows App';
  const os = isWindows ? 'Windows' : 'Android';

  // 스크린샷 (상대경로: apps/ 하위이므로 ../)
  const shotRel = [];
  const shotAbs = [];
  for (let i = 1; i <= app.shots; i++) {
    shotRel.push(`../images/shots/${app.slug}-${i}.jpg?v=${V}`);
    shotAbs.push(`${BASE}/images/shots/${app.slug}-${i}.jpg`);
  }

  // 데이터 섬(토글용): 한/영 전체 + 라이트박스용 스크린샷 경로
  const island = {
    slug: app.slug,
    category: c.category,
    tagline: c.tagline,
    long: c.long,
    features: c.features,
    faq: c.faq,
    shots: shotRel,
  };

  // ---- JSON-LD ----
  const ldApp = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: app.name,
    operatingSystem: os,
    applicationCategory: categoryFor(c.category.en),
    description: c.long.en,
    image: iconAbs,
    url,
    author: { '@type': 'Organization', name: 'CodeDAC', url: `${BASE}/` },
    publisher: { '@type': 'Organization', name: 'CodeDAC', url: `${BASE}/` },
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
  };
  if (shotAbs.length) ldApp.screenshot = shotAbs;
  if (app.store) ldApp.installUrl = app.store;

  const ldBreadcrumb = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'CodeDAC', item: `${BASE}/` },
      { '@type': 'ListItem', position: 2, name: '앱 소개', item: `${BASE}/#apps` },
      { '@type': 'ListItem', position: 3, name: app.name, item: url },
    ],
  };

  const ldFaq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: c.faq.ko.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };

  // ---- 조각 렌더 (기본 = 한국어, 크롤러가 읽는 본문) ----
  const featuresHtml = c.features.ko.map((f) => `        <li>${escText(f)}</li>`).join('\n');
  const faqHtml = c.faq.ko.map((f) =>
    `        <div class="faq-item"><p class="faq-q">${escText(f.q)}</p><p class="faq-a">${escText(f.a)}</p></div>`
  ).join('\n');

  const shotsSection = app.shots ? `
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title" data-i18n="screenshots">스크린샷</h2>
      <p class="section-lead" data-i18n="shotsHint" style="margin-bottom:22px">스크린샷을 누르면 크게 볼 수 있습니다.</p>
      <div class="detail-shots" id="d-shots">
${shotRel.map((s, i) => `        <img class="shot" src="${s}" alt="${esc(app.name)} 스크린샷 ${i + 1}" loading="lazy" data-idx="${i}" />`).join('\n')}
      </div>
    </div>
  </section>` : '';

  const heroAction = app.store
    ? `<a href="${esc(app.store)}" class="btn btn-primary" target="_blank" rel="noopener" data-i18n="store">Google Play에서 보기 →</a>`
    : `<span class="app-platform-note">Windows 데스크톱 앱</span>`;

  const lightbox = app.shots ? `
  <div class="lightbox" id="lightbox" aria-hidden="true">
    <button class="lb-close" id="lbClose" aria-label="close">&times;</button>
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="previous">&#8249;</button>
    <img class="lb-img" id="lbImg" alt="" />
    <button class="lb-nav lb-next" id="lbNext" aria-label="next">&#8250;</button>
  </div>` : '';

  const metaDesc = `${c.tagline.ko} — CodeDAC ${app.name}.`;
  const title = `${app.name} — ${c.category.ko} | CodeDAC`;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(metaDesc)}" />
  <meta name="keywords" content="${esc(app.name)}, ${esc(c.category.ko)}, CodeDAC, 코드댁, ${esc(app.name)} ${isWindows ? 'Windows' : '안드로이드'}, ${isWindows ? 'Windows app' : 'Android app'}" />
  <meta name="author" content="CodeDAC" />
  <meta name="robots" content="index, follow" />
  <meta name="theme-color" content="#2f6bff" />
  <link rel="canonical" href="${url}" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CodeDAC" />
  <meta property="og:title" content="${esc(title)}" />
  <meta property="og:description" content="${esc(c.tagline.ko)}" />
  <meta property="og:url" content="${url}" />
  <meta property="og:image" content="${shotAbs[0] || iconAbs}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${esc(title)}" />
  <meta name="twitter:description" content="${esc(c.tagline.ko)}" />
  <meta name="twitter:image" content="${shotAbs[0] || iconAbs}" />

  <script type="application/ld+json">
${JSON.stringify(ldApp, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(ldBreadcrumb, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(ldFaq, null, 2)}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect rx='22' width='100' height='100' fill='%232f6bff'/%3E%3Ctext x='50' y='72' font-size='64' font-family='Arial,sans-serif' font-weight='bold' fill='white' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E" />
  <link rel="stylesheet" href="../css/style.css?v=${V}" />
</head>
<body>
  <!-- ===== 상단 네비게이션 ===== -->
  <header class="site-header" id="top">
    <div class="container nav-wrap">
      <a href="../" class="logo">Code<span>DAC</span></a>
      <nav class="nav" id="nav">
        <a href="../#about" data-i18n="nav.about">회사 소개</a>
        <a href="../#services" data-i18n="nav.services">서비스</a>
        <a href="../#apps" data-i18n="nav.apps">앱 소개</a>
      </nav>
      <div class="nav-right">
        <div class="lang-switch" role="group" aria-label="Language">
          <button type="button" class="lang-btn is-active" data-lang="ko">KR</button>
          <span class="lang-sep">|</span>
          <button type="button" class="lang-btn" data-lang="en">EN</button>
        </div>
        <button class="nav-toggle" id="navToggle" aria-label="menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <!-- ===== 브레드크럼 ===== -->
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="../" data-i18n="bc.home">홈</a>
      <span class="sep">/</span>
      <a href="../#apps" data-i18n="bc.apps">앱 소개</a>
      <span class="sep">/</span>
      <span class="current">${esc(app.name)}</span>
    </nav>
  </div>

  <!-- ===== 앱 헤더 ===== -->
  <section class="app-hero-d">
    <div class="container app-hero-inner">
      <img class="app-icon-lg" src="../images/icons/${app.slug}.png?v=${V}" alt="${esc(app.name)} 아이콘" width="96" height="96" />
      <div class="app-hero-text">
        <span class="app-tag" id="d-category">${escText(c.category.ko)}</span>
        <h1>${esc(app.name)}</h1>
        <p class="app-tagline" id="d-tagline">${escText(c.tagline.ko)}</p>
        <div class="app-hero-actions">
          ${heroAction}
          <a href="mailto:codedac1@gmail.com" class="btn btn-ghost" data-i18n="contact">문의하기</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== 개요 ===== -->
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title" data-i18n="overview">개요</h2>
      <p class="detail-long" id="d-long">${escText(c.long.ko)}</p>
    </div>
  </section>

  <!-- ===== 주요 기능 ===== -->
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title" data-i18n="features">주요 기능</h2>
      <ul class="feature-list" id="d-features">
${featuresHtml}
      </ul>
    </div>
  </section>
${shotsSection}
  <!-- ===== FAQ ===== -->
  <section class="detail-section">
    <div class="container">
      <h2 class="detail-title" data-i18n="faq">자주 묻는 질문</h2>
      <div class="faq-list" id="d-faq">
${faqHtml}
      </div>
    </div>
  </section>

  <!-- ===== 다른 앱 CTA ===== -->
  <div class="detail-cta">
    <a href="../#apps" class="btn btn-primary" data-i18n="otherApps">다른 앱 둘러보기</a>
  </div>

  <!-- ===== 푸터 ===== -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <span class="logo small">Code<span>DAC</span></span>
      <div class="footer-right">
        <a class="footer-email" href="mailto:codedac1@gmail.com">codedac1@gmail.com</a>
        <a class="footer-email" href="../privacy.html" data-i18n="footer.privacy">개인정보처리방침</a>
        <p>&copy; <span id="year"></span> CodeDAC. All rights reserved.</p>
      </div>
    </div>
  </footer>
${lightbox}
  <script type="application/json" id="app-data">${jsonIsland(island)}</script>
  <script src="../js/app-detail.js?v=${V}"></script>
</body>
</html>
`;
}

// --- 생성 실행 ---
let count = 0;
for (const app of APPS) {
  const html = buildPage(app);
  fs.writeFileSync(path.join(OUT_DIR, `${app.slug}.html`), html, 'utf8');
  sitemapUrls.push({ loc: `${BASE}/apps/${app.slug}.html`, priority: '0.7', changefreq: 'monthly' });
  count++;
}

// --- sitemap.xml 재생성 (개인정보 처리방침 포함) ---
sitemapUrls.push({ loc: `${BASE}/privacy.html`, priority: '0.3', changefreq: 'yearly' });
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapUrls.map((u) => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemap, 'utf8');

console.log(`생성 완료: apps/*.html ${count}개, sitemap.xml (${sitemapUrls.length} URLs)`);
