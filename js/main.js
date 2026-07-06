// =====================================================================
//  CodeDAC 홈페이지 스크립트
//  - I18N: 정적 UI 문구(국문/영문)
//  - APPS: 앱 목록 데이터(국문/영문) → 카드 자동 생성
// =====================================================================

// ===== 다국어(i18n) 사전 : UI 문구 =====
const I18N = {
  ko: {
    'meta.title': 'CodeDAC | 스마트폰 유틸리티 앱',
    'meta.desc': 'CodeDAC는 Clipboard+, AutoStart+, FloatCalc+ 등 13종의 스마트폰 유틸리티 앱을 만들고 배포합니다.',

    'nav.about': '회사 소개',
    'nav.services': '서비스',
    'nav.apps': '앱 소개',

    'hero.eyebrow': 'SMARTPHONE UTILITY APPS',
    'hero.title': '스마트폰을<br />더 스마트하게',
    'hero.sub': 'CodeDAC는 일상을 더 편하게 만드는 <br class="br-pc" />스마트폰 유틸리티 앱을 만듭니다.',
    'hero.cta1': '앱 둘러보기',
    'hero.cta2': '문의하기',

    'about.title': '회사 소개',
    'about.meaning': 'Code 기반의 <b>D</b>evelopment <b>A</b>nd <b>C</b>onsulting',
    'about.lead': 'CodeDAC는 이름 그대로 코드(Code)를 기반으로 개발(Development)과 컨설팅(Consulting)을 제공하는 것을 지향하는 개발사입니다. 지금은 매일 손이 가는 스마트폰 유틸리티 앱을 직접 만들어 선보이고 있으며, 앞으로 탄탄한 기술력으로 고객의 문제를 함께 풀어가는 파트너로 성장하고자 합니다.',
    'about.c1.t': '단순함',
    'about.c1.d': '복잡한 기능보다, 한눈에 이해되고 바로 쓰는 편리함을 우선합니다.',
    'about.c2.t': '신뢰',
    'about.c2.d': '불필요한 권한과 광고를 줄이고, 사용자 데이터를 존중합니다.',
    'about.c3.t': '꾸준함',
    'about.c3.d': '출시로 끝내지 않고, 사용자 피드백을 반영해 계속 개선합니다.',

    'services.title': '서비스',
    'services.lead': '아이디어 구상부터 개발과 운영까지, CodeDAC가 기술 파트너로 함께합니다.',
    'services.s1.t': '앱 개발',
    'services.s1.d': 'Android·iOS 및 크로스플랫폼 앱을 기획부터 출시·운영까지 개발합니다.',
    'services.s2.t': '웹 개발',
    'services.s2.d': '반응형 웹사이트, 웹 애플리케이션, 관리자 시스템을 구축합니다.',
    'services.s3.t': '기술 컨설팅',
    'services.s3.d': '아키텍처 설계, 기술 스택 선정, 코드 리뷰 등 기술 의사결정을 함께합니다.',
    'services.s4.t': '유지보수 · 운영',
    'services.s4.d': '안정적인 운영, 성능 개선, 배포 자동화(CI/CD)로 서비스를 지속 관리합니다.',
    'services.tech': '기술 스택',
    'services.cta': '프로젝트 문의하기',

    'apps.title': '앱 소개',
    'apps.lead': 'CodeDAC가 만들어 배포 중인 스마트폰 유틸리티 앱입니다. 스크린샷을 누르면 크게 볼 수 있습니다.',

    'footer.privacy': '개인정보처리방침',
  },
  en: {
    'meta.title': 'CodeDAC | Smartphone Utility Apps',
    'meta.desc': 'CodeDAC builds and publishes 13 smartphone utility apps including Clipboard+, AutoStart+ and FloatCalc+.',

    'nav.about': 'About',
    'nav.services': 'Services',
    'nav.apps': 'Apps',

    'hero.eyebrow': 'SMARTPHONE UTILITY APPS',
    'hero.title': 'Make your phone<br />smarter',
    'hero.sub': 'CodeDAC builds smartphone utility apps <br class="br-pc" />that make everyday life easier.',
    'hero.cta1': 'Explore apps',
    'hero.cta2': 'Contact us',

    'about.title': 'About Us',
    'about.meaning': 'Code-based <b>D</b>evelopment <b>A</b>nd <b>C</b>onsulting',
    'about.lead': 'True to its name, CodeDAC is built on Code to deliver Development And Consulting. Today we design and publish smartphone utility apps people reach for every day, and we aim to grow into a trusted technology partner that solves our clients’ challenges with solid engineering.',
    'about.c1.t': 'Simplicity',
    'about.c1.d': 'We favor clarity and instant usability over complex features.',
    'about.c2.t': 'Trust',
    'about.c2.d': 'We minimize unnecessary permissions and ads, and respect your data.',
    'about.c3.t': 'Consistency',
    'about.c3.d': 'Launch is just the start — we keep improving with user feedback.',

    'services.title': 'Services',
    'services.lead': 'From idea to development and operations, CodeDAC partners with you across the whole journey.',
    'services.s1.t': 'App Development',
    'services.s1.d': 'We build Android, iOS and cross-platform apps from planning to launch and operation.',
    'services.s2.t': 'Web Development',
    'services.s2.d': 'We build responsive websites, web applications and admin systems.',
    'services.s3.t': 'Technical Consulting',
    'services.s3.d': 'We advise on architecture, tech-stack selection and code review to guide key decisions.',
    'services.s4.t': 'Maintenance & Ops',
    'services.s4.d': 'We keep services healthy with stable operations, performance tuning and CI/CD automation.',
    'services.tech': 'Tech Stack',
    'services.cta': 'Start a project',

    'apps.title': 'Our Apps',
    'apps.lead': 'Smartphone utility apps built and published by CodeDAC. Tap a screenshot to view it larger.',

    'footer.privacy': 'Privacy Policy',
  },
};

