
import pandas as pd
from scipy.stats import scoreatpercentile
import numpy as np
import math

def main():

    combined_df = {'Number of Authors':[],
            'Percent Self-References':[],
            'Journal':[]}

    num_authors_df = {}
            
    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()

    minimum_references = 20
    window_size = 11
    missing_pmids = set()

    for line in h:
        journal, pmid, all_authors, num_selfrefs_all, perc_selfrefs_all, max_authors, selfref, totalrefs, perc = line.rstrip().split('\t')
        
        totalrefs = int(totalrefs)
        if int(totalrefs) < minimum_references:
            continue

        perc_selfref = int(selfref) / totalrefs * 100

        all_authors = all_authors.split(';')
        num_authors = len(all_authors)

        combined_df['Number of Authors'].append(num_authors)
        combined_df['Percent Self-References'].append(perc_selfref)
        combined_df['Journal'].append(journal)

        combined_df['Number of Authors'].append(num_authors)
        combined_df['Percent Self-References'].append(perc_selfref)
        combined_df['Journal'].append('All Publications')
        
    h.close()

    calc_rollingmeans_of_medians(combined_df, 'All Publications', window_size)


def calc_rollingmeans_of_medians(df, journal_arg, window_size):

    gap_size = 10

    df = pd.DataFrame.from_dict(df)
    label_set = set(df['Journal'])

    output = open('TableS5_PercentSelfReferences_by_NumAuthors_AllPercentiles.tsv', 'w')
    output.write('\t'.join(['', '', 'Number of Authors --->']) + '\n')
    output.write('\t'.join(['Journal', 'Percentile'] + [str(x) for x in range(1, 101)]) + '\n')

    for journal in label_set:
        temp_df = df[df['Journal'] == journal]
        yval_list = list(temp_df['Percent Self-References'])
        xval_list = list(temp_df['Number of Authors'])

        max_xval = max([x for x in xval_list if xval_list.count(x) >= 3])
        min_xval = min(xval_list)
        xval_range = [x for x in range(min_xval, max_xval)]

        final_xvals = []
        percentilescores_lists = [[] for x in range(1, 101)]
        raw_percentilescores_lists = []
        
        latest_xval = xval_range[0]
        
        for xval in xval_range:
            yvals = [y for i, y in enumerate(yval_list) if xval_list[i] == xval]
            
            # LIMITS PLOTTING TO ONLY CALCULATING/INCLUDING MEDIAN IF THERE ARE 3 OR MORE DATA POINTS.
            if len(yvals) < 3:
                continue
                
            if xval - latest_xval > gap_size:
                break

            scores_at_percentiles = scoreatpercentile(yvals, per=[x for x in range(1,101)])
            
            for i, score in enumerate(scores_at_percentiles):
                percentilescores_lists[i].append(score)
                
            raw_percentilescores_lists.append(scores_at_percentiles)
            final_xvals.append(xval)
            latest_xval = xval
                
        for i, percentilescores_list in enumerate(percentilescores_lists):
            vals = pd.Series(percentilescores_list)
            rolling_meanvals = list( vals.rolling(window_size, min_periods=math.ceil(window_size/2), center=True).mean() )

            new_xval_range = [x for x in range(1, max(final_xvals))]
            interpolated_rolling_meanvals = list( np.interp(new_xval_range, final_xvals, rolling_meanvals) )
            
            no_data_list = ['nd'] * ( 100-len(interpolated_rolling_meanvals) )

            percentile_cat = str(i+1)
            if i+1 == 25:
                percentile_cat += ' (Q1)'
            elif i+1 == 50:
                percentile_cat += ' (Median, Q2)'
            elif i+1 == 75:
                percentile_cat += ' (Q3)'
            elif i+1 == 100:
                percentile_cat += ' (Maximum)'
            output.write('\t'.join([journal, percentile_cat] + [str(round(x, 2)) for x in interpolated_rolling_meanvals] + no_data_list) + '\n')

    output.close()


if __name__ == '__main__':
    main()