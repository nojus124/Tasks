from .gdpr import dismiss_banner

def deselect_all(page):
    while True:
        tags = page.locator("span.selected svg")
        if tags.count() == 0:
            break
        tags.first.scroll_into_view_if_needed()
        tags.first.click()
        page.wait_for_timeout(250)

def select_columns(page):
    SELECTED_METRICS = [
        "24h %",
        "Market Cap"
    ]
    print(f"[Info] Selecting columns: {SELECTED_METRICS}")

    page.locator('button:has-text("Columns")').click()
    page.locator('text=Choose up to').wait_for(timeout=5000)
    dismiss_banner(page)
    deselect_all(page)

    for metric in SELECTED_METRICS:
        locator = page.locator(
            f'xpath=//span[normalize-space()="{metric}" and not(contains(@class,"selected"))]'
        )
        try:
            locator.wait_for(state="visible", timeout=5000)
            locator.scroll_into_view_if_needed()
            locator.click()
            print(f"[Info] Selected: {metric}")
            page.wait_for_timeout(150)
        except Exception as e:
            print(f"[Warning] Could NOT select metric '{metric}': {e}")

    try:
        page.locator('button:has-text("Apply Changes")').click()
        page.wait_for_timeout(2000)
    except Exception as e:
        print(f"[Fatal] Could not click 'Apply Changes': {e}")