// 자산 캐시 버전 (아이콘/스크린샷을 바꾸면 숫자를 올리세요. index.html의 ?v= 와 맞춤)
const V = '13';

// ===== 앱 목록 데이터 =====
// shots: images/shots/<slug>-1.jpg 형식으로 존재하는 스크린샷 개수
// store: 실제 Google Play 주소를 넣으면 카드에 스토어 버튼이 표시됩니다. (없으면 '' 로 두세요)
const APPS = [
  { slug: 'clipboard', name: 'Clipboard+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.clipboard',
    tag: { ko: '클립보드', en: 'Clipboard' },
    desc: { ko: '복사한 내용을 자동 저장해 어디서든 다시 붙여넣는 클립보드 관리자.', en: 'Auto-saves your clipboard history to paste anywhere, anytime.' } },
  { slug: 'autostart', name: 'AutoStart+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.autostart',
    tag: { ko: '자동 실행', en: 'Auto Start' },
    desc: { ko: '부팅 시 원하는 앱을 자동으로 실행. 루트 불필요, 한 번 설정으로 끝.', en: 'Auto-launch your apps on boot. No root required, set once.' } },
  { slug: 'floatcalc', name: 'FloatCalc+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.floatcalc',
    tag: { ko: '플로팅 도구', en: 'Floating' },
    desc: { ko: '앱을 벗어나지 않고 계산하는 플로팅 계산기·환율·단위 변환기.', en: 'A floating calculator, FX & unit converter on top of any app.' } },
  { slug: 'floatcrypto', name: 'FloatCrypto+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.floatcrypto',
    tag: { ko: '플로팅 도구', en: 'Floating' },
    desc: { ko: '비트코인·이더리움 실시간 시세를 화면 위에 띄우는 오버레이.', en: 'Live Bitcoin & crypto prices floating over any app.' } },
  { slug: 'floattimer', name: 'FloatTimer+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.floattimer',
    tag: { ko: '플로팅 도구', en: 'Floating' },
    desc: { ko: '인터벌·뽀모도로·멀티 타이머를 화면 위에 띄우는 플로팅 타이머.', en: 'A floating interval, Pomodoro & multi-timer over any app.' } },
  { slug: 'volumebooster', name: 'VolumeBooster+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.volumebooster',
    tag: { ko: '오디오', en: 'Audio' },
    desc: { ko: '볼륨 부스터·이퀄라이저·베이스 부스터를 진짜 dB로 정확하게.', en: 'Volume booster, equalizer & bass boost with real, measured dB.' } },
  { slug: 'photocleaner', name: 'PhotoCleaner+', shots: 3, store: '',
    tag: { ko: '개인정보', en: 'Privacy' },
    desc: { ko: '사진·PDF 속 개인정보를 단색으로 가려 안전하게. 완전 오프라인.', en: 'Hide personal info in photos & PDFs, fully on-device.' } },
  { slug: 'secretalbum', name: 'SecretAlbum+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.secretalbum',
    tag: { ko: '개인정보', en: 'Privacy' },
    desc: { ko: 'AES-256 암호화와 PIN 잠금으로 사진·동영상을 숨기는 비밀 금고.', en: 'Hide photos & videos with AES-256 encryption and a PIN lock.' } },
  { slug: 'readfocus', name: 'ReadFocus+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.readfocus',
    tag: { ko: '접근성', en: 'Accessibility' },
    desc: { ko: '난독증·ADHD 읽기 보조. 줄 강조·마스크로 읽는 줄에 시선 고정.', en: 'A dyslexia & ADHD reading aid with line highlight & mask.' } },
  { slug: 'colorcards', name: 'Color Cards+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.colorcards',
    tag: { ko: '유아 교육', en: 'Kids' },
    desc: { ko: '보고 듣고 따라 말하며 색깔을 배우는 유아용 플래시카드.', en: 'Talking color flashcards that help toddlers learn colors.' } },
  { slug: 'wordcards', name: 'Word Cards+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.wordcards',
    tag: { ko: '유아 교육', en: 'Kids' },
    desc: { ko: '유아가 단어를 말하고 들으며 배우는 플래시카드.', en: 'Flashcards for toddlers to speak and listen to words.' } },
  { slug: 'sleepbaby', name: 'SleepBaby+', shots: 3, store: 'https://play.google.com/store/apps/details?id=com.codedac.whitenoise',
    tag: { ko: '육아', en: 'Family' },
    desc: { ko: '아기의 잠을 돕는 자장가와 백색소음.', en: 'Soothing lullabies and white noise to help your baby sleep.' } },
  { slug: 'clipboardwin', name: 'Clipboard+ for Windows', shots: 0, store: '',
    tag: { ko: 'Windows 앱', en: 'Windows App' },
    desc: { ko: 'Clipboard+ 안드로이드 앱과 동기화되는 Windows 트레이 클립보드 관리자.', en: 'A Windows tray clipboard manager that syncs with the Clipboard+ Android app.' } },
];

