import argparse
from crawler.html_scraper  import CoinMarketCapHTMLScraper
from crawler.json_scraper  import CoinMarketCapJSONScraper   # ← NEW

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["html", "json"], default="html")
    parser.add_argument("--out", default="data/cmc.csv")
    parser.add_argument("--pages", type=int, default=5)
    parser.add_argument("--rows",  type=int, default=100)
    args = parser.parse_args()

    if args.mode == "html":
        scraper = CoinMarketCapHTMLScraper()
    else:
        scraper = CoinMarketCapJSONScraper()

    rows = scraper.scrape_all(pages=args.pages, row_limit=args.rows)
    scraper.to_csv(rows, path=args.out)
    print(f"[Done] wrote {len(rows)} rows → {args.out}")

if __name__ == "__main__":
    run()
