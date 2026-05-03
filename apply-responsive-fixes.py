"""
Adds responsive fixes to all PourOver HTML files.
Run: python3 apply-responsive-fixes.py  (from the project folder)

The script inserts a <link rel="stylesheet"> tag pointing to
responsive.css  **right before </head>**  in each HTML file.
It also fixes the inline nav <a> tags to be pill-shaped without
overriding color logic.
"""

import os
import re

HTML_FILES = [
    "index.html",
    "filter.html",
    "moka.html",
    "chemex.html",
    "aeropress.html",
    "french-press.html",
]

LINK_TAG = '<link rel="stylesheet" href="responsive.css">\n'


def patch_file(path):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject link tag before </head> (idempotent)
    if 'href="responsive.css"' not in html:
        html = html.replace("</head>", LINK_TAG + "</head>", 1)
        print(f"  + injected <link> in {path}")
    else:
        print(f"  = already patched {path}")

    # 2. Make sure the nav element has overflow-x:auto inline style
    #    (belt-and-suspenders for environments without the linked CSS)
    nav_pattern = re.compile(
        r'(<nav\s+style=")([^"]*?)(")',
        re.DOTALL,
    )

    def upgrade_nav_style(m):
        existing = m.group(2)
        additions = []
        if "overflow-x" not in existing:
            additions.append("overflow-x:auto")
        if "white-space" not in existing:
            additions.append("white-space:nowrap")
        if "-webkit-overflow-scrolling" not in existing:
            additions.append("-webkit-overflow-scrolling:touch")
        if additions:
            new_style = existing.rstrip(";") + ";" + ";".join(additions) + ";"
            return m.group(1) + new_style + m.group(3)
        return m.group(0)

    html_new = nav_pattern.sub(upgrade_nav_style, html)
    if html_new != html:
        html = html_new
        print(f"  + nav inline style updated in {path}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    print("Applying responsive fixes…\n")
    for fn in HTML_FILES:
        patch_file(fn)
    print("\nDone. Place responsive.css in the same folder as your HTML files.")
