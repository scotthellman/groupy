import matplotlib.pyplot as plt
import numpy as np

#from http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor
def multiplication_table_with_ordering(group, ordering=None):
    if ordering is None:
        ordering = list(group.elements.keys())
    #build table
    table = np.zeros((len(group),len(group)))
    for i,left in enumerate(ordering):
        for j,right in enumerate(ordering):
            table[i,j] = ordering.index((group[left]*group[right]).name)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(table, cmap=plt.cm.jet)
    ax.set_xticks(np.arange(table.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(table.shape[1])+0.5, minor=False)

    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.set_xticklabels(ordering, minor=False)
    ax.set_yticklabels(ordering, minor=False)
    plt.show()
