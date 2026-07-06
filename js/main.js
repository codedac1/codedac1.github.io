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
    'nav.apps': '앱 소개',
    'nav.contact': '문의',

    'hero.eyebrow': 'SMARTPHONE UTILITY APPS',
    'hero.title': '스마트폰을<br />더 스마트하게',
    'hero.sub': 'CodeDAC는 일상을 더 편하게 만드는<br class="br-pc" />스마트폰 유틸리티 앱을 만듭니다.',
    'hero.cta1': '앱 둘러보기',
    'hero.cta2': '문의하기',

    'about.title': '회사 소개',
    'about.lead': 'CodeDAC는 스마트폰을 더 편리하게 쓰도록 돕는 유틸리티 앱을 만들고 배포하는 개발사입니다. 작지만 매일 쓰게 되는, 꼭 필요한 도구를 지향합니다.',
    'about.c1.t': '단순함',
    'about.c1.d': '복잡한 기능보다, 한눈에 이해되고 바로 쓰는 편리함을 우선합니다.',
    'about.c2.t': '신뢰',
    'about.c2.d': '불필요한 권한과 광고를 줄이고, 사용자 데이터를 존중합니다.',
    'about.c3.t': '꾸준함',
    'about.c3.d': '출시로 끝내지 않고, 사용자 피드백을 반영해 계속 개선합니다.',

    'apps.title': '앱 소개',
    'apps.lead': 'CodeDAC가 만들어 배포 중인 스마트폰 유틸리티 앱입니다. 스크린샷을 누르면 크게 볼 수 있습니다.',

    'contact.title': '문의 · 연락처',
    'contact.lead': '앱에 대한 의견, 버그 제보, 협업 제안을 남겨 주세요. 확인 후 빠르게 답변드리겠습니다.',
    'contact.email': '이메일',
    'contact.hours': '응답 시간',
    'contact.hours.v': '평일 1–2일 이내',

    'form.name': '이름',
    'form.name.ph': '홍길동',
    'form.email': '이메일',
    'form.msg': '문의 내용',
    'form.msg.ph': '문의하실 내용을 입력해 주세요.',
    'form.submit': '문의 보내기',
    'form.note': '* 전송 버튼을 누르면 메일 앱이 열립니다.',

    'mail.subject': '[홈페이지 문의] ',
    'mail.name': '이름',
    'mail.email': '이메일',
  },
  en: {
    'meta.title': 'CodeDAC | Smartphone Utility Apps',
    'meta.desc': 'CodeDAC builds and publishes 13 smartphone utility apps including Clipboard+, AutoStart+ and FloatCalc+.',

    'nav.about': 'About',
    'nav.apps': 'Apps',
    'nav.contact': 'Contact',

    'hero.eyebrow': 'SMARTPHONE UTILITY APPS',
    'hero.title': 'Make your phone<br />smarter',
    'hero.sub': 'CodeDAC builds smartphone utility apps<br class="br-pc" />that make everyday life easier.',
    'hero.cta1': 'Explore apps',
    'hero.cta2': 'Contact us',

    'about.title': 'About Us',
    'about.lead': 'CodeDAC is a studio that builds and publishes utility apps that make smartphones more convenient. We aim for small, essential tools you reach for every day.',
    'about.c1.t': 'Simplicity',
    'about.c1.d': 'We favor clarity and instant usability over complex features.',
    'about.c2.t': 'Trust',
    'about.c2.d': 'We minimize unnecessary permissions and ads, and respect your data.',
    'about.c3.t': 'Consistency',
    'about.c3.d': 'Launch is just the start — we keep improving with user feedback.',

    'apps.title': 'Our Apps',
    'apps.lead': 'Smartphone utility apps built and published by CodeDAC. Tap a screenshot to view it larger.',

    'contact.title': 'Contact',
    'contact.lead': 'Share feedback, report a bug, or propose a collaboration. We’ll get back to you soon.',
    'contact.email': 'Email',
    'contact.hours': 'Response',
    'contact.hours.v': 'Within 1–2 business days',

    'form.name': 'Name',
    'form.name.ph': 'John Doe',
    'form.email': 'Email',
    'form.msg': 'Message',
    'form.msg.ph': 'Please enter your message.',
    'form.submit': 'Send message',
    'form.note': '* Pressing send will open your mail app.',

    'mail.subject': '[Website inquiry] ',
    'mail.name': 'Name',
    'mail.email': 'Email',
  },
};

// 자산 캐시 버전 (아이콘/스크린샷을 바꾸면 숫자를 올리세요. index.html의 ?v= 와 맞춤)
const V = '7';

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

// ===== 언어 적용 =====
let currentLang = localStorage.getItem('lang') || 'ko';

function applyLang(lang) {
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
  localStorage.setItem('lang', lang);
}

document.querySelectorAll('.lang-btn').forEach((btn) => {
  btn.addEventListener('click', () => applyLang(btn.dataset.lang));
});
applyLang(currentLang);

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

// ===== 문의 폼 (mailto) =====
// ▼ 받는 이메일 주소를 수정하세요 ▼
const CONTACT_EMAIL = 'codedac1@gmail.com';

const form = document.getElementById('contactForm');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const dict = I18N[currentLang];
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const message = document.getElementById('message').value.trim();
  const subject = encodeURIComponent(dict['mail.subject'] + name);
  const body = encodeURIComponent(
    `${dict['mail.name']}: ${name}\n${dict['mail.email']}: ${email}\n\n${message}`
  );
  window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
});
