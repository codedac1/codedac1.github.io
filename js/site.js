// =====================================================================
//  CodeDAC 공용 스크립트 (모든 정적 페이지 공용)
//  - 콘텐츠는 언어별 정적 HTML로 이미 렌더링돼 있으므로, 이 스크립트는
//    상호작용(언어 드롭다운 · 모바일 메뉴 · 스크린샷 라이트박스)만 담당한다.
// =====================================================================

// ===== 언어 드롭다운 =====
(function () {
  const btn = document.getElementById('langBtn');
  const menu = document.getElementById('langMenu');
  if (!btn || !menu) return;
  const close = () => { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); };
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', (e) => { if (!menu.contains(e.target)) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });

  // 사용자가 언어를 직접 고르면 저장해 둔다. 루트(한국어) 페이지는 이 값이 있을 때만
  // 리다이렉트하므로, 저장되는 값은 반드시 폴더 코드여야 한다.
  // hreflang 에서 코드를 되짚으면 안 된다 — 필리핀어는 hreflang 이 'tl' 이라 '/tl/' 로
  // 저장되고, 중국어는 'zh-Hans' 를 잘라 'zh' 가 되는 식으로 어긋난다.
  menu.querySelectorAll('.lang-item').forEach((a) => {
    a.addEventListener('click', () => {
      const code = a.getAttribute('data-lang');
      if (code) { try { localStorage.setItem('lang', code); } catch (e) { /* 저장 불가 무시 */ } }
    });
  });
})();

// ===== 언어 제안 배너 =====
//  브라우저 언어만 보고 방문자를 다른 언어로 자동 이동시키지 않는다(구글 권장).
//  대신 읽을 수 있을 법한 언어가 따로 있으면 배너로 제안만 하고 선택은 맡긴다.
//  - 이전에 스스로 고른 언어가 있으면 그 언어를 제안한다(브라우저 언어보다 우선).
//  - 한 번 닫으면 다시 띄우지 않는다.
//  - 배너 문구·링크는 gen_site.js 가 window.__LANG_BANNER 로 인라인 주입한다.
(function () {
  const D = window.__LANG_BANNER;
  if (!D || !D.langs) return;

  const get = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  if (get('langBannerOff')) return;

  const langs = D.langs;
  const has = (c) => typeof c === 'string' && Object.prototype.hasOwnProperty.call(langs, c);

  // 저장된 선택이 먼저. 없으면 브라우저 언어를 순서대로 훑는다.
  let pick = null;
  const stored = get('lang');
  if (has(stored)) pick = stored;
  else {
    const list = navigator.languages || [navigator.language || ''];
    for (let i = 0; i < list.length; i++) {
      const base = String(list[i]).toLowerCase().split('-')[0];
      const code = (typeof D.alias[base] === 'string') ? D.alias[base] : base;
      if (has(code)) { pick = code; break; }
    }
  }
  // 방문자가 가장 먼저 원하는 언어가 이미 이 페이지의 언어라면 제안할 것이 없다.
  if (!pick || pick === D.cur) return;

  const t = langs[pick];
  const bar = document.createElement('div');
  bar.className = 'lang-banner';
  // 배너 내용만 대상 언어의 방향으로 쓴다. 문서 방향은 그대로 둔다.
  bar.setAttribute('dir', t.r);
  bar.lang = pick;

  const text = document.createElement('span');
  text.className = 'lang-banner-text';
  text.textContent = t.t;

  const cta = document.createElement('a');
  cta.className = 'lang-banner-cta';
  cta.href = t.u;
  cta.textContent = t.c;
  // 배너로 이동한 것도 명시적 선택으로 본다. 다음 방문부터 그 언어로 바로 간다.
  cta.addEventListener('click', () => { try { localStorage.setItem('lang', pick); } catch (e) { /* 무시 */ } });

  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'lang-banner-close';
  close.setAttribute('aria-label', t.d);
  close.title = t.d;
  close.textContent = '×';
  close.addEventListener('click', () => {
    bar.remove();
    try { localStorage.setItem('langBannerOff', '1'); } catch (e) { /* 무시 */ }
  });

  bar.append(text, cta, close);
  document.body.appendChild(bar);
})();

// ===== 모바일 메뉴 =====
(function () {
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');
  if (!navToggle || !nav) return;
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });
})();

// ===== 스크린샷 라이트박스 =====
(function () {
  const lightbox = document.getElementById('lightbox');
  if (!lightbox) return;
  const lbImg = document.getElementById('lbImg');
  let list = [];
  let idx = 0;
  const show = () => { lbImg.src = list[idx]; };
  const open = (srcs, start) => {
    list = srcs; idx = start; show();
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
  };
  const close = () => {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    lbImg.src = '';
  };
  const step = (dir) => { idx = (idx + dir + list.length) % list.length; show(); };

  // 클릭한 썸네일이 속한 그룹(.app-shots 또는 .detail-shots)의 이미지들을 모은다
  document.addEventListener('click', (e) => {
    const img = e.target.closest('.shot');
    if (!img) return;
    const group = img.closest('.app-shots, .detail-shots');
    if (!group) return;
    const imgs = [...group.querySelectorAll('.shot')];
    open(imgs.map((i) => i.src), imgs.indexOf(img));
  });
  document.getElementById('lbClose').addEventListener('click', close);
  document.getElementById('lbPrev').addEventListener('click', (e) => { e.stopPropagation(); step(-1); });
  document.getElementById('lbNext').addEventListener('click', (e) => { e.stopPropagation(); step(1); });
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) close(); });
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    // RTL에서는 이미지가 오른쪽에서 왼쪽으로 늘어서므로 좌우 키의 의미도 뒤집는다.
    const rtl = document.documentElement.getAttribute('dir') === 'rtl';
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') step(rtl ? 1 : -1);
    else if (e.key === 'ArrowRight') step(rtl ? -1 : 1);
  });
})();

// ===== 현재 연도 (정적 렌더값 보정) =====
(function () {
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

// ===== 다크 모드 토글 (초기 테마는 <head> 인라인 스크립트가 설정) =====
(function () {
  const btn = document.getElementById('themeToggle');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) { /* 저장 불가 무시 */ }
  });
})();

// ===== 헤더 스크롤 그림자 =====
(function () {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// ===== 스크롤 리빌 애니메이션 (콘텐츠 변경 없이 진행 강화) =====
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // 리빌 대상: 섹션 헤더 문구·카드·앱 카드·상세 섹션
  const targets = document.querySelectorAll(
    '.section-label, .section-title, .section-lead, .name-meaning, .card, .app-card, ' +
    '.services-cta, .detail-section, .app-hero-inner, .faq-item'
  );
  if (!targets.length) return;
  if (reduce || !('IntersectionObserver' in window)) {
    targets.forEach((el) => el.classList.add('is-in'));
    return;
  }
  targets.forEach((el) => el.classList.add('reveal'));
  const io = new IntersectionObserver((entries) => {
    // 한 번에 들어오는 카드들이 살짝 순차적으로 나타나도록 배치 내에서만 지연
    let n = 0;
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      io.unobserve(el);
      const delay = Math.min(n++, 5) * 55;
      if (delay) setTimeout(() => el.classList.add('is-in'), delay);
      else el.classList.add('is-in');
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  targets.forEach((el) => io.observe(el));
})();
