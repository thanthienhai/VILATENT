"""Hình 1 (tổng quan ViLatent) bằng matplotlib, biểu tượng vẽ tay dạng vector.

Ghi paper_icisn/figures/overview.{pdf,png} và paper_icisn_vi/figures/overview.{pdf,png}.
Không đọc số liệu nào; chỉ là sơ đồ.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
BLUE, BLUE_L = "#0F4D92", "#DCE8F5"
RED, RED_L = "#B64342", "#F8E3E2"
GREY, GREY_L = "#5B6770", "#ECEEF0"
INK = "#222222"

TEXT = {
    "en": dict(
        once="written once per document, without the question",
        doc="Document $C$", writer="Writer", writer2="bottom $L$ layers, trained",
        mem="$M$", mem2="$k_m$ vectors",
        q="Question $Q$", ev="BM25 sentences $E$", ev2="$\\leq k(r)-k_m$ tokens",
        reader="Reader", reader2="frozen Qwen3.5-2B",
        router="Router", yes="yes: keep the answer", no="no: read $M$ alone"),
    "vi": dict(
        once="ghi một lần cho mỗi tài liệu, không cần biết câu hỏi",
        doc="Tài liệu $C$", writer="Bộ ghi", writer2="$L$ lớp dưới, được huấn luyện",
        mem="$M$", mem2="$k_m$ vector",
        q="Câu hỏi $Q$", ev="Câu BM25 $E$", ev2="$\\leq k(r)-k_m$ token",
        reader="Mô hình đọc", reader2="Qwen3.5-2B đóng băng",
        router="Router", yes="có: giữ câu trả lời", no="không: chỉ đọc $M$"),
}


def box(ax, x, y, w, h, fc, ec, lw=0.9, z=2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=2",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, p, q, color=INK, ls="-", rad=0.0, lw=0.9):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=6, lw=lw,
                                 color=color, ls=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}", zorder=3))


def doc_icon(ax, x, y, s=1.0, color=GREY, fill="white", lines=5, hi=()):
    w, h, f = 8 * s, 10.5 * s, 2.6 * s
    x0, y0 = x - w / 2, y - h / 2
    ax.add_patch(Polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h - f), (x0 + w - f, y0 + h),
                          (x0, y0 + h)], closed=True, fc=fill, ec=color, lw=0.8, zorder=4))
    ax.add_patch(Polygon([(x0 + w - f, y0 + h), (x0 + w - f, y0 + h - f), (x0 + w, y0 + h - f)],
                         closed=True, fc=GREY_L, ec=color, lw=0.6, zorder=5))
    for i in range(lines):
        yy = y0 + h - 4.4 * s - i * 1.35 * s
        if yy < y0 + 1.2 * s:
            break
        if i in hi:
            ax.add_patch(Rectangle((x0 + 1.2 * s, yy - 0.5 * s), w - 2.4 * s, 1.05 * s,
                                   fc=RED_L, ec="none", zorder=5))
        ax.plot([x0 + 1.5 * s, x0 + w - 1.5 * s], [yy, yy], color=RED if i in hi else GREY,
                lw=0.7, solid_capstyle="round", zorder=6)


def vectors_icon(ax, x, y, n=4):
    gap, hh, ww = 1.1, 2.0, 11
    top = y + (n * hh + (n - 1) * gap) / 2
    shades = ["#7FA6D6", "#4F82BD", "#2A66AD", "#0F4D92"]
    for i in range(n):
        yy = top - (i + 1) * hh - i * gap
        ax.add_patch(Rectangle((x - ww / 2, yy), ww, hh, fc=shades[i % 4], ec="white", lw=0.4, zorder=4))


def bubble_icon(ax, x, y):
    box(ax, x, y + 0.6, 10, 7.2, "white", GREY, lw=0.8, z=4)
    ax.add_patch(Polygon([(x - 2.5, y - 3), (x - 4.5, y - 5.6), (x, y - 3)], closed=True,
                         fc="white", ec=GREY, lw=0.8, zorder=4))
    ax.plot([x - 2.6, x], [y - 3.02, y - 3.02], color="white", lw=1.4, zorder=5)
    ax.text(x, y + 0.5, "?", ha="center", va="center", fontsize=8, color=GREY, zorder=6,
            fontweight="bold")


def snow_icon(ax, x, y, r=2.6):
    import math
    for k in range(3):
        a = math.pi * k / 3
        ax.plot([x - r * math.cos(a), x + r * math.cos(a)],
                [y - r * math.sin(a), y + r * math.sin(a)], color=GREY, lw=0.9,
                solid_capstyle="round", zorder=6)


def draw(lang):
    t = TEXT[lang]
    fig, ax = plt.subplots(figsize=(4.8, 1.88))
    ax.set_xlim(0, 120)
    ax.set_ylim(-6.5, 40.5)
    ax.axis("off")
    plt.rcParams["mathtext.fontset"] = "dejavusans"
    fs = 6.4
    yt, yb = 29.0, 5.0

    # ---- hàng ghi
    doc_icon(ax, 9, yt + 0.5, 1.15, lines=6)
    ax.text(9, yt - 8.2, t["doc"], ha="center", va="top", fontsize=fs, color=INK)
    box(ax, 40, yt, 31, 12.5, BLUE_L, BLUE)
    ax.text(40, yt + 2.2, t["writer"], ha="center", va="center", fontsize=fs + 0.6,
            color=BLUE, fontweight="bold")
    ax.text(40, yt - 2.6, t["writer2"], ha="center", va="center", fontsize=fs - 0.6, color=INK)
    vectors_icon(ax, 76, yt + 0.5)
    ax.text(76, yt - 8.2, t["mem"] + " (" + t["mem2"] + ")",
            ha="center", va="top", fontsize=fs, color=INK)
    arrow(ax, (14.5, yt + 0.5), (24.2, yt))
    arrow(ax, (55.8, yt), (69.5, yt + 0.5))
    ax.add_patch(FancyBboxPatch((1.2, yt - 13.4), 85.5, 22.4, boxstyle="round,pad=0,rounding_size=3",
                                fc="none", ec=BLUE, lw=0.7, ls=(0, (3, 2)), zorder=1))
    ax.text(3.6, yt + 9.0, t["once"], ha="left", va="center", fontsize=fs - 0.7, color=BLUE,
            style="italic", bbox=dict(fc="white", ec="none", pad=0.6), zorder=2)

    # ---- hàng đọc
    bubble_icon(ax, 9, yb + 1.6)
    ax.text(9, yb - 6.2, t["q"], ha="center", va="top", fontsize=fs, color=INK)
    doc_icon(ax, 41, yb + 0.8, 1.0, lines=6, hi=(1, 3))
    ax.text(41, yb - 6.2, t["ev"], ha="center", va="top", fontsize=fs, color=INK)
    box(ax, 76, yb, 27, 12.5, GREY_L, GREY)
    snow_icon(ax, 67.6, yb + 2.4)
    ax.text(80, yb + 2.2, t["reader"], ha="center", va="center", fontsize=fs + 0.6,
            color=GREY, fontweight="bold")
    ax.text(76, yb - 2.6, t["reader2"], ha="center", va="center", fontsize=fs - 0.6, color=INK)
    # router
    rx = 106
    ax.add_patch(Polygon([(rx, yb + 7), (rx + 11, yb), (rx, yb - 7), (rx - 11, yb)], closed=True,
                         fc=RED_L, ec=RED, lw=0.9, zorder=2))
    ax.text(rx, yb, t["router"], ha="center", va="center", fontsize=fs - 0.5, color=RED,
            fontweight="bold")
    ax.text(rx, yb - 7.8, t["yes"], ha="center", va="top", fontsize=fs - 0.9, color=RED, style="italic",
            linespacing=1.05)

    # ---- mũi tên
    arrow(ax, (14.5, yb + 1.6), (35.5, yb + 0.8))
    arrow(ax, (46.5, yb + 0.8), (62.3, yb))
    arrow(ax, (89.5, yb), (94.8, yb))
    arrow(ax, (76, yt - 13.4), (76, yb + 6.4))
    # tài liệu -> câu BM25
    ax.plot([9, 9], [yt - 11.6, yt - 11.6], lw=0)
    arrow(ax, (9, yt - 10.4), (9, yt - 10.4))
    ax.add_patch(FancyArrowPatch((18.6, yt - 9.6), (38.5, yb + 7.6), arrowstyle="-|>",
                                 mutation_scale=6, lw=0.9, color=INK, shrinkA=0, shrinkB=0,
                                 connectionstyle="angle,angleA=0,angleB=90,rad=2", zorder=3))
    # router -> bộ nhớ (đỏ, nét đứt)
    ax.add_patch(FancyArrowPatch((rx, yb + 7), (82.2, yt + 0.5), arrowstyle="-|>",
                                 mutation_scale=6, lw=0.9, color=RED, ls=(0, (3, 2)),
                                 shrinkA=0, shrinkB=0,
                                 connectionstyle="angle,angleA=90,angleB=0,rad=3", zorder=3))
    ax.text(rx - 2.0, yt + 1.4, t["no"], ha="right", va="bottom", fontsize=fs - 0.9, color=RED,
            style="italic")
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    return fig


def main():
    for lang, d in (("en", "paper_icisn"), ("vi", "paper_icisn_vi")):
        fig = draw(lang)
        out = ROOT / d / "figures"
        out.mkdir(exist_ok=True)
        fig.savefig(out / "overview.pdf")
        fig.savefig(out / "overview.png", dpi=220)
        plt.close(fig)
        print("wrote", out / "overview.pdf")


if __name__ == "__main__":
    main()
