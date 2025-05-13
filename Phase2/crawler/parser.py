def parse_row(row, index):
    """
    Parses a single <tr> row from the CoinMarketCap HTML table
    and returns a list of string values in fixed column order:
    Rank, Name, Symbol, Price (USD), 24h % Change, Market Cap (USD)
    """
    def safe_text(locator, fallback="-"):
        try:
            txt = locator.inner_text(timeout=2000).strip()
            return txt if txt and txt != "?" else fallback
        except Exception:
            return fallback

    def clean(txt):
        return txt.replace("$", "").replace(",", "").strip()

    try:
        # Fixed column layout:
        rank   = safe_text(row.locator("td:nth-child(2)"))
        name   = safe_text(row.locator("td:nth-child(3) p").nth(0))
        symbol = safe_text(row.locator("td:nth-child(3) p").nth(1))
        price  = clean(safe_text(row.locator("td:nth-child(4)")))

        change_cell = row.locator("td:nth-child(5)")
        raw_change = safe_text(change_cell).replace("%", "")
        is_neg = change_cell.locator(".icon-Caret-down").count() > 0
        if is_neg and raw_change and not raw_change.startswith("-"):
            raw_change = "-" + raw_change

        market_cap = clean(safe_text(row.locator("td:nth-child(6)")))

        return [rank, name, symbol, price, raw_change or "-", market_cap]

    except Exception as e:
        print(f"[Fatal] Failed to parse row {index + 1}: {e}")
        try:
            print("[Debug] Row HTML:\n", row.inner_html())
        except Exception:
            print("[Debug] Could not extract row HTML.")
        raise