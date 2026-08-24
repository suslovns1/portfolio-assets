#!/usr/bin/env python3
"""
Restore Section 3 of the Notion portfolio from a JSON snapshot.

    python3 restore_section3.py ~/WORK/CV_BUILDER/backups_notion/<snapshot>.json

Snapshots live OUTSIDE this repo (`~/WORK/CV_BUILDER/backups_notion/`) because this
repo is public and the older ones still carry the real client names that the page
now redacts to Company 1 / Company 2.

Appends the snapshot's blocks, then deletes the Section 3 blocks that were there
before — in that order, so a failure mid-way never leaves the page without the
section. Section 3 is the last section on the page, which is what makes this safe.

The diagrams themselves are versioned in git; `git log -- '*.py'` in the parent
folder finds the matching revision, and the image URLs in the snapshot still carry
the `?v=` they were published with.
"""
import json
import os
import sys
import urllib.request

# This repo is public — the token is never committed. Supply it at run time:
#     NOTION_API_KEY=ntn_… python3 restore_section3.py <snapshot>.json
# or drop it in a gitignored `.notion_token` next to this script. It also lives
# in HANDOFF.md, which stays out of this repo.
_here = os.path.dirname(os.path.abspath(__file__))
_file = os.path.join(_here, ".notion_token")
TOKEN = os.environ.get("NOTION_API_KEY") or (
    open(_file).read().strip() if os.path.exists(_file) else "")
if not TOKEN:
    sys.exit("Set NOTION_API_KEY, or put the token in .notion_token next to this script.")

PAGE = "3c499d7c-5959-8164-a0eb-d3ec43b74b87"
BASE = "https://api.notion.com/v1"
H = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28",
     "Content-Type": "application/json"}


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, headers=H, method=method)
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read().decode())


def children(block_id):
    out, cursor = [], None
    while True:
        p = f"/blocks/{block_id}/children?page_size=100"
        if cursor:
            p += f"&start_cursor={cursor}"
        d = req("GET", p)
        out.extend(d["results"])
        if not d.get("has_more"):
            break
        cursor = d["next_cursor"]
    return out


def main(path):
    snapshot = json.load(open(path))
    before = children(PAGE)
    start = next(i for i, b in enumerate(before)
                 if b["type"] == "heading_1"
                 and "3." in "".join(x["plain_text"] for x in b["heading_1"]["rich_text"]))
    doomed = [b["id"] for b in before[start:]]

    print(f"restoring {len(snapshot)} blocks, replacing {len(doomed)}")
    for i in range(0, len(snapshot), 90):
        req("PATCH", f"/blocks/{PAGE}/children", {"children": snapshot[i:i + 90]})
        print(f"  appended {min(i + 90, len(snapshot))}/{len(snapshot)}")
    for bid in doomed:
        req("DELETE", f"/blocks/{bid}")
    print(f"  deleted {len(doomed)} superseded blocks — done")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
