/*
 * Detox end-to-end test covering core reading flow.
 */

describe('Reading flow', () => {
  it('opens a chapter', async () => {
    await device.launchApp();
    await expect(element(by.text('Start Reading'))).toBeVisible();
    await element(by.text('Start Reading')).tap();
    await expect(element(by.id('chapter-view'))).toBeVisible();
  });
});
