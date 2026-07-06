// Puppeteer로 로컬 페이지를 열어 콘솔 오류 / 깨진 이미지 / 카드 수를 확인한다.
const puppeteer = require('C:/CodeDAC/Clipboard/node_modules/puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
  page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message));
  page.on('requestfailed', (r) => errors.push('REQFAIL: ' + r.url() + ' — ' + r.failure().errorText));

  const url = 'file://' + path.resolve('C:/CodeDAC/codedac/index.html').replace(/\\/g, '/');
  await page.goto(url, { waitUntil: 'networkidle0' });

  const cardCount = await page.$$eval('.app-card', (els) => els.length);
  const shotCount = await page.$$eval('.app-shots .shot', (els) => els.length);
  const brokenImgs = await page.$$eval('img', (imgs) =>
    imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.getAttribute('src'))
  );

  // 스크린샷 저장 (전체 페이지)
  await page.screenshot({ path: 'C:/CodeDAC/codedac/scripts/_preview_ko.png', fullPage: true });

  // 영문 전환 후 첫 카드 텍스트 확인
  await page.click('.lang-btn[data-lang="en"]');
  await new Promise((r) => setTimeout(r, 300));
  const firstCardEn = await page.$eval('.app-card h3', (el) => el.textContent);
  const navAboutEn = await page.$eval('a[data-i18n="nav.about"]', (el) => el.textContent);

  // 라이트박스 열기 테스트
  await page.click('.lang-btn[data-lang="ko"]');
  await new Promise((r) => setTimeout(r, 200));
  await page.click('.app-shots .shot');
  await new Promise((r) => setTimeout(r, 300));
  const lbOpen = await page.$eval('#lightbox', (el) => el.classList.contains('open'));

  console.log('app cards      :', cardCount);
  console.log('screenshots    :', shotCount);
  console.log('broken images  :', brokenImgs.length, brokenImgs.slice(0, 5));
  console.log('EN first card  :', firstCardEn);
  console.log('EN nav.about   :', navAboutEn);
  console.log('lightbox opens :', lbOpen);
  console.log('errors         :', errors.length);
  errors.slice(0, 10).forEach((e) => console.log('  -', e));

  await browser.close();
})();
