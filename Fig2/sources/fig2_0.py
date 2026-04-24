import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from matplotlib.colors import ListedColormap
from scipy.interpolate import griddata

params = {
    'font.family': 'Times'
}
matplotlib.rcParams.update(params)

datadir       = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig2/sources/'
datadir2write = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig2/sources/data_each/'


# ============================================================
# Basic style / helpers
# ============================================================
fsize_main   = 14
fsize_panel  = 14
fsize_tick   = 14
fsize_bar    = 14

terrain = cm.get_cmap('terrain', 36)

margin = 0.1
xmin, xmax = -margin, 3/2 + margin
ymin, ymax = -margin, np.sqrt(3)/2 + margin

dx = xmax - xmin
dy = ymax - ymin

# 데이터 비율을 그대로 사용: width : height = sqrt(3) : 1
# 실제로는 dx/dy 가 거의 sqrt(3)에 해당
cell_ratio = dx / dy          # width / height
cell_h_over_w = dy / dx       # height / width


def draw_realspace_panel(ax, stack_type, ang12, ang32):
    datadir_each = f"{datadir2write}{stack_type}_{ang12}_{ang32}/"

    Cell    = np.genfromtxt(f"{datadir_each}generate.xyz", max_rows=3)
    L       = Cell[0, 0]

    Ratio12 = np.genfromtxt(f"{datadir_each}Ratio_figdata_12.txt", skip_header=1)
    Ratio23 = np.genfromtxt(f"{datadir_each}Ratio_figdata_23.txt", skip_header=1)

    num = 1500
    x   = np.linspace(0, 3/2, num)
    y   = np.linspace(0, np.sqrt(3)/2, num)

    SurfaceIntRebo1 = griddata(
        (Ratio12[:, 0] / L, Ratio12[:, 1] / L),
        Ratio12[:, -1],
        (x[None, :], y[:, None]),
        method='linear',
        fill_value=100
    )
    SurfaceIntRebo2 = griddata(
        (Ratio23[:, 0] / L, Ratio23[:, 1] / L),
        Ratio23[:, -1],
        (x[None, :], y[:, None]),
        method='linear',
        fill_value=100
    )
    SurfaceIntReboSum = SurfaceIntRebo1 * 6 + SurfaceIntRebo2

    ax.imshow(
        SurfaceIntReboSum,
        extent=[0, 3/2, 0, np.sqrt(3)/2],
        origin="lower",
        cmap='terrain',
        vmin=0, vmax=35,
        interpolation='nearest'
    )

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # 데이터 비율과 axes box 비율을 동시에 고정
    ax.set_aspect('equal', adjustable='box')
    ax.set_box_aspect(cell_h_over_w)
    ax.set_anchor('C')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(
        labelsize=fsize_tick,
        direction='inout',
        length=3,
        width=0.8,
        top=True, right=True,
        bottom=True, left=True
    )


def plot_ratio_bars(ax, stack_type, idx_pair,ang12="1.53",ang32s=["1.53", "1.43", "1.23"], show_xlabel=False):
    xx          = np.arange(len(ang32s))

    vals_bottom = []
    vals_top    = []

    for ang32 in ang32s:
        datadir_each = f"{datadir2write}{stack_type}_{ang12}_{ang32}/"
        ratio = np.genfromtxt(f"{datadir_each}ratioVals.txt", skip_header=1)[:, -1]
        vals_bottom.append(ratio[idx_pair[0]])
        vals_top.append(   ratio[idx_pair[1]])

    vals_bottom = np.array(vals_bottom)
    vals_top    = np.array(vals_top)

    barw = 0.46
    b0 = ax.bar(xx, vals_bottom, color=terrain(idx_pair[0]), width=barw)
    b1 = ax.bar(xx, vals_top,    color=terrain(idx_pair[1]), width=barw, bottom=vals_bottom)

    totals = vals_bottom + vals_top
    ax.bar_label(b1, labels=[f"{v:.1f}" for v in totals], padding=2, fontsize=fsize_tick)

    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(0, 110)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.tick_params(axis='y', labelsize=fsize_tick, length=3, width=0.8)
    ax.tick_params(axis='x', labelsize=fsize_tick, length=3, width=0.8)

    if show_xlabel:
        ax.set_xticks(xx)
        ax.set_xticklabels([rf"{ang32}"+r"${}^{\circ}$" for ang32 in ang32s], fontsize=fsize_tick)
    else:
        ax.set_xticks(xx)
        ax.set_xticklabels([])