// ===== 앱 카드 렌더링 =====
const appGrid = document.getElementById('appGrid');

function renderApps(lang) {
  appGrid.innerHTML = APPS.map((app) => {
    const shots = [];
    for (let i = 1; i <= app.shots; i++) {
      shots.push(
        `<img src="images/shots/${app.slug}-${i}.jpg?v=${V}" alt="${app.name} screenshot ${i}" loading="lazy" class="shot" data-app="${app.slug}" data-idx="${i - 1}" />`
      );
    }
    const shotsHtml = app.shots
      ? `<div class="app-shots">${shots.join('')}</div>`
      : '';
    const storeHtml = app.store
      ? `<a class="app-link" href="${app.store}" target="_blank" rel="noopener">${lang === 'ko' ? 'Google Play에서 보기 →' : 'View on Google Play →'}</a>`
      : '';
    return `
      <article class="app-card">
        <div class="app-head">
          <img class="app-icon" src="images/icons/${app.slug}.png?v=${V}" alt="${app.name} icon" loading="lazy" />
          <div class="app-meta">
            <h3>${app.name}</h3>
            <span class="app-tag">${app.tag[lang]}</span>
          </div>
        </div>
        <p class="app-desc">${app.desc[lang]}</p>
        ${shotsHtml}
        ${storeHtml}
      </article>`;
  }).join('');
}

