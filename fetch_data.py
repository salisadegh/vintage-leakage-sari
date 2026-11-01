"""Download the pinned ERVISS SARI files and verify each against the manifest.

Usage:  python fetch_data.py --data-dir data
"""
import argparse
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd  # noqa: E402

import config as C  # noqa: E402
from vl_data import sha256  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    man = pd.read_csv(os.path.join(here, C.MANIFEST))
    os.makedirs(os.path.join(args.data_dir, "snapshots"), exist_ok=True)
    ok = 0
    for r in man.itertuples():
        dest = os.path.join(args.data_dir, r.path)
        if os.path.exists(dest) and sha256(dest) == r.sha256:
            ok += 1
            continue
        url = f"{C.RAW_BASE}/{r.path}"
        for attempt in range(4):
            try:
                urllib.request.urlretrieve(url, dest)
                break
            except Exception as exc:  # network hiccup: retry with backoff
                if attempt == 3:
                    raise SystemExit(f"Could not download {url}: {exc}")
                time.sleep(2 ** attempt)
        if sha256(dest) != r.sha256:
            raise SystemExit(f"Hash mismatch for {r.path}: the source file differs from the pinned version.")
        ok += 1
    print(f"{ok} of {len(man)} files present and verified (commit {C.COMMIT[:7]}).")


if __name__ == "__main__":
    main()
