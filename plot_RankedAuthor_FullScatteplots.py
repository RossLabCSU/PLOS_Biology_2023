
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np


def main():
    
    max_cutoffs = [2000, 100, 400000]
    categories = ['Total Publications', 'Percentage of All Self Publications Referenced', 'Author Rank']
    fig_labels = [('FigS3A', 'FigS3B'), ('FigS3C', 'FigS3D'), ('FigS3E', 'FigS3F')]
    minimum_references = 20
    minimum_percent_selfrefs = 30 - 0.00000001
    
    ioannidis_authors, ioannidis_df, ioannidis_authors_to_numpubs = get_ioannidis_authors()
    df = get_selfref_data(ioannidis_df, ioannidis_authors_to_numpubs, minimum_references)
    df = pd.DataFrame.from_dict(df)
    
    for i, category in enumerate(categories):
        max_cutoff = max_cutoffs[i]
        fig_label_set = fig_labels[i]
        fig_label = fig_label_set[0]    # GETS OVERRIDDEN TO INDEX [1] IF THE CUTOFFS ARE USED
        for use_min_percent_selfrefs_cutoff in [False, True]:
            if use_min_percent_selfrefs_cutoff:
                fig_label = fig_label_set[1]
                plotting_df = df[df['Percent Self-References'] > minimum_percent_selfrefs]
                plotting_df = plotting_df[plotting_df[category] <= max_cutoff]
                plotting_scatter(plotting_df, fig_label, category, 'Percent Self-References')
            else:
                plotting_scatter(df, fig_label, category, 'Percent Self-References')
                
    plotting_df = make_authorset_df(df)
    plotting_df = pd.DataFrame.from_dict(plotting_df)
    filtered_df = plotting_df[plotting_df['Total Publications'] >= 500]
    plotting_scatter(filtered_df, 'FigS4C', 'Total Publications', 'Author Rank')
    plotting_scatter(plotting_df, 'FigS4B', 'Total Publications', 'Author Rank')

    
def make_authorset_df(df):

    plotting_df = {key:[] for key in df}
    
    author_tracking = set()
    for i, author in enumerate(list(df['Author'])):
        
        if author in author_tracking:
            continue
        
        for key in plotting_df:
            plotting_df[key].append( df[key][i] )
            
        author_tracking.add(author)

    return plotting_df

    
def get_selfref_data(ioannidis_df, ioannidis_authors_to_numpubs, minimum_references):

    df = {'Total Publications':[],
        'Percentage of All Self Publications Referenced':[],
        'Author Rank':[],
        'Percent Self-References':[],
        'Author':[]}

    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()
    
    for line in h:
        journal, pmid, all_authors, num_selfrefs_all, perc_selfrefs_all, max_authors, selfref, totalrefs, perc = line.rstrip().split('\t')

        totalrefs = int(totalrefs)
        if int(totalrefs) < minimum_references:
            continue
                
        max_authors = max_authors.split(';')

        for author in max_authors:
            if author not in ioannidis_authors_to_numpubs:
                continue
                
            perc_selfref = int(selfref) / totalrefs * 100

            totalpubs = ioannidis_authors_to_numpubs[author]
            author_rank = ioannidis_df[author]
            totalpubs = ioannidis_authors_to_numpubs[author]
            perc_totalpubs_reffed = int(selfref) / totalpubs * 100

            df['Total Publications'].append(totalpubs)
            df['Percent Self-References'].append(perc_selfref)
            df['Author'].append(author)
            df['Percentage of All Self Publications Referenced'].append(perc_totalpubs_reffed)
            df['Author Rank'].append(author_rank)
        
    h.close()
    
    return df
        
    
def plotting_scatter(df, fig_label, xcat, ycat):

    xy = np.vstack([df[xcat], df[ycat]])
    z = gaussian_kde(xy)(xy)

    plt.scatter(df[xcat], df[ycat], linewidth=0, alpha=0.3, s=6, c=z, cmap=sns.color_palette('coolwarm', as_cmap=True))

    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel(xcat, fontname='Arial', fontsize=14)
    plt.ylabel(ycat, fontname='Arial', fontsize=14)
    
    plt.savefig(fig_label + '_' + ycat.title().replace(' ', '') + '_vs_' + xcat.title().replace(' ', '') + '_Scatterplot.tif', bbox_inches='tight', dpi=600, pil_kwargs={'compression':'tiff_lzw'})
    plt.close()
    

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