// ===== 스크린샷 라이트박스 =====
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lbImg');
let lbList = [];
let lbIndex = 0;

function openLightbox(slug, idx) {
  const app = APPS.find((a) => a.slug === slug);
  if (!app) return;
  lbList = [];
  for (let i = 1; i <= app.shots; i++) lbList.push(`images/shots/${slug}-${i}.jpg?v=${V}`);
  lbIndex = idx;
  showLbImage();
  lightbox.classList.add('open');
  lightbox.setAttribute('aria-hidden', 'false');
}
function showLbImage() { lbImg.src = lbList[lbIndex]; }
function closeLightbox() {
  lightbox.classList.remove('open');
  lightbox.setAttribute('aria-hidden', 'true');
  lbImg.src = '';
}
function lbStep(d) { lbIndex = (lbIndex + d + lbList.length) % lbList.length; showLbImage(); }

appGrid.addEventListener('click', (e) => {
  const img = e.target.closest('.shot');
  if (img) openLightbox(img.dataset.app, Number(img.dataset.idx));
});
document.getElementById('lbClose').addEventListener('click', closeLightbox);
document.getElementById('lbPrev').addEventListener('click', (e) => { e.stopPropagation(); lbStep(-1); });
document.getElementById('lbNext').addEventListener('click', (e) => { e.stopPropagation(); lbStep(1); });
lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
document.addEventListener('keydown', (e) => {
  if (!lightbox.classList.contains('open')) return;
  if (e.key === 'Escape') closeLightbox();
  else if (e.key === 'ArrowLeft') lbStep(-1);
  else if (e.key === 'ArrowRight') lbStep(1);
});

// ===== 언어 결정 =====
// 우선순위: 사용자가 직접 고른 값(localStorage) > 접속 지역 자동 감지
// 자동 감지: 브라우저 언어가 한국어이거나 시간대가 서울이면 한국어, 그 외에는 영어
function detectLang() {
  const saved = localStorage.getItem('lang');
  if (saved === 'ko' || saved === 'en') return saved;

  const langs = navigator.languages || [navigator.language || ''];
  if (langs.some((l) => (l || '').toLowerCase().startsWith('ko'))) return 'ko';

  try {
    if (Intl.DateTimeFormat().resolvedOptions().timeZone === 'Asia/Seoul') return 'ko';
  } catch (e) { /* 무시 */ }

  return 'en'; // 외국 접속 기본값: 영어
}

let currentLang = detectLang();

function applyLang(lang, persist) {
  const dict = I18N[lang] || I18N.ko;
  currentLang = lang;
  document.documentElement.lang = lang;

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    const text = dict[key];
    if (text === undefined) return;
    const attr = el.getAttribute('data-i18n-attr');
    if (attr) el.setAttribute(attr, text);
    else el.innerHTML = text; // <br> 등 허용 (정적 사전이라 안전)
  });

  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('is-active', btn.dataset.lang === lang);
  });

  renderApps(lang); // 앱 카드도 언어에 맞게 다시 그리기
  if (persist) localStorage.setItem('lang', lang); // 사용자가 직접 고른 경우만 기억
}

document.querySelectorAll('.lang-btn').forEach((btn) => {
  btn.addEventListener('click', () => applyLang(btn.dataset.lang, true));
});
applyLang(currentLang, false); // 초기 로드: 자동 감지값(저장 안 함)

// ===== 현재 연도 =====
document.getElementById('year').textContent = new Date().getFullYear();

// ===== 모바일 메뉴 =====
const navToggle = document.getElementById('navToggle');
const nav = document.getElementById('nav');
navToggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});
nav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => nav.classList.remove('open'));
});
