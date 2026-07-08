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

  // 사용자가 언어를 직접 고르면 저장해 둔다. 루트(한국어) 페이지의 자동 감지
  // 리다이렉트는 이 값을 우선 존중하므로, 선택이 매번 덮어써지지 않는다.
  menu.querySelectorAll('.lang-item').forEach((a) => {
    a.addEventListener('click', () => {
      const code = (a.getAttribute('hreflang') || '').toLowerCase().split('-')[0];
      if (code) { try { localStorage.setItem('lang', code); } catch (e) { /* 저장 불가 무시 */ } }
    });
  });
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
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') step(-1);
    else if (e.key === 'ArrowRight') step(1);
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
