def dismiss_banner(page):
    try:
        dlg = page.locator('div[role="dialog"][aria-label*="Privacy"]').first
        if dlg.count() == 0 or not dlg.is_visible():
            return
        print("[Info] GDPR banner visible, dismissing...")

        page.evaluate("""
            () => {
                const b = document.querySelector("#onetrust-accept-btn-handler");
                if (b) b.click();
            }
        """)
        page.wait_for_timeout(800)

    except Exception as e:
        print(f"[Warning] GDPR banner dismissal failed: {e}")
