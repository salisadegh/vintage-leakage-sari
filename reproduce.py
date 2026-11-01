"""Reproduce every result in the paper, in order.

Usage:  python reproduce.py --data-dir data [--out results] [--jobs 2] [--dry-run]
Steps: download and verify the pinned ECDC files (if missing); forecast errors for all analyses (run_all.py);
sensitivity runs; Figure 1; surge alerts at the 75th (main), 50th and 90th percentile thresholds (alerts.py);
forecast-horizon audit (horizon_audit.py); the table of every number in the paper (paper_numbers.py).
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out", default="results")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--dry-run", action="store_true", help="print the steps without running them")
    a = ap.parse_args()
    py = sys.executable
    d, o = a.data_dir, a.out
    sens = os.path.join(o, "sensitivity")
    steps = []
    if not os.path.exists(os.path.join(d, "SARIRates.csv")):
        steps.append(["fetch_data.py", "--data-dir", d])
    steps += [
        ["run_all.py", "--data-dir", d, "--out", o, "--jobs", str(a.jobs)],
        ["run_all.py", "--data-dir", d, "--out", os.path.join(sens, "timely_2wk"), "--only", "main", "--first-delay", "2"],
        ["run_all.py", "--data-dir", d, "--out", os.path.join(sens, "timely_6wk"), "--only", "main", "--first-delay", "6"],
        ["run_all.py", "--data-dir", d, "--out", os.path.join(sens, "log_offset_1"), "--only", "main", "--eps", "1.0"],
        ["run_all.py", "--data-dir", d, "--out", os.path.join(sens, "restatement_5pct"), "--only", "main",
         "--max-restatement", "0.05"],
        ["make_paper_figure.py", "--data-dir", d, "--results", o],
        ["alerts.py", "--data-dir", d, "--results", o],
        ["alerts.py", "--data-dir", d, "--results", o, "--quantile", "0.5"],
        ["alerts.py", "--data-dir", d, "--results", o, "--quantile", "0.9"],
        ["horizon_audit.py", "--data-dir", d, "--results", o],
        ["paper_numbers.py", "--results", o],
    ]
    for s in steps:
        cmd = [py, os.path.join(HERE, s[0])] + s[1:]
        print(">", " ".join([os.path.basename(py)] + s), flush=True)
        if not a.dry_run:
            r = subprocess.run(cmd, stdout=subprocess.DEVNULL if s[0] != "run_all.py" else None)
            if r.returncode != 0:
                sys.exit(f"step failed: {' '.join(s)}")
    if not a.dry_run:
        print(f"Done. Every number in the paper is listed in {os.path.join(o, 'paper_numbers.md')}")


if __name__ == "__main__":
    main()
