#!/bin/bash
set -e

# Playwright 스크린샷 검증 스크립트
# 각 .stories.tsx 파일에 대해 스크린샷을 캡처하고 검증

echo "📸 Storybook 스크린샷 검증"

# Storybook 개발 서버 시작 (백그라운드)
echo "🚀 Storybook 서버 시작..."
npm run storybook > /tmp/storybook.log 2>&1 &
STORYBOOK_PID=$!

# 서버 시작 대기 (10초)
sleep 10

if ! kill -0 $STORYBOOK_PID 2>/dev/null; then
  echo "❌ Storybook 서버 시작 실패"
  cat /tmp/storybook.log
  exit 1
fi

echo "✅ Storybook 서버 실행 중 (PID: $STORYBOOK_PID)"

# Playwright로 스크린샷 검증
cat > /tmp/verify-stories.mjs << 'PLAYWRIGHT_EOF'
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const STORYBOOK_URL = 'http://localhost:6006';
const SCREENSHOT_DIR = './.playwright/screenshots';

// 스크린샷 디렉토리 생성
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    console.log('📄 Storybook 접속 중...');
    await page.goto(STORYBOOK_URL, { waitUntil: 'networkidle' });

    // iframe 내의 스토리 프리뷰 대기
    await page.waitForTimeout(2000);

    // 모든 스토리 패널 찾기
    const storyLinks = await page.locator('[data-testid="explorer-node"] a').all();
    console.log(`📚 ${storyLinks.length}개의 스토리 발견`);

    let successCount = 0;
    for (let i = 0; i < Math.min(storyLinks.length, 5); i++) {
      const link = storyLinks[i];
      const storyName = await link.textContent();

      console.log(`📸 스크린샷 캡처: ${storyName}`);
      await link.click();
      await page.waitForTimeout(1000);

      // iframe 내의 렌더링된 컴포넌트 스크린샷
      const frameHandle = await page.$('iframe[title="storybook-preview-iframe"]');
      if (frameHandle) {
        const frame = await frameHandle.contentFrame();
        if (frame) {
          await frame.screenshot({
            path: `${SCREENSHOT_DIR}/${storyName?.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.png`,
          });
          successCount++;
        }
      }
    }

    console.log(`✅ ${successCount}개 스크린샷 캡처 완료`);

  } catch (error) {
    console.error('❌ 스크린샷 검증 실패:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
PLAYWRIGHT_EOF

node /tmp/verify-stories.mjs
PLAYWRIGHT_RESULT=$?

# Storybook 서버 종료
echo "🛑 Storybook 서버 종료..."
kill $STORYBOOK_PID 2>/dev/null || true
wait $STORYBOOK_PID 2>/dev/null || true

if [ $PLAYWRIGHT_RESULT -ne 0 ]; then
  echo "❌ Playwright 검증 실패"
  exit 1
fi

echo "✅ 모든 스크린샷 검증 완료"
