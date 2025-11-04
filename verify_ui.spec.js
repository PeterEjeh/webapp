const { test, expect } = require('@playwright/test');

test('verify UI', async ({ page }) => {
  await page.goto('http://127.0.0.1:8080/users/login/');
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await page.waitForURL('http://127.0.0.1:8080/');
  await page.screenshot({ path: 'verify_ui.png' });
});
