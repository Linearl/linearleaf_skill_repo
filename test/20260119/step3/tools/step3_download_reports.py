import pathlib
import sys

from step3_cninfo_reports_and_notes import (
    STOCKS,
    download_pdf,
    get_session,
    query_latest_reports,
    REPORTS_DIR,
)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    session = get_session()

    failures: list[str] = []

    selected_codes = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        selected_codes = {c.strip() for c in sys.argv[1].split(",") if c.strip()}

    for stock in STOCKS:
        if selected_codes is not None and stock.code not in selected_codes:
            continue
        print(f"==> {stock.track} {stock.code} {stock.name}")
        stock_dir = REPORTS_DIR / f"{stock.code}_{stock.name}"
        picked = query_latest_reports(session, stock)
        if not picked:
            failures.append(f"{stock.code} {stock.name}: no announcements")
            continue
        for kind, ann in picked.items():
            try:
                download_pdf(session, stock, ann, stock_dir)
            except Exception as e:
                failures.append(f"{stock.code} {stock.name} {kind}: {e}")

    if failures:
        tools_dir = pathlib.Path(__file__).resolve().parents[1] / "tools"
        tools_dir.mkdir(parents=True, exist_ok=True)
        (tools_dir / "step3_download_failures.json").write_text(
            "[\n" + ",\n".join([f"  {repr(f)}" for f in failures]) + "\n]",
            encoding="utf-8",
        )
        print("\nSome failures occurred; see tools/step3_download_failures.json")

    print("\nDone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
