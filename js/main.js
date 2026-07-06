// ===== 다국어(i18n) 사전 =====
// 텍스트를 수정할 때는 ko / en 두 쪽을 함께 바꿔 주세요.
const I18N = {
  ko: {
    'meta.title': 'CodeDAC | 스마트폰 유틸리티 앱',
    'meta.desc': 'CodeDAC는 Clipboard+, AutoStart+ 등 편리한 스마트폰 유틸리티 앱을 만들고 배포합니다.',

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
    'apps.lead': 'CodeDAC가 만들어 배포 중인 스마트폰 유틸리티 앱입니다.',
    'apps.clip.tag': '클립보드 관리',
    'apps.clip.desc': '복사한 내용을 자동으로 기록해 두고, 언제든 다시 꺼내 붙여넣을 수 있는 스마트 클립보드 앱입니다.',
    'apps.auto.tag': '자동 실행',
    'apps.auto.desc': '스마트폰을 켤 때 원하는 앱을 자동으로 실행해 주는 앱입니다. 매번 직접 여는 번거로움을 줄여 줍니다.',
    'apps.store': 'Google Play에서 보기 →',
    'apps.more': '그 외에도 다양한 유틸리티 앱을 준비하고 있습니다.',

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
    'meta.desc': 'CodeDAC builds and publishes handy smartphone utility apps such as Clipboard+ and AutoStart+.',

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
    'apps.lead': 'Smartphone utility apps built and published by CodeDAC.',
    'apps.clip.tag': 'Clipboard manager',
    'apps.clip.desc': 'A smart clipboard app that automatically saves what you copy so you can paste it back anytime.',
    'apps.auto.tag': 'Auto launcher',
    'apps.auto.desc': 'Automatically launches your favorite apps when your phone starts, so you don’t have to open them yourself.',
    'apps.store': 'View on Google Play →',
    'apps.more': 'More utility apps are on the way.',

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
    if (attr) {
      el.setAttribute(attr, text);
    } else {
      el.innerHTML = text; // <br> 등 허용 (정적 사전이라 안전)
    }
  });

  // 언어 버튼 활성화 상태
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('is-active', btn.dataset.lang === lang);
  });

  localStorage.setItem('lang', lang);
}

// 언어 토글 버튼
document.querySelectorAll('.lang-btn').forEach((btn) => {
  btn.addEventListener('click', () => applyLang(btn.dataset.lang));
});

// 초기 언어 적용
applyLang(currentLang);

// 현재 연도 표시
document.getElementById('year').textContent = new Date().getFullYear();

// 모바일 메뉴 토글
const navToggle = document.getElementById('navToggle');
const nav = document.getElementById('nav');
navToggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});
nav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => nav.classList.remove('open'));
});

// 문의 폼: 별도 서버 없이 메일 앱으로 전송 (mailto)
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
