
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import scoreatpercentile
import numpy as np
import math

axislabel_df = {'Total Publications':'Total Publications',
            'Percent of All Self Publications Referenced':'Percent of All Self Publications Referenced',
            'Author Rank':'Author Rank'}

def main():

    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()
    
    df = {'Total Publications':[],
        'Percent Self-References':[],
        'Percent of All Self Publications Referenced':[],
        'Author':[],
        'Author Rank':[]}

    ioannidis_authors, ioannidis_df, ioannidis_authors_to_numpubs = get_ioannidis_authors()
        
    window_size = 11
    minimum_references = 20

    for line in h:
        journal, pmid, all_authors, num_selfrefs_all, perc_selfrefs_all, max_authors, selfref, totalrefs, perc = line.rstrip().split('\t')
        
        max_authors = max_authors.split(';')
            
        for author in max_authors:
            if author not in ioannidis_authors_to_numpubs:
                continue
            totalrefs = int(totalrefs)
            if int(totalrefs) < minimum_references:
                continue
            perc_selfref = int(selfref) / totalrefs * 100

            totalpubs = ioannidis_authors_to_numpubs[author]

            perc_pubs_referenced = round(int(selfref) / totalpubs *100)

            rank = ioannidis_df[author]
            
            df['Total Publications'].append(totalpubs)
            df['Percent Self-References'].append(perc_selfref)
            df['Author'].append(author)
            df['Author Rank'].append(rank)
            df['Percent of All Self Publications Referenced'].append(perc_pubs_referenced)

    h.close()
    
    plotting_df = calc_rollingmeans_of_medians(df, 'Total Publications', 'Percent Self-References', window_size)
    plot_medians(plotting_df, 'Total Publications', 'Percent Self-References', 'Fig5A')

    plotting_df = calc_rollingmeans_of_medians(df, 'Percent of All Self Publications Referenced', 'Percent Self-References', window_size)
    plot_medians(plotting_df, 'Percent of All Self Publications Referenced', 'Percent Self-References', 'Fig5B')
    
    plotting_df = calc_rollingmeans_of_medians(df, 'Author Rank', 'Percent Self-References', window_size)
    plot_medians(plotting_df, 'Author Rank', 'Percent Self-References', 'Fig5C')
    
    plotting_df = calc_rollingmeans_of_medians(df, 'Total Publications', 'Author Rank', window_size)
    plot_medians(plotting_df, 'Total Publications', 'Author Rank', 'FigS4A')

    totalpubs_cutoffs = [(0, 250), (250, 500), (500, 5000)]
    fig_labels = ['FigS4D', 'FigS4E', 'FigS4F']
    df = pd.DataFrame.from_dict(df)
    
    for i, cutoffs in enumerate(totalpubs_cutoffs):
        temp_df = df[df['Total Publications'] > cutoffs[0]]
        temp_df = temp_df[temp_df['Total Publications'] <= cutoffs[1]]
        plotting_df = calc_rollingmeans_of_medians(temp_df, 'Author Rank', 'Percent Self-References', window_size)
        plot_medians(plotting_df, 'Author Rank', 'Percent Self-References', fig_labels[i])


