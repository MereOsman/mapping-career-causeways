import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import seaborn as sns
import  mapping_career_causeways

useful_paths = mapping_career_causeways.Paths()

class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)
    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    Reference:
    """

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

def export_figure(figure_name, figure_folder = useful_paths.figure_dir, png=True, svg=True):

    export_params = {'dpi': 200, 'bbox_inches': 'tight', 'transparent': True}

    if png:
        plt.savefig(f'{figure_folder}{figure_name}.png', **export_params)
    if svg:
        plt.savefig(f'{figure_folder}svg/{figure_name}.svg', **export_params)

def fix_heatmaps(ax):
    """
    Fix for mpl bug that cuts off top/bottom of seaborn viz
    Reference:
    """
    b, t = ax.get_ylim()
    b += 0.5 # Add 0.5 to the bottom
    t -= 0.5 # Subtract 0.5 from the top
    ax.set_ylim(b, t)

def plot_heatmap(mat, x_labels, y_labels=None, cmap=None,
                 figsize=(10,10), fix_heatmap=False, limits = (None, None),
                 annot=True, shorten_xlabel=True,
                 new_order=None,
                 include_rows=None, include_cols=None):

    f, ax = plt.subplots(figsize=figsize)

    if y_labels is None:
        y_labels = x_labels

    # Re-order columns
    if type(new_order) != type(None):
        mat = mat[new_order,:]
        mat = mat[:, new_order]
        x_labels = np.array(x_labels)[new_order]
        y_labels = np.array(y_labels)[new_order]

        map_old_to_new_order = dict(zip(new_order, range(len(new_order))))
        if type(include_rows) != type(None):
            include_rows = [map_old_to_new_order[x] for x in include_rows]
        if type(include_cols) != type(None):
            include_cols = [map_old_to_new_order[x] for x in include_cols]

    # Select a subsection of the matrix
    if type(include_rows) != type(None):
        mat = mat[include_rows,:]
        y_labels = y_labels[include_rows]
    if type(include_cols) != type(None):
        mat = mat[:, include_cols]
        x_labels = x_labels[include_cols]

    if type(cmap) == type(None):
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

    ax = sns.heatmap(
        mat,
        annot=annot,
        cmap=cmap,
        vmin = limits[0],
        vmax = limits[1],
        cbar_kws={"shrink": 0.5},
        center=0, square=True, linewidths=.1)

    if fix_heatmap:
        fix_heatmaps(ax)

    if shorten_xlabel == True:
        x_labels = [x.split(' ')[0]+'..' for x in x_labels]
    plt.yticks(ticks=np.array(list(range(len(y_labels))))+0.5, labels=y_labels, rotation=0)
    plt.xticks(ticks=np.array(list(range(len(x_labels))))+0.5, labels=x_labels, rotation=90)
    # ax.tick_params(axis='both', which='major', labelsize=9)

    return ax
