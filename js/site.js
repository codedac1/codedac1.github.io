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