def calc_rollingmeans_of_medians(df, xcat, ycat, window_size):

    if xcat == 'Author Rank':
        gap_size = 10000
    else:
        gap_size = 10
    
    print('Calculating...', xcat, 'quartiles')
    
    plotting_df = {'Value':[],
                xcat:[],
                'Category':[]}
    xval_list = df[xcat][:]
    yval_list = df[ycat][:]
    max_xval = max([x for x in xval_list if x != 'N/A'])
    min_xval = min([x for x in xval_list if x != 'N/A'])
    if xcat == 'Percent of All Self Publications Referenced':
        gap_size = 5
        window_size = 5
        xval_range = [x for x in range(100)]
        xval_list = np.digitize(xval_list, xval_range, right=True)
    elif xcat == 'Author Rank':
        gap_size = 5000
        window_size = 101
        xval_range = [x for x in range(0, max_xval+1000, 1000)]
        xval_list = np.digitize(xval_list, xval_range, right=True)
        xval_list = [x*1000 for x in xval_list]
    else:
        gap_size = 50
        window_size = 21
        xval_range = [x for x in range(min_xval+1, max_xval)]

    # IN ORDER: [q1, median, q3]
    quartile_lists = [[], [], []]
    final_xvals = []
    
    latest_xval = xval_range[0]
    
    for xval in xval_range:
        
        yvals = [y for i, y in enumerate(yval_list) if xval_list[i] == xval]
        
        if len(yvals) < 3:
            continue
            
        if xval - latest_xval > gap_size:
            break
            
        scores_at_percentiles = scoreatpercentile(yvals, [25, 50, 75])

        for i, score in enumerate(scores_at_percentiles):
            quartile_lists[i].append(score)
            
        final_xvals.append(xval)
        latest_xval = xval
        
    labels = ['1st Quartile (Q1)', 'Median (Q2)', '3rd Quartile (Q3)']
    for i, quartile_list in enumerate(quartile_lists):
        label = labels[i]
        vals = pd.Series(quartile_list)
        rolling_meanvals = list( vals.rolling(window_size, min_periods=math.ceil(window_size/2), center=True).mean() )
        
        new_xval_range = [x for x in xval_range if x in final_xvals]
        if len(rolling_meanvals) < 1:
            continue
        interpolated_rolling_meanvals = list( np.interp(new_xval_range, final_xvals, rolling_meanvals) )

        plotting_df['Value'] += interpolated_rolling_meanvals
        plotting_df[xcat] += new_xval_range
        plotting_df['Category'] += [label] * len(interpolated_rolling_meanvals)

    return plotting_df

    
def plot_medians(df, xcat, ylabel, fig_label):

    colors = ['#95e084', '#42ab2a', '#215515']     # GREEN SHADES

    ax = sns.lineplot(x=xcat, y='Value', data=df, hue='Category', palette=colors, linewidth=2)
    
    q1_vals = [val for i, val in enumerate(df['Value']) if df['Category'][i] == '1st Quartile (Q1)']
    q3_vals = [val for i, val in enumerate(df['Value']) if df['Category'][i] == '3rd Quartile (Q3)']
    xvals = [xval for i, xval in enumerate(df[xcat]) if df['Category'][i] == '3rd Quartile (Q3)']
    ax.fill_between(xvals, q1_vals, q3_vals, color='#42ab2a', alpha=0.2)

    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    if ylabel == 'Percent Self-References':
        plt.ylabel('Percent Self-References', fontname='Arial', fontsize=14)
    else:
        plt.ylabel('Author Rank', fontname='Arial', fontsize=14)
    plt.xlabel(axislabel_df[xcat], fontname='Arial', fontsize=14)

    if fig_label in ['Fig5C', 'FigS4A', 'FigS4D', 'FigS4E', 'FigS4F']:
        leg = plt.legend(loc='upper right', prop={'family':'Arial', 'size':12}, handletextpad=0.3)
    else:
        leg = plt.legend(loc='lower right', prop={'family':'Arial', 'size':12}, handletextpad=0.3)
    for line in leg.get_lines():
        line.set_linewidth(3.0)
        
    cutoffs_df = {'FigS4D':(0, 250), 'FigS4E':(250, 500), 'FigS4F':(500, 5000)}
    if fig_label in ['FigS4D', 'FigS4E', 'FigS4F']:
        cutoff = cutoffs_df[fig_label]
        if cutoff[1] == 5000:
            plt.title('>' + str(cutoff[0]) + ' Total Publications', fontname='Arial', fontsize=14)
        else:
            plt.title(str(cutoff[0]+1) + '-' + str(cutoff[1]) + ' Total Publications', fontname='Arial', fontsize=14)
        if fig_label == 'FigS4D':
            r = [x for x in range(0, 500000, 100000)]
            plt.xticks(r, labels=r, fontname='Arial', fontsize=12)
        else:
            plt.xticks(fontname='Arial', fontsize=12)
        yr = [x for x in range(2,22,2)]
        plt.yticks(yr, labels=yr, fontname='Arial', fontsize=12)
        plt.ylim(2, 21)
    plt.savefig(fig_label + '_' + xcat + '_SelfReferencingRate_SlidingQuartiles.tif', bbox_inches='tight', dpi=600, pil_kwargs={'compression':'tiff_lzw'})
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
        if rank > 1000000:  # EXCLUDE AUTHORS WITH A NUMERICAL RANK >1MILLION
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
