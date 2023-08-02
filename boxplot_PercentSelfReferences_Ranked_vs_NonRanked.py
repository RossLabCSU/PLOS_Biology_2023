
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def main():

    ioannidis_authors, ioannidis_df = get_ioannidis_authors()

    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()

    boxplot_df = {'Percent Self-References':[],
                'Category':[],
                'Xposition':[]}
        
    minimum_references = 20

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

        boxplot_df['Percent Self-References'].append(perc_selfref)
        boxplot_df['Xposition'].append(0)
        
        if max_authors[0] in ioannidis_authors:
            boxplot_df['Category'].append('Ranked Authors')
        else:
            boxplot_df['Category'].append('Non-Ranked Authors')
        
    h.close()
    
    ranked_vals = [val for i, val in enumerate(boxplot_df['Percent Self-References']) if boxplot_df['Category'][i] == 'Ranked Authors']
    nonranked_vals = [val for i, val in enumerate(boxplot_df['Percent Self-References']) if boxplot_df['Category'][i] == 'Non-Ranked Authors']

    tstat, pval = stats.ttest_ind(ranked_vals, nonranked_vals, alternative='two-sided')

    print('\nP-value, two-sided t-test:', str(pval))
    print('Best p-value precision is < 1 x 10^-300\n')
    
    boxplot(boxplot_df)
    

def boxplot(df):

    order = ['Non-Ranked Authors', 'Ranked Authors']
    pal = ['#4C8055', '#967969']  # GREEN, MOCHA
    
    sns.boxplot(x='Xposition', y='Percent Self-References', data=df, hue='Category', hue_order=order, showfliers=False, palette=['0.8'])
    sns.stripplot(x='Xposition', y='Percent Self-References', data=df, hue='Category', hue_order=order, palette=pal, dodge=True, alpha=0.3, s=1.5)
    plt.xticks([])
    plt.xlabel('')
    plt.yticks(fontname='Arial', fontsize=12)
    plt.ylabel('Percent Self-References', fontname='Arial', fontsize=14)
    
    from matplotlib.lines import Line2D

    legend_elements = [Line2D([0], [0], marker='o', color='w', label=order[0], markerfacecolor=pal[0], markersize=8),
                    Line2D([0], [0], marker='o', color='w', label=order[1], markerfacecolor=pal[1], markersize=8)]

    ax = plt.gca()
    ax.legend(handles=legend_elements, bbox_to_anchor=(0.5,1), loc=8, handletextpad=0.0, prop={'family':'Arial'})
    
    plt.ylim(-2, 102)
    
    fig = plt.gcf()
    fig.set_size_inches(3,5)
    plt.savefig('Fig6A_PercentSelfReferences_Ranked_vs_NonRanked_Boxplot.tif', bbox_inches='tight', dpi=600)
    plt.close()


def get_ioannidis_authors():

    h = open('Table_1_Authors_career_2021_pubs_since_1788_wopp_extracted_202209b.txt')
    header = h.readline()
    
    authors = set()
    df = {}

    for line in h:
        author, *remainder = line.rstrip().split('\t')
        rank = int(remainder[5].replace(',', '').replace('"', ''))
        if rank > 1000000:
            continue
        author_info = author.replace('"', '').replace('.', ' ').split(', ')     # REPLACING THE '.' WITH A SPACE (' ') AND USING .rstrip() IN THE NEXT LINE YIELDS THE PROPER MIDDLE INITIALS FOR AUTHORS WITH MORE THAN ONE MIDDLE INITIAL.
        author_info[-1] = author_info[-1].rstrip()
        author = ' '.join(author_info[1:] + [author_info[0]])

        authors.add(author)
        
        df[author] = rank

    h.close()

    return authors, df
    

if __name__ == '__main__':
    main()
