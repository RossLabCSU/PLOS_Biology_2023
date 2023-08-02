
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import scoreatpercentile
import numpy as np
import math

journal_args = ['PlosBiol', 'PlosGenet', 'PlosPath', 'PlosMed', 'PlosCompBiol', 'MCB', 'Cell', 'mBio', 'CurrBiol', 'Genetics', 'BMCmed', 'Bioinformatics', 'Nature', 'Science', 'JCellBiol']
j_hue_order = ['PLOS Biology', 'PLOS Genetics', 'PLOS Pathogens', 'PLOS Medicine', 'PLOS Comput Biol', 'Current Biology', 'Genetics', 'mBio', 'BMC Medicine', 'Bioinformatics', 'Cell', 'Nature', 'Science', 'Mol and Cell Biol', 'J Cell Biology']
legend_order = [0,5,1,6,2,7,3,8,4,9,10,11,12,13,14]
journal_labels = ['PLOS Biology', 'PLOS Genetics', 'PLOS Pathogens', 'PLOS Medicine', 'PLOS Comput Biol', 'Mol and Cell Biol', 'Cell', 'mBio', 'Current Biology', 'Genetics', 'BMC Medicine','Bioinformatics', 'Nature', 'Science', 'J Cell Biology']
journal_df = {journal_arg:journal_labels[i] for i, journal_arg in enumerate(journal_args)}
journal_df['All Publications'] = 'All Publications'


def main():

    combined_df = {'Total References':[],
            'Percent Self-References':[],
            'Journal':[]}
            
            
    df = {'Total References':[],
        'Percent Self-References':[],
        'Journal':[]}

    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()

    minimum_references = 20
    window_size = 11

    for line in h:
        journal, pmid, all_authors, num_selfrefs_all, perc_selfrefs_all, max_authors, selfref, totalrefs, perc = line.rstrip().split('\t')
        
        totalrefs = int(totalrefs)
        if int(totalrefs) < minimum_references:
            continue
            
        perc_selfref = int(selfref) / totalrefs * 100
        
        df['Total References'].append(totalrefs)
        df['Percent Self-References'].append(perc_selfref)
        df['Journal'].append(journal)
        
        combined_df['Total References'].append(totalrefs)
        combined_df['Percent Self-References'].append(perc_selfref)
        combined_df['Journal'].append(journal)
        
        combined_df['Total References'].append(totalrefs)
        combined_df['Percent Self-References'].append(perc_selfref)
        combined_df['Journal'].append('All Publications')

    h.close()

    plotting_df = calc_rollingmeans_of_medians(combined_df, 'All Publications', window_size)

    subplots(plotting_df, 'Fig2A')
    plot_medians_alljournals(plotting_df, 'Fig2B')
    
    
def plot_medians_alljournals(df, fig_label):

    colors = ['#80C4B7', '#E3856B', '#b790d4']
    
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae65']
    col1 = [colors[i] for i in range(0, len(colors), 2)]
    col2 = [colors[i] for i in range(1, len(colors), 2)]
    colors = col1[:5] + col2[:5] + col1[5:] + col2[5:]
    colors = colors[:15]    # THERE ARE 15 JOURNALS PLOTTED IN FIG 2B
    
    df = pd.DataFrame.from_dict(df)
    plotting_df = df[df['Category'] == '50th Percentile']
    if fig_label == 'Fig2B':    # RESTRICT PLOTTING TO A MAXIMUM OF 200 TOTAL REFERENCES FOR MAIN MANUSCRIPT FIGURE ONLY
        df = df[df['Total References'] <= 200]

    ax = sns.lineplot(x='Total References', y='Value', data=plotting_df, hue='Journal', palette=colors, linewidth=2, hue_order=j_hue_order)

    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.ylabel('Median Percent Self-References', fontname='Arial', fontsize=14)
    plt.xlabel('Total References', fontname='Arial', fontsize=14)

    leg_handles,leg_labels = ax.get_legend_handles_labels()
    leg_handles = [leg_handles[i] for i in legend_order]
    leg_labels = [leg_labels[i] for i in legend_order]

    leg = plt.legend(leg_handles, leg_labels, loc=2, bbox_to_anchor=(1,1), prop={'family':'Arial', 'size':10}, handletextpad=0.3)
    for line in leg.get_lines():
        line.set_linewidth(3.0)
    fig = plt.gcf()
    fig.set_size_inches(6,4)
    plt.savefig(fig_label + '_PercentSelfReferences_vs_NumReferences_Medians.tif', bbox_inches='tight', dpi=600)
    plt.close()
    

