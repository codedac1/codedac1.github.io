// =====================================================================
//  CodeDAC 다국어 사이트 생성기 (single source of truth)
//  - 데이터: scripts/apps_base.json (앱 기본정보) + i18n/<code>.json (언어별 문구)
//  - 출력:
//      /                         홈 (ko, 루트)
//      /apps/<slug>.html         앱 상세 (ko)
//      /<code>/                  홈 (en, ja, es, pt, de, fr, id, hi, vi)
//      /<code>/apps/<slug>.html  앱 상세
//      sitemap.xml               (hreflang 대체 링크 포함)
//  - 모든 페이지에 hreflang 대체 링크가 들어가 시장별 SEO를 지원한다.
//  사용: node scripts/gen_site.js
// =====================================================================
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const BASE = 'https://codedac1.github.io';
const V = '16'; // 자산 캐시 버전 (css/js). 자산 변경 시 올릴 것.
const LASTMOD = new Date().toISOString().slice(0, 10);

// 언어 정의 (표시 순서 = 스위처 순서). code=폴더/파일, hreflang=검색엔진용
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
];
const XDEFAULT = 'en';

// schema.org applicationCategory (slug 기준)
const APP_SCHEMA_CAT = {
  colorcards: 'EducationalApplication',
  wordcards: 'EducationalApplication',
  sleepbaby: 'LifestyleApplication',
};
const schemaCat = (slug) => APP_SCHEMA_CAT[slug] || 'UtilitiesApplication';

// --- 데이터 로드 ---
const APPS = require('./apps_base.json');
const L = {};
for (const lang of LANGS) {
  const p = path.join(ROOT, 'i18n', `${lang.code}.json`);
  if (!fs.existsSync(p)) { console.warn(`(경고) i18n/${lang.code}.json 없음 — 이 언어는 건너뜀`); continue; }
  L[lang.code] = require(p);
}
const ACTIVE = LANGS.filter((l) => L[l.code]);

