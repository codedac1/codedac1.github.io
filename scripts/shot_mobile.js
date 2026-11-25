// 모바일 화면 점검용 캡처(2026-11-25 ExamScan 페이지). 로컬 서버(py -m http.server 8000)를 띄운 뒤:
//   node scripts/shot_mobile.js <url> <out.png> [width=390] [--open-dialog]
// 기기 에뮬레이션(폭·DPR·터치·모바일 UA)으로 찍는다 — 헤드리스 Chrome 의 --window-size 는 최소 폭 때문에
// 390 으로 줄여도 실제 레이아웃 폭이 더 넓게 잡혀 오른쪽이 잘린 것처럼 보인다.
const puppeteer = require('puppeteer');
(async () => {
  const [url, out, w = '390'] = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  const openDialog = process.argv.includes('--open-dialog');
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.emulate({
    viewport: { width: Number(w), height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
    userAgent: 'Mozilla/5.0 (Linux; Android 14; SM-A346N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36',
  });
  await page.goto(url, { waitUntil: 'networkidle0' });
  const overflow = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const wide = [];
    document.querySelectorAll('body *').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 && r.width > 0 && getComputedStyle(el).position !== 'fixed' && !el.closest('.exs-shots, .app-shots, .lang-menu, dialog')) wide.push(`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} → ${Math.round(r.right)}`);
    });
    return { vw, scrollW: document.documentElement.scrollWidth, wide: wide.slice(0, 12) };
  });
  console.log(JSON.stringify(overflow));
  if (openDialog) {
    await page.click('[data-form="wf-org"]');
    await new Promise((r) => setTimeout(r, 400));
    await page.screenshot({ path: out });
  } else {
    await page.screenshot({ path: out, fullPage: true });
  }
  await browser.close();
})();
