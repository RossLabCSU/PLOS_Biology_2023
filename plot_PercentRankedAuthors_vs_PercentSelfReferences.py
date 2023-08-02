
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math

def main():

    ioannidis_authors, ioannidis_df, ioannidis_authors_to_numpubs = get_ioannidis_authors()

    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()

    minimum_references = 20

    perc_selfref_vals = []
    authors = []

    for line in h:
        journal, pmid, all_authors, num_selfrefs_all, perc_selfrefs_all, max_authors, selfref, totalrefs, perc = line.rstrip().split('\t')

        max_authors = max_authors.split(';')

        if len(max_authors) > 1:
            max_author = max_authors[-1]
        else:
            max_author = max_authors[0]
            
        totalrefs = int(totalrefs)
        if int(totalrefs) < minimum_references:
            continue
        perc_selfref = int(selfref) / totalrefs * 100

        perc_selfref_vals.append(perc_selfref)
        authors.append(max_author)

    h.close()
    
    xvals, yvals = calc_fraction_on_ioannidis_list_RollingMean(perc_selfref_vals, authors, ioannidis_authors)
    plot_lineplot(xvals, yvals)
    
    
def plot_lineplot(xvals, yvals):

    colors = ['#80C4B7', '#E3856B']

    sns.lineplot(x=xvals, y=yvals, color='0.3', linewidth=2.5)  #GRAY
    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Percent Self-References', fontname='Arial', fontsize=14)
    plt.ylabel('Percentage of Max. Authors\non Ranked Author List', fontname='Arial', fontsize=14)
    fig = plt.gcf()
    fig.set_size_inches(5,5)
    plt.savefig('Fig6B_PercentRankedAuthors_vs_PercentSelfReferences.tif', bbox_inches='tight', dpi=600)
    plt.close()

    
def calc_fraction_on_ioannidis_list_RollingMean(perc_selfref_vals, authors, ioannidis_authors):

    xval_range = [x for x in range(100)]
    xval_list = np.digitize(perc_selfref_vals, xval_range, right=True)
        
    yvals = []
    xvals = []
    
    gap_size = 5
    window_size = 5
    
    latest_xval = xval_range[0]
    final_xvals = []
    
    for xval in xval_range:
        
        filtered_authors = [authors[i] for i, perc in enumerate(xval_list) if perc == xval]
        filtered_percs = [perc for perc in xval_list if perc == xval]
        author_indicator = [1 for author in filtered_authors if author in ioannidis_authors]
        
        if len(filtered_percs) < 3:
            continue
            
        if xval - latest_xval > gap_size:
            break
        
        perc_on_list = sum(author_indicator) / len(filtered_authors) * 100
        
        xvals.append(xval)
        yvals.append(perc_on_list)

        final_xvals.append(xval)
        latest_xval = xval
        
    vals = pd.Series(yvals)
    rolling_meanvals = list( vals.rolling(window_size, min_periods=math.ceil(window_size/2), center=True).mean() )
    new_xval_range = [x for x in xval_range if x in final_xvals]
    interpolated_rolling_meanvals = list( np.interp(new_xval_range, final_xvals, rolling_meanvals) )

    return new_xval_range, interpolated_rolling_meanvals

    
def calc_fraction_on_ioannidis_list(perc_selfref_vals, authors, ioannidis_authors):

    xval_range = np.linspace(0, max(perc_selfref_vals))
    yvals = []
    xvals = []
    
    for xval in xval_range:
        
        filtered_authors = [authors[i] for i, perc in enumerate(perc_selfref_vals) if perc >= xval-0.000001]
        filtered_percs = [perc for perc in perc_selfref_vals if perc >= xval-0.000001]
        author_indicator = [1 for author in filtered_authors if author in ioannidis_authors]
        
        perc_on_list = sum(author_indicator) / len(filtered_authors) * 100
        
        xvals.append(xval)
        yvals.append(perc_on_list)
        
    return xvals, yvals


def get_ioannidis_authors():

    h = open('Table_1_Authors_career_2021_pubs_since_1788_wopp_extracted_202209b.txt')
    header = h.readline()
    
    authors = set()
    df = {}
    authors_to_numpubs = {}

    for line in h:
        author, *remainder = line.rstrip().split('\t')
        rank = int(remainder[5].replace(',', '').replace('"', ''))
        numpubs = int(remainder[2].replace(',', '').replace('"', ''))
        if rank > 1000000:
            continue
        author_info = author.replace('"', '').replace('.', ' ').split(', ')     # REPLACING THE '.' WITH A SPACE (' ') AND USING .rstrip() IN THE NEXT LINE YIELDS THE PROPER MIDDLE INITIALS FOR AUTHORS WITH MORE THAN ONE MIDDLE INITIAL.
        author_info[-1] = author_info[-1].rstrip()
        author = ' '.join(author_info[1:] + [author_info[0]])

        authors.add(author)
        
        df[author] = rank
        authors_to_numpubs[author] = numpubs

    h.close()

    return authors, df, authors_to_numpubs
    

if __name__ == '__main__':
    main()
