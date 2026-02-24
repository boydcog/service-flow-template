#!/bin/bash
set -e

# Playwright   
#  .stories.tsx     

echo " Storybook  "

# Storybook    ()
echo " Storybook  ..."
npm run storybook > /tmp/storybook.log 2>&1 &
STORYBOOK_PID=$!

#    (10)
sleep 10

if ! kill -0 $STORYBOOK_PID 2>/dev/null; then
  echo " Storybook   "
  cat /tmp/storybook.log
  exit 1
fi

echo " Storybook    (PID: $STORYBOOK_PID)"

# Playwright  
cat > /tmp/verify-stories.mjs << 'PLAYWRIGHT_EOF'
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const STORYBOOK_URL = 'http://localhost:6006';
const SCREENSHOT_DIR = './.playwright/screenshots';

//   
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    console.log(' Storybook  ...');
    await page.goto(STORYBOOK_URL, { waitUntil: 'networkidle' });

    // iframe    
    await page.waitForTimeout(2000);

    //    
    const storyLinks = await page.locator('[data-testid="explorer-node"] a').all();
    console.log(` ${storyLinks.length}  `);

    let successCount = 0;
    for (let i = 0; i < Math.min(storyLinks.length, 5); i++) {
      const link = storyLinks[i];
      const storyName = await link.textContent();

      console.log(`  : ${storyName}`);
      await link.click();
      await page.waitForTimeout(1000);

      // iframe    
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

    console.log(` ${successCount}   `);

  } catch (error) {
    console.error('   :', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
PLAYWRIGHT_EOF

node /tmp/verify-stories.mjs
PLAYWRIGHT_RESULT=$?

# Storybook  
echo " Storybook  ..."
kill $STORYBOOK_PID 2>/dev/null || true
wait $STORYBOOK_PID 2>/dev/null || true

if [ $PLAYWRIGHT_RESULT -ne 0 ]; then
  echo " Playwright  "
  exit 1
fi

echo "    "