def calc_rollingmeans_of_medians(df, journal_arg, window_size):

    gap_size = 10
    
    plotting_df = {'Value':[],
                'Total References':[],
                'Category':[],
                'Journal':[]}
                
    df = pd.DataFrame.from_dict(df)
    label_set = set(df['Journal'])
    
    output = open('Summarized_TableS4_PercentSelfReferences_by_TotalReferences.tsv', 'w')
    output.write('\t'.join(['', '', '', 'Total References --->']) + '\n')
    output.write('\t'.join(['Journal', 'Quartile', 'Data Range (minimum, maximum)'] + [str(x) for x in range(20, 251)]) + '\n')

    for journal in label_set:
        temp_df = df[df['Journal'] == journal]
        yval_list = list(temp_df['Percent Self-References'])
        xval_list = list(temp_df['Total References'])

        max_xval = max([x for x in xval_list if xval_list.count(x) >= 3])
        min_xval = min(xval_list)
        xval_range = [x for x in range(min_xval, max_xval)]

        # IN ORDER: [q1, median, q3]
        quartile_lists = [[], [], []]
        final_xvals = []
        
        latest_xval = xval_range[0]
        
        for xval in xval_range:
            yvals = [y for i, y in enumerate(yval_list) if xval_list[i] == xval]
            
            # LIMITS PLOTTING TO ONLY CALCULATING/INCLUDING MEDIAN IF THERE ARE 3 OR MORE DATA POINTS.
            if len(yvals) < 3:
                continue
                
            # STOPS RUNNING THIS LOOP WHEN A GAP LARGER THAN THE gap_size IS ENCOUNTERED
            if xval - latest_xval > gap_size:
                break
                
            scores_at_percentiles = scoreatpercentile(yvals, [25, 50, 75])

            for i, score in enumerate(scores_at_percentiles):
                quartile_lists[i].append(score)
                
            final_xvals.append(xval)
            latest_xval = xval
                
        labels = ['25th Percentile', '50th Percentile', '75th Percentile']
        for i, quartile_list in enumerate(quartile_lists):
            label = labels[i]
            vals = pd.Series(quartile_list)
            rolling_meanvals = list( vals.rolling(window_size, min_periods=math.ceil(window_size/2), center=True).mean() )

            new_xval_range = [x for x in range(20, max(final_xvals))]
            interpolated_rolling_meanvals = list( np.interp(new_xval_range, final_xvals, rolling_meanvals) )

            plotting_df['Value'] += interpolated_rolling_meanvals
            plotting_df['Total References'] += new_xval_range
            plotting_df['Category'] += [label] * len(interpolated_rolling_meanvals)
            plotting_df['Journal'] += [journal_df[journal]] * len(interpolated_rolling_meanvals)
            
            range_min = min(interpolated_rolling_meanvals)
            range_max = max(interpolated_rolling_meanvals)
            
            range_str = '(' + str(round(range_min, 2)) + ', ' + str(round(range_max, 2)) + ')'
            
            output.write('\t'.join([journal, label, range_str] + [str(round(x, 2)) for x in interpolated_rolling_meanvals]) + '\n')

    output.close()
    
    return plotting_df
    

def subplots(df, fig_label):

    colors = ['#95e084', '#42ab2a', '#215515']     # GREEN SHADES

    df = pd.DataFrame.from_dict(df)
    df = df[df['Total References'] <= 200]  # RESTRICT PLOTTING TO A MAXIMUM OF 200 TOTAL REFERENCES FOR MAIN MANUSCRIPT FIGURE
    fig, axes = plt.subplots(4,4,sharex=True, sharey=True, figsize=(8,8))

    big_subplot = fig.add_subplot(111)
    big_subplot.spines['top'].set_color('none')
    big_subplot.spines['bottom'].set_color('none')
    big_subplot.spines['left'].set_color('none')
    big_subplot.spines['right'].set_color('none')
    big_subplot.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
        
    label_set = []

    journal_order = ['PLOS Biology', 'Current Biology', 'PLOS Genetics', 'Genetics',  'PLOS Pathogens', 'mBio', 'PLOS Medicine', 'BMC Medicine', 'PLOS Comput Biol', 'Bioinformatics', 'Cell', 'Nature', 'Science', 'Mol and Cell Biol', 'J Cell Biology']
    for index, journal in enumerate(journal_order + ['All Publications']):
        ax = plt.subplot(4,4, index+1)
        temp_df = df[df['Journal'] == journal]

        sns.lineplot(x='Total References', y='Value', data=temp_df, hue='Category', palette=colors, linewidth=2)
        
        cat_vals = list(temp_df['Category'])

        q1_vals = [val for i, val in enumerate(temp_df['Value']) if cat_vals[i] == '25th Percentile']
        q3_vals = [val for i, val in enumerate(temp_df['Value']) if cat_vals[i] == '75th Percentile']
        xvals = [xval for i, xval in enumerate(temp_df['Total References']) if cat_vals[i] == '75th Percentile']
        
        ax.fill_between(xvals, q1_vals, q3_vals, color='#42ab2a', alpha=0.2)

        plt.yticks(fontname='Arial', fontsize=12)

        plt.xticks([20, 50, 100, 150, 200], labels=['20', '50', '100', '150', '200'], fontname='Arial', fontsize=12)

        plt.ylim(0, 28)
        plt.xlim(15, 203)
        plt.xlabel('')
        plt.ylabel('')

        ax.text(.5, .9, journal,
            horizontalalignment='center',
            transform=ax.transAxes, fontname='Arial', fontsize=12)
        ax.get_legend().remove()
    
    fig.text(-0.025, 0.5, 'Percent Self-References', va='center', rotation='vertical', fontname='Arial', fontsize=16)
    fig.text(0.5, -0.02, 'Total Number of References', ha='center', fontname='Arial', fontsize=16)
    plt.tight_layout(pad=0.2)
    plt.savefig(fig_label + '_PercentSelfReferences_vs_NumReferences_JournalSubplots.tif', bbox_inches ='tight', dpi=600)
    plt.close()  


if __name__ == '__main__':
    main()