// --- 유틸 ---
const escText = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = (s) => escText(s).replace(/"/g, '&quot;');

// 내부 링크(루트 절대경로) — 사용자 사이트(codedac1.github.io)라 / 로 시작 가능
function pathFor(code, kind, slug) {
  const dir = code === 'ko' ? '/' : `/${code}/`;
  return kind === 'home' ? dir : `${dir}apps/${slug}.html`;
}
// 절대 URL (canonical/hreflang/OG)
function urlFor(code, kind, slug) {
  return BASE + pathFor(code, kind, slug);
}
// 출력 파일 경로
function fileFor(code, kind, slug) {
  const dir = code === 'ko' ? '' : `${code}/`;
  return kind === 'home' ? `${dir}index.html` : `${dir}apps/${slug}.html`;
}

// hreflang 대체 링크 블록
function hreflangLinks(kind, slug) {
  const links = ACTIVE.map((l) =>
    `  <link rel="alternate" hreflang="${l.hreflang}" href="${urlFor(l.code, kind, slug)}" />`
  );
  const xd = ACTIVE.find((l) => l.code === XDEFAULT) || ACTIVE[0];
  links.push(`  <link rel="alternate" hreflang="x-default" href="${urlFor(xd.code, kind, slug)}" />`);
  return links.join('\n');
}

// 언어 스위처 (드롭다운)
function langSwitcher(curCode, kind, slug) {
  const cur = LANGS.find((l) => l.code === curCode);
  const items = ACTIVE.map((l) => {
    const active = l.code === curCode ? ' is-active' : '';
    return `        <a class="lang-item${active}" href="${pathFor(l.code, kind, slug)}" hreflang="${l.hreflang}" lang="${l.htmlLang}">${l.native}</a>`;
  }).join('\n');
  return `<div class="lang-switch">
        <button type="button" class="lang-btn" id="langBtn" aria-haspopup="true" aria-expanded="false">${cur.native} <span class="caret">▾</span></button>
        <div class="lang-menu" id="langMenu" role="menu">
${items}
        </div>
      </div>`;
}

const FAVICON = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect rx='22' width='100' height='100' fill='%232f6bff'/%3E%3Ctext x='50' y='72' font-size='64' font-family='Arial,sans-serif' font-weight='bold' fill='white' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E`;

function headCommon(lang, { title, desc, canonical, ogImage, kind, slug, keywords }) {
  return `  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="EEOUsUwfv3SoTVMdi2dL1EePYJ9cLNKexZgbojtycc0" />
  <meta name="naver-site-verification" content="15e984a2c53000d6d9b698695cbaebf8a3359c0b" />
  <title>${escText(title)}</title>
  <meta name="description" content="${escAttr(desc)}" />
  <meta name="keywords" content="${escAttr(keywords)}" />
  <meta name="author" content="CodeDAC" />
  <meta name="robots" content="index, follow" />
  <meta name="theme-color" content="#2f6bff" />
  <link rel="canonical" href="${canonical}" />
${hreflangLinks(kind, slug)}

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CodeDAC" />
  <meta property="og:locale" content="${lang.hreflang.replace('-', '_')}" />
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
        <a href="${pathFor(code, 'home')}#apps">${escText(ui['nav.apps'])}</a>
      </nav>
      <div class="nav-right">
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
      <span class="logo small">Code<span>DAC</span></span>
      <div class="footer-right">
        <a class="footer-email" href="mailto:codedac1@gmail.com">codedac1@gmail.com</a>
        <a class="footer-email" href="/privacy.html">${escText(ui['footer.privacy'])}</a>
        <p>&copy; <span id="year">${new Date().getFullYear()}</span> CodeDAC. All rights reserved.</p>
      </div>
    </div>
  </footer>`;
}

const TECH = ['Android', 'Java', 'Gradle', '.NET / C#', 'WPF', 'Google Play Services', 'JavaScript', 'Git · GitHub'];

// ---------- 홈 페이지 ----------
function buildHome(lang) {
  const code = lang.code;
  const d = L[code];
  const ui = d.ui;
  const canonical = urlFor(code, 'home');

  const cards = APPS.map((app) => {
    const a = d.apps[app.slug];
    const shotsHtml = app.shots ? `
        <div class="app-shots">
${Array.from({ length: app.shots }, (_, i) =>
      `          <img class="shot" src="/images/shots/${app.slug}-${i + 1}.jpg?v=${V}" alt="${escAttr(a.name)} ${escAttr(ui['screenshots'])} ${i + 1}" loading="lazy" data-idx="${i}" />`).join('\n')}
        </div>` : '';
    const store = app.store
      ? `<a class="app-link" href="${escAttr(app.store)}" target="_blank" rel="noopener">${escText(ui['store'])}</a>`
      : '';
    return `        <article class="app-card">
          <div class="app-head">
            <img class="app-icon" src="/images/icons/${app.slug}.png?v=${V}" alt="${escAttr(a.name)} icon" loading="lazy" width="56" height="56" />
            <div class="app-meta"><h3><a href="${pathFor(code, 'detail', app.slug)}">${escText(a.name)}</a></h3><span class="app-tag">${escText(a.tag)}</span></div>
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
<html lang="${lang.htmlLang}">
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
      <div class="tech-stack">
        <p class="tech-label">${escText(ui['services.tech'])}</p>
        <ul class="tech-badges">${TECH.map((t) => `<li>${escText(t)}</li>`).join('')}</ul>
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

${footer(code, ui)}

  <div class="lightbox" id="lightbox" aria-hidden="true">
    <button class="lb-close" id="lbClose" aria-label="close">&times;</button>
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="previous">&#8249;</button>
    <img class="lb-img" id="lbImg" alt="" />
    <button class="lb-nav lb-next" id="lbNext" aria-label="next">&#8250;</button>
  </div>

  <script src="/js/site.js?v=${V}"></script>
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

  const heroAction = app.store
    ? `<a href="${escAttr(app.store)}" class="btn btn-primary" target="_blank" rel="noopener">${escText(ui['store'])}</a>`
    : `<span class="app-platform-note">${escText(ui['platform.windows'])}</span>`;

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
<html lang="${lang.htmlLang}">
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
      <span class="current">${escText(a.name)}</span>
    </nav>
  </div>

  <section class="app-hero-d">
    <div class="container app-hero-inner">
      <img class="app-icon-lg" src="/images/icons/${app.slug}.png?v=${V}" alt="${escAttr(a.name)} icon" width="96" height="96" />
      <div class="app-hero-text">
        <span class="app-tag">${escText(a.tag)}</span>
        <h1>${escText(a.name)}</h1>
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

  <div class="detail-cta">
    <a href="${pathFor(code, 'home')}#apps" class="btn btn-primary">${escText(ui['otherApps'])}</a>
  </div>

${footer(code, ui)}
${lightbox}
  <script src="/js/site.js?v=${V}"></script>
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
const sitemapEntries = []; // {kind, slug}
for (const lang of ACTIVE) {
  writeOut(fileFor(lang.code, 'home'), buildHome(lang));
  pages++;
  for (const app of APPS) {
    writeOut(fileFor(lang.code, 'detail', app.slug), buildDetail(lang, app));
    pages++;
  }
}

// --- sitemap.xml (언어별 대체 링크 포함) ---
function sitemapUrl(kind, slug) {
  const alts = ACTIVE.map((l) =>
    `    <xhtml:link rel="alternate" hreflang="${l.hreflang}" href="${urlFor(l.code, kind, slug)}" />`
  );
  const xd = ACTIVE.find((l) => l.code === XDEFAULT) || ACTIVE[0];
  alts.push(`    <xhtml:link rel="alternate" hreflang="x-default" href="${urlFor(xd.code, kind, slug)}" />`);
  // loc = 각 언어 버전마다 하나씩 (여기서는 대표로 ko/루트 및 각 언어를 모두 등록)
  return ACTIVE.map((l) => `  <url>
    <loc>${urlFor(l.code, kind, slug)}</loc>
${alts.join('\n')}
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${kind === 'home' ? '1.0' : '0.7'}</priority>
  </url>`).join('\n');
}
const urls = [sitemapUrl('home')];
for (const app of APPS) urls.push(sitemapUrl('detail', app.slug));
urls.push(`  <url>
    <loc>${BASE}/privacy.html</loc>
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>`);
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls.join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemap, 'utf8');

console.log(`생성 완료: ${ACTIVE.length}개 언어, ${pages}개 페이지, sitemap.xml`);
console.log(`언어: ${ACTIVE.map((l) => l.code).join(', ')}`);
