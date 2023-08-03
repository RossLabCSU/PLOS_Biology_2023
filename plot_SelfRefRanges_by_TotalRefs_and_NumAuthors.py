
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def main():

    df = {'Value':[],
        'xpos':[],
        'Category':[]}
    total_refs_ranges = get_ranges('Summarized_TableS4_PercentSelfReferences_by_TotalReferences.tsv')
    df['Value'] += total_refs_ranges
    df['xpos'] += [0 for x in range(len(total_refs_ranges))]
    df['Category'] += ['Total References' for x in range(len(total_refs_ranges))]
    
    num_authors_ranges = get_ranges('Summarized_TableS5_PercentSelfReferences_by_NumAuthors.tsv')
    df['Value'] += num_authors_ranges
    df['xpos'] += [0 for x in range(len(num_authors_ranges))]
    df['Category'] += ['Number of Authors' for x in range(len(num_authors_ranges))]

    tstat, pval = stats.ttest_ind(total_refs_ranges, num_authors_ranges, alternative='two-sided')
    
    print('\nP-value, two-sided t-test:', pval, '\n')
    
    plotting(df)
    
    
def plotting(df):

    order = ['Total References', 'Number of Authors']
    pal = ['#4C8055', '#967969']  # GREEN, MOCHA
    sns.boxplot(x='xpos', y='Value', data=df, hue='Category', showfliers=False, palette=['0.8'])
    sns.stripplot(x='xpos', y='Value', data=df, hue='Category', dodge=True, alpha=0.8, palette=pal)
    plt.xticks([])
    plt.xlabel('')
    plt.yticks(fontname='Arial', fontsize=12)
    plt.ylabel('Range, Median Percent Self-References', fontname='Arial', fontsize=14)
    
    plt.ylim(1, 13)
    
    from matplotlib.lines import Line2D

    legend_elements = [Line2D([0], [0], marker='o', color='w', label=order[0] + ' (Fig 2A)', markerfacecolor=pal[0], markersize=8),
                    Line2D([0], [0], marker='o', color='w', label=order[1] + ' (Fig 3A)', markerfacecolor=pal[1], markersize=8)]

    ax = plt.gca()
    ax.legend(handles=legend_elements, bbox_to_anchor=(0.35,1), loc=8, handletextpad=0.0, prop={'family':'Arial', 'size':10})
    
    fig = plt.gcf()
    fig.set_size_inches(2,5)
    plt.savefig('Fig3C_PercentSelfReferences_RANGES_TotalRefs_vs_NumAuthors.tif', bbox_inches='tight', dpi=600)
    plt.close()
    

def get_ranges(file):

    h = open(file)
    header = h.readline()
    header = h.readline()
    
    ranges = []
    for line in h:
        journal, quartile, range, *vals = line.rstrip().split('\t')
        if quartile != '50th Percentile':
            continue
            
        data_min, data_max = range[1:-1].split(', ')
        data_range = float(data_max) - float(data_min)
        
        ranges.append(data_range)
        
    h.close()
    
    return ranges


if __name__ == '__main__':
    main()
