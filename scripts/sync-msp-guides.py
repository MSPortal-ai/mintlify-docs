#!/usr/bin/env python3
"""Keep MSP Guides readers inside the MSP Guides tab.

Mintlify shows a page in the first tab that lists it. A user-guides page listed
in both Company Guides and MSP Guides therefore always opens in Company Guides,
even when the reader clicked it in MSP Guides. This script gives every shared
page its own MSP address:

- MSP Guides navigation entries for shared pages point to msp-guides/<path>.
- msp-guides/<path>.mdx is generated from user-guides/<path>.mdx, with links to
  other MSP pages rewritten to their msp-guides address.
- Pages that only MSP Guides lists (and hand-maintained msp-guides pages) get
  the same link rewrite in place.
- Generated copies no longer in MSP Guides navigation are deleted.

Edit user-guides only, then run `python3 scripts/sync-msp-guides.py`. Generated
copies carry a marker comment; an msp-guides page without it is hand-maintained
and never overwritten. `--check` changes nothing and exits 1 when a run would.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPANY_TAB = "Company Guides"
MSP_TAB = "MSP Guides"
SOURCE = "user-guides/"
COPY = "msp-guides/"
MARKER = "{/* Generated from /%s.mdx by scripts/sync-msp-guides.py. Edit the source page, then rerun the script. */}"
MARKER_RE = re.compile(r"^\{/\* Generated from /user-guides/.* by scripts/sync-msp-guides\.py\..*\*/\}\n", re.M)
# An absolute /user-guides/ link, not part of a longer path or external URL.
LINK_RE = re.compile(r"(?<![\w./-])/user-guides/([A-Za-z0-9_/-]+)")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)


def nav_pages(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for child in node:
            yield from nav_pages(child)
    elif isinstance(node, dict):
        for key in ("anchors", "groups", "pages"):
            yield from nav_pages(node.get(key, []))


def rewrite_nav(node, shared):
    """Point MSP navigation entries for shared pages at their msp-guides copy."""
    if isinstance(node, list):
        return [rewrite_nav(child, shared) for child in node]
    if isinstance(node, dict):
        return {k: rewrite_nav(v, shared) if k in ("anchors", "groups", "pages") else v
                for k, v in node.items()}
    if isinstance(node, str) and node in shared:
        return COPY + node[len(SOURCE):]
    return node


def rewrite_links(text, msp_copies):
    def swap(match):
        path = match[1].rstrip("/")
        return "/" + COPY + match[1] if COPY + path in msp_copies else match[0]
    return LINK_RE.sub(swap, text)


def generate(source_text, path, msp_copies):
    body = rewrite_links(source_text, msp_copies)
    marker = MARKER % (SOURCE + path) + "\n"
    frontmatter = FRONTMATTER_RE.match(body)
    if not frontmatter:
        return marker + "\n" + body
    rest = body[frontmatter.end():]
    return body[:frontmatter.end()] + "\n" + marker + rest


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report pending changes and exit 1 instead of writing")
    args = parser.parse_args()

    docs_path = ROOT / "docs.json"
    docs_text = docs_path.read_text()
    docs = json.loads(docs_text)
    tabs = {tab["tab"]: tab for tab in docs["navigation"]["tabs"]}
    company = set(nav_pages(tabs[COMPANY_TAB]))
    shared = {p for p in nav_pages(tabs[MSP_TAB]) if p.startswith(SOURCE) and p in company}

    msp_index = next(i for i, t in enumerate(docs["navigation"]["tabs"]) if t["tab"] == MSP_TAB)
    docs["navigation"]["tabs"][msp_index] = rewrite_nav(tabs[MSP_TAB], shared)
    msp = list(dict.fromkeys(nav_pages(docs["navigation"]["tabs"][msp_index])))

    def is_generated(page):
        target = ROOT / (page + ".mdx")
        return not target.is_file() or bool(MARKER_RE.search(target.read_text()))

    # Generated copies are for MSP readers, so their links go to every MSP version,
    # hand-maintained ones included. Hand-written pages only have links to generated
    # copies moved: the content matches, so the reader sees the same page while
    # staying in MSP Guides. A link from a hand-written page to a page with a
    # hand-maintained MSP version keeps the destination its author chose.
    msp_versions = {p for p in msp if p.startswith(COPY)}
    msp_copies = {p for p in msp_versions if is_generated(p)}

    writes, deletes, errors = {}, [], []
    new_docs = json.dumps(docs, indent=2, ensure_ascii=False) + "\n"
    if new_docs != docs_text:
        writes[docs_path] = new_docs

    generated = set()
    for page in msp:
        target = ROOT / (page + ".mdx")
        if page.startswith(COPY):
            current = target.read_text() if target.is_file() else None
            if current is not None and not MARKER_RE.search(current):
                expected = rewrite_links(current, msp_copies)  # hand-maintained
            else:
                path = page[len(COPY):]
                source = ROOT / (SOURCE + path + ".mdx")
                if not source.is_file():
                    errors.append(f"{page}: no msp-guides page and no source {source.relative_to(ROOT)}")
                    continue
                expected = generate(source.read_text(), path, msp_versions)
                generated.add(target)
        elif page.startswith(SOURCE) and page not in company and target.is_file():
            current = target.read_text()
            expected = rewrite_links(current, msp_copies)  # MSP-only page
        else:
            continue
        if current != expected:
            writes[target] = expected

    for existing in sorted((ROOT / COPY).rglob("*.mdx")):
        if existing not in generated and MARKER_RE.search(existing.read_text()):
            deletes.append(existing)

    for message in errors:
        print("error:", message, file=sys.stderr)
    changes = [f"update {p.relative_to(ROOT)}" for p in sorted(writes)] + \
              [f"delete {p.relative_to(ROOT)}" for p in deletes]
    if args.check:
        for line in changes:
            print(line)
        if changes:
            print(f"{len(changes)} change(s) pending: run python3 scripts/sync-msp-guides.py", file=sys.stderr)
        return 1 if changes or errors else 0

    for path, text in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    for path in deletes:
        path.unlink()
    print(f"{len(writes)} file(s) written, {len(deletes)} deleted, "
          f"{len(generated)} generated copies, {len(shared)} navigation entries moved")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