def make_discrete_cbar(ax, colors, labels):
    cmap = ListedColormap(colors)
    arr = np.arange(len(colors)).reshape(-1, 1)

    ax.imshow(arr, cmap=cmap, aspect='auto', origin='lower')
    ax.set_xticks([])
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=fsize_main-3)
    ax.yaxis.tick_right()
    ax.tick_params(axis='y', length=0, pad=3)

    for sp in ax.spines.values():
        sp.set_linewidth(0.8)

    # ax.text(1.6, 1.04, left_title, transform=ax.transAxes,
    #         ha='center', va='bottom', fontsize=fsize_main-2)
    # ax.text(3.05, 1.04, right_title, transform=ax.transAxes,
    #         ha='center', va='bottom', fontsize=fsize_main-2)


# ============================================================
# Figure geometry in inches
# ============================================================
fig_w = 6.8

left_margin   = 0.08
right_margin  = 0.04
top_margin    = 0.055
bottom_margin = 0.08

# horizontal geometry
usable_w = fig_w * (1 - left_margin - right_margin)

# top 3x3: 3 equal columns, no gap
top_gap_x = 0.0
top_cell_w = usable_w / 3.0
top_cell_h = top_cell_w / cell_ratio
top_block_h = 3 * top_cell_h

# middle: left 3x2 has same cell size as top, equal aspect preserved
mid_left_cell_w = top_cell_w
mid_left_cell_h = top_cell_h
mid_left_block_w = 2 * mid_left_cell_w
mid_left_block_h = 3 * mid_left_cell_h

# gap between middle-left 2 columns and bar column: smaller than one top-cell gap
mid_gap_x = 0.06 * fig_w

# bar column width chosen so its right edge matches top panel right edge
mid_bar_w = usable_w - mid_left_block_w - mid_gap_x
mid_bar_h = mid_left_block_h

# vertical spacings
# gap_top_to_mid = 0.07 * fig_w
# gap_mid_to_cbar = 0.075 * fig_w
gap_top_to_mid  = 0.10 * fig_w
gap_mid_to_cbar = 0.105 * fig_w

# colorbar area
cbar_h = 0.3 * fig_w

fig_h = (
    top_margin * fig_w
    + top_block_h
    + gap_top_to_mid
    + mid_left_block_h
    + gap_mid_to_cbar
    + cbar_h
    + bottom_margin * fig_w
)

fig = plt.figure(figsize=(fig_w, fig_h))

# normalized positions
L = left_margin
R = 1 - right_margin
T = 1 - (top_margin * fig_w) / fig_h
B = (bottom_margin * fig_w) / fig_h

# heights in normalized figure coordinates
top_h_n   = top_block_h / fig_h
mid_h_n   = mid_left_block_h / fig_h
cbar_h_n  = cbar_h / fig_h
gap_tm_n  = gap_top_to_mid / fig_h
gap_mc_n  = gap_mid_to_cbar / fig_h

# top block
top_bottom = T - top_h_n
gs_top = fig.add_gridspec(
    3, 3,
    left=L, right=R,
    bottom=top_bottom, top=T,
    wspace=0.0, hspace=0.0
)

# middle block
mid_top    = top_bottom - gap_tm_n
mid_bottom = mid_top - mid_h_n

mid_left_w_n = mid_left_block_w / fig_w
mid_gap_x_n  = mid_gap_x / fig_w
mid_bar_w_n  = mid_bar_w / fig_w

mid_left = L
mid_left_right = L + mid_left_w_n
mid_bar_left = mid_left_right + mid_gap_x_n
mid_bar_right = R

gs_mid_left = fig.add_gridspec(
    3, 2,
    left=mid_left, right=mid_left_right,
    bottom=mid_bottom, top=mid_top,
    wspace=0.0, hspace=0.0
)

gs_mid_bar = fig.add_gridspec(
    3, 1,
    left=mid_bar_left, right=mid_bar_right,
    bottom=mid_bottom, top=mid_top,
    hspace=0.0
)

# ============================================================
# Bottom colorbar block: equal spacing for all 6 colorbars
# ============================================================
cbar_top = mid_bottom - gap_mc_n
cbar_bottom = cbar_top - cbar_h_n

total_cbar_w = R - L

# colorbar 자체 폭을 조금 줄이고, 모든 간격을 동일하게 설정
cbar_gap = 0.02          # figure fraction 단위로 직접 지정
cbar_width_scale = 0.2   # 1보다 작게 두면 각 colorbar 폭이 줄어듦

# 6개 colorbar + 5개 동일 간격
base_slot_w = (total_cbar_w - 5 * cbar_gap) / 6.0
cbar_w = base_slot_w * cbar_width_scale

cbar_axes = []
for i in range(6):
    slot_left = L + i * (base_slot_w + cbar_gap)
    ax_left = slot_left 
    cbar_axes.append(fig.add_axes([ax_left, cbar_bottom, cbar_w, cbar_h_n]))

