"""Figure 2 of the ICISN paper: the five preregistered tests on XQuAD-vi as a forest plot.

Reads results/icisn/confirm/numbers.json (written by confirm_numbers.py) and writes
paper_icisn/figures/fig_confirm.pdf (English) and paper_icisn_vi/figures/fig_confirm.pdf (Vietnamese).
Style: scientific-figure-making skill (blue = key result, red = test not passed, neutral = exploratory),
sized for the 12.2 cm text width of the LNCS class.

    python -X utf8 scripts/icisn/make_figures.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
PALETTE = {"blue": "#0F4D92", "red": "#B64342", "neutral": "#767676", "light": "#CFCECE"}
DELTA = 2.0
KEYS = ["H-R1", "H-R1_prompt_fbest", "H-R2a", "H-R2b", "H-S1", "H-S2"]
KINDS = ["main", "explore", "main", "main", "main", "main"]

TEXT = {
    "en": {"dir": "paper_icisn", "single": "Single passages", "long": "Long articles", "xlabel": "Difference in F1 (points)",
           "rows": ["H-R1  gain where selection\nmisses the answer", "H-R1 vs prompt at best $\\mathit{f}$",
                    "H-R2a  router $-$ memory alone", "H-R2b  router $-$ BM25 2k", "H-S1  memory $-$ summary",
                    "H-S2  ME $-$ summary+E"],
           "legend": ["passes (F1 and ACC-LLM)", "does not pass", "exploratory", r"$-\delta$ (H-R2b)"]},
    "vi": {"dir": "paper_icisn_vi", "single": "Đoạn đơn", "long": "Bài dài", "xlabel": "Chênh lệch F1 (điểm)",
           "rows": ["H-R1  lợi ích khi bộ chọn câu\nbỏ sót đáp án", "H-R1 so với prompt ở $\\mathit{f}$ tốt nhất",
                    "H-R2a  router $-$ chỉ bộ nhớ", "H-R2b  router $-$ BM25 2k", "H-S1  bộ nhớ $-$ tóm tắt",
                    "H-S2  ME $-$ tóm tắt+E"],
           "legend": ["đạt (F1 và ACC-LLM)", "không đạt", "thăm dò", r"$-\delta$ (H-R2b)"]},
}


def style():
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5, "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.major.width": 0.8, "ytick.major.width": 0.0, "pdf.fonttype": 42, "mathtext.default": "regular"})


def draw(d, lang):
    T = TEXT[lang]
    fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.0), sharey=True, gridspec_kw={"wspace": 0.06})
    ypos = list(range(len(KEYS)))[::-1]
    for ax, st, title in zip(axes, ("single", "long"), (T["single"], T["long"])):
        ax.axvline(0, color="black", lw=0.8, zorder=1)
        for y, key, kind in zip(ypos, KEYS, KINDS):
            t = d["xquad"][st]["f1"][key]
            diff, lo, hi = t["diff"], t["ci_low"], t["ci_high"]
            if key == "H-R2b":  # the file stores the difference plus delta; plot the raw difference
                diff, lo, hi = t["raw_diff"], lo - DELTA, hi - DELTA
            passed = d["verdict"].get(f"{st}:{key}", {}).get("status") == "đạt"
            if kind == "explore":
                col, face = PALETTE["neutral"], "white"
            else:
                col = PALETTE["blue"] if passed else PALETTE["red"]
                face = col if passed else "white"
            ax.plot([lo, hi], [y, y], color=col, lw=1.6, solid_capstyle="butt", zorder=2)
            ax.plot(diff, y, "o" if kind == "main" else "D", ms=4.6, mfc=face, mec=col, mew=1.2, zorder=3)
            if key == "H-R2b":
                ax.plot([-DELTA, -DELTA], [y - 0.34, y + 0.34], color=PALETTE["red"], lw=0.9, ls=(0, (2, 1.5)), zorder=1)
        ax.set_xlim(-6, 47)
        ax.set_ylim(-0.6, len(KEYS) - 0.4)
        ax.set_xticks([0, 10, 20, 30, 40])
        ax.set_title(title, fontsize=8, pad=4)
        ax.set_xlabel(T["xlabel"], fontsize=7.5)
        ax.tick_params(axis="x", length=2.5, pad=2)
        ax.grid(axis="x", color=PALETTE["light"], lw=0.4, zorder=0)
        ax.set_axisbelow(True)
    axes[0].set_yticks(ypos)
    axes[0].set_yticklabels(T["rows"], fontsize=7)
    axes[0].tick_params(axis="y", length=0)
    axes[1].tick_params(axis="y", length=0)
    axes[1].spines["left"].set_visible(False)
    h = [Line2D([], [], marker="o", ls="", ms=4.6, mfc=PALETTE["blue"], mec=PALETTE["blue"], label=T["legend"][0]),
         Line2D([], [], marker="o", ls="", ms=4.6, mfc="white", mec=PALETTE["red"], mew=1.2, label=T["legend"][1]),
         Line2D([], [], marker="D", ls="", ms=4.2, mfc="white", mec=PALETTE["neutral"], mew=1.2, label=T["legend"][2]),
         Line2D([], [], color=PALETTE["red"], lw=0.9, ls=(0, (2, 1.5)), label=T["legend"][3])]
    fig.legend(handles=h, loc="lower center", ncol=4, frameon=False, fontsize=6.8, bbox_to_anchor=(0.56, -0.015),
               handletextpad=0.3, columnspacing=1.2)
    fig.subplots_adjust(left=0.30 if lang == "en" else 0.34, right=0.99, top=0.93, bottom=0.34)
    out = ROOT / T["dir"] / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "fig_confirm.pdf")
    fig.savefig(out / "fig_confirm.png", dpi=200)
    plt.close(fig)
    print("wrote", out / "fig_confirm.pdf")


def main():
    d = json.loads((ROOT / "results/icisn/confirm/numbers.json").read_text(encoding="utf-8"))
    style()
    for lang in TEXT:
        draw(d, lang)


if __name__ == "__main__":
    main()
