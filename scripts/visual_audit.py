#!/usr/bin/env python3
"""visual_audit.py — measure the dashboard's responsiveness, don't guess it.

Loads the generated index.html at four widths (small phone, standard
phone, desktop, large desktop) and fails if the document carries
horizontal overflow beyond 1px. Reports the widest unclipped element
when there is one, so the fix starts with a name.

Optional dependency: playwright + chromium (skips with exit 0 and a
note when unavailable — this is a human instrument, not a CI gate;
the machine contract is tests/test_responsive.py).

Usage: python scripts/visual_audit.py [--shots DIR]
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HTML = REPO / "index.html"

VIEWPORTS = [
    ("phone-sm", 360, 800),
    ("phone", 390, 844),
    ("desktop", 1440, 900),
    ("desktop-lg", 1920, 1080),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright unavailable — visual audit skipped (optional tooling)")
        return 0

    shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(f"file://{HTML}")
            page.wait_for_timeout(900)
            if shots:
                shots.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(shots / f"{name}.png"))
            m = page.evaluate("""() => {
                  const vw = document.documentElement.clientWidth;
                  let worst = null;
                  document.querySelectorAll('body *').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if ((!worst || r.right > worst.right) && r.right > vw + 1) {
                      let clipped = false, a = el.parentElement;
                      while (a && a !== document.body) {
                        const o = getComputedStyle(a).overflowX;
                        if (o === 'auto' || o === 'scroll' || o === 'hidden') {
                          clipped = true; break;
                        }
                        a = a.parentElement;
                      }
                      if (!clipped) {
                        worst = {right: r.right,
                                 name: el.tagName + '.' +
                                   (el.className || '').toString().slice(0, 40)};
                      }
                    }
                  });
                  return {vw, scrollW: document.documentElement.scrollWidth, worst};
                }""")
            overflow = m["scrollW"] - m["vw"]
            status = "OK" if overflow <= 1 else "OVERFLOW"
            line = f"{name}: vw={m['vw']} scrollW={m['scrollW']} overflow={overflow}px {status}"
            if m["worst"]:
                w = m["worst"]
                line += f" | widest unclipped: {w['name']} (right={round(w['right'])})"
            print(line)
            if overflow > 1:
                failures.append(name)
            page.close()
        browser.close()

    if failures:
        print(f"FAIL: horizontal overflow at {', '.join(failures)}")
        return 1
    print("PASS: no horizontal overflow at any audited width")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