# ============================================================
# Top panel: 3x3, no gap
# ============================================================
top_axes = [[fig.add_subplot(gs_top[i, j]) for j in range(3)] for i in range(3)]

top_stack_types = [
    ["AAA",  "AAB",  "AAC"],
    ["AAAp", "AABp", "AACp"],
    ["AApA", "AApB", "AApC"]
]
top_stack_names = [
    ["AAA",  "AAB",  "AAC"],
    ["AAA'", "AAB'", "AAC'"],
    ["AA'A", "AA'B", "AA'C"]
]

ang12 = "1.53"
ang32 = "1.53"

for i in range(3):
    for j in range(3):
        draw_realspace_panel(
            top_axes[i][j],
            top_stack_types[i][j],
            ang12, ang32
        )

# row labels for middle left panel
middle_row_labels = [r"BN/BN/BN", r"NB/BN/BN", r"BN/NB/BN"]
for i, label in enumerate(middle_row_labels):
    top_axes[i][0].text(
        -0.10, 0.5, label,
        transform=top_axes[i][0].transAxes,
        rotation=270,
        va='center', ha='right',
        fontsize=fsize_panel+2
    )

# ============================================================
# Middle left: 3x2, same cell size and same aspect as top
# ============================================================
mid_left_axes = [[fig.add_subplot(gs_mid_left[i, j]) for j in range(2)] for i in range(3)]

mid_left_stack_types = ["AAA", "AACp", "AApA"]
mid_left_stack_names = ["AAA", "AAC'", "AA'A"]
mid_ang32_cols       = ["1.43", "1.23"]

for i in range(3):
    for j in range(2):
        draw_realspace_panel(
            mid_left_axes[i][j],
            mid_left_stack_types[i],
            "1.53",
            mid_ang32_cols[j]
        )

# row labels for middle left panel
middle_row_labels = [r"BN/BN/BN", r"NB/BN/BN", r"BN/NB/BN"]
for i, label in enumerate(middle_row_labels):
    mid_left_axes[i][0].text(
        -0.10, 0.5, label,
        transform=mid_left_axes[i][0].transAxes,
        rotation=270,
        va='center', ha='right',
        fontsize=fsize_panel+2
    )

# ============================================================
# Middle right: stacked bar ratios
# ============================================================
bar_axes = [fig.add_subplot(gs_mid_bar[i, 0]) for i in range(3)]

bar_specs = [
    ("AAA",  [8, 13], r"BN/BN/BN"),
    ("AACp", [7, 12], r"NB/BN/BN"),
    ("AApA", [0,  8], r"BN/NB/BN"),
]

for i, (stype, idx_pair, rowlab) in enumerate(bar_specs):
    plot_ratio_bars(
        bar_axes[i],
        stype,
        idx_pair,
        show_xlabel=(i == 2)
    )


# ============================================================
# Bottom: 6 colorbars
# ============================================================
# palette approximation; replace if you want exact colors from your original figure
cbar_color_sets = [
    [terrain(0), terrain(1), terrain(2), terrain(3), terrain(4), terrain(5)],
    [terrain(6), terrain(7), terrain(8), terrain(9), terrain(10), terrain(11)],
    [terrain(12), terrain(13), terrain(14), terrain(15), terrain(16), terrain(17)],
    [terrain(18), terrain(19), terrain(20), terrain(21), terrain(22), terrain(23)],
    [terrain(24), terrain(25), terrain(26), terrain(27), terrain(28), terrain(29)],
    [terrain(30), terrain(31), terrain(32), terrain(33), terrain(34), terrain(35)],
]

cbar_labels = [
    ["AAA", "AAB", "AAC", "AA-DW1", "AA-DW2", "AA-DW3"],
    ["ABB", "ABC", "ABA", "AB-DW1", "AB-DW2", "AB-DW3"],
    ["ACC", "ACA", "ACB", "AC-DW1", "AC-DW2", "AC-DW3"],
    ["DW1-AA", "DW1-AB", "DW1-BA", "DW1-DW1", "DW1-DW2", "DW1-DW3"],
    ["DW2-AA", "DW2-AB", "DW2-BA", "DW2-DW1", "DW2-DW2", "DW2-DW3"],
    ["DW3-AA", "DW3-AB", "DW3-BA", "DW3-DW1", "DW3-DW2", "DW3-DW3"],
]

for i, ax in enumerate(cbar_axes):
    make_discrete_cbar(
        ax,
        cbar_color_sets[i],
        cbar_labels[i] #,
    )

fig.savefig(f"{datadir}fig2_0.pdf", dpi=500)

print("Done!")