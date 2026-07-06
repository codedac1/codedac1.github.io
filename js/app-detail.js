// =====================================================================
//  CodeDAC 앱 상세 페이지 스크립트
//  - 각 상세 페이지(apps/<slug>.html)의 <script id="app-data"> 데이터 섬을
//    읽어 언어(KR/EN)에 맞게 본문을 다시 그린다.
//  - 정적 HTML에는 한국어 본문이 미리 렌더링되어 있어(크롤러용), JS는
//    사용자가 EN을 고르거나 영어권 접속일 때 영어로 교체한다.
// =====================================================================

// ===== 공통 UI 문구(모든 상세 페이지 공용) =====
const UI = {
  ko: {
    'nav.about': '회사 소개', 'nav.services': '서비스', 'nav.apps': '앱 소개',
    'bc.home': '홈', 'bc.apps': '앱 소개',
    'overview': '개요', 'features': '주요 기능', 'faq': '자주 묻는 질문',
    'screenshots': '스크린샷', 'shotsHint': '스크린샷을 누르면 크게 볼 수 있습니다.',
    'store': 'Google Play에서 보기 →', 'contact': '문의하기',
    'otherApps': '다른 앱 둘러보기', 'footer.privacy': '개인정보처리방침',
  },
  en: {
    'nav.about': 'About', 'nav.services': 'Services', 'nav.apps': 'Apps',
    'bc.home': 'Home', 'bc.apps': 'Apps',
    'overview': 'Overview', 'features': 'Key Features', 'faq': 'FAQ',
    'screenshots': 'Screenshots', 'shotsHint': 'Tap a screenshot to view it larger.',
    'store': 'View on Google Play →', 'contact': 'Contact us',
    'otherApps': 'Explore more apps', 'footer.privacy': 'Privacy Policy',
  },
};

// ===== 페이지 데이터 섬 읽기 =====
const DATA = JSON.parse(document.getElementById('app-data').textContent);

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ===== 본문 렌더링 =====
function renderDetail(lang) {
  const d = DATA;

  const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  set('d-category', d.category[lang]);
  set('d-tagline', d.tagline[lang]);
  set('d-long', d.long[lang]);

  const feat = document.getElementById('d-features');
  if (feat) feat.innerHTML = d.features[lang].map((f) => `<li>${esc(f)}</li>`).join('');

  const faq = document.getElementById('d-faq');
  if (faq) faq.innerHTML = d.faq[lang].map((item) =>
    `<div class="faq-item"><p class="faq-q">${esc(item.q)}</p><p class="faq-a">${esc(item.a)}</p></div>`
  ).join('');
}

// ===== 정적 라벨 적용 =====
function applyUi(lang) {
  const dict = UI[lang] || UI.ko;
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const t = dict[el.getAttribute('data-i18n')];
    if (t !== undefined) el.textContent = t;
  });
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('is-active', btn.dataset.lang === lang);
  });
}

// ===== 언어 결정 (index와 동일 규칙) =====
function detectLang() {
  const saved = localStorage.getItem('lang');
  if (saved === 'ko' || saved === 'en') return saved;
  const langs = navigator.languages || [navigator.language || ''];
  if (langs.some((l) => (l || '').toLowerCase().startsWith('ko'))) return 'ko';
  try {
    if (Intl.DateTimeFormat().resolvedOptions().timeZone === 'Asia/Seoul') return 'ko';
  } catch (e) { /* 무시 */ }
  return 'en';
}

function applyLang(lang, persist) {
  document.documentElement.lang = lang;
  applyUi(lang);
  renderDetail(lang);
  if (persist) localStorage.setItem('lang', lang);
}

document.querySelectorAll('.lang-btn').forEach((btn) => {
  btn.addEventListener('click', () => applyLang(btn.dataset.lang, true));
});
applyLang(detectLang(), false);

// ===== 스크린샷 라이트박스 =====
const lightbox = document.getElementById('lightbox');
if (lightbox) {
  const lbImg = document.getElementById('lbImg');
  const shots = DATA.shots || [];
  let lbIndex = 0;
  const show = () => { lbImg.src = shots[lbIndex]; };
  const open = (idx) => {
    lbIndex = idx; show();
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
  };
  const close = () => {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    lbImg.src = '';
  };
  const step = (dir) => { lbIndex = (lbIndex + dir + shots.length) % shots.length; show(); };

  const shotsWrap = document.getElementById('d-shots');
  if (shotsWrap) shotsWrap.addEventListener('click', (e) => {
    const img = e.target.closest('.shot');
    if (img) open(Number(img.dataset.idx));
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
}

// ===== 현재 연도 =====
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ===== 모바일 메뉴 =====
const navToggle = document.getElementById('navToggle');
const nav = document.getElementById('nav');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });
}
