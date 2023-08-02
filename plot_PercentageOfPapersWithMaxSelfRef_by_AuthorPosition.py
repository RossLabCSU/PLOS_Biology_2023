
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

def main():

    minimum_references = 20
    num_lastauthors_threshold = 5

    minimum_num_authors_list = [3, (10, 20), (20, 30), (30, 40), (40, 51)]
    minimum_num_authors_list = minimum_num_authors_list[::-1]

    categories = ['1-3', '4-9', '10-19', '20-29', '30-39', '40-50']
    categories = categories[::-1]
    plotting_df = {'Percent Self-References':[],
                    'Category':[],
                    'Author Position':[]}
                    
    df = {cat:{i+1:0 for i in range(num_lastauthors_threshold)} for cat in categories}
    for cat in categories:
        df[cat]['>5'] = 0
        df[cat]['First Author'] = 0
    colors = sns.color_palette('pastel')
    
    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    
    header = h.readline()
    
    vals = []
    
    for line in h:
        journal, pmid, authors, num_selfrefs, perc_selfrefs, max_author, num_selfrefs_maxauthor, total_refs, perc_selfrefs_maxauthor = line.rstrip().split('\t')
        
        total_refs = int(total_refs)
        if total_refs < minimum_references:
            continue
        
        num_selfrefs = num_selfrefs.split(';')
        num_selfrefs = [int(x) for x in num_selfrefs]
        num_selfrefs = num_selfrefs[::-1]
        
        num_selfrefs_maxauthor = int(num_selfrefs_maxauthor)
        num_authors = len(num_selfrefs)
        
        # NOTE THAT, IN CASES OF TIES, THIS GETS ONLY THE FIRST POSITION THAT THE MAX IS ENCOUNTERED, WHICH IS AS-DESIRED.
        maxauthor_pos = num_selfrefs.index(num_selfrefs_maxauthor) + 1     # ADD 1 TO CHANGE INDEX TO POSITION (I.E. STARTING AT 1 RATHER THAN 0)
        
        if num_authors <= 3:
            cat = '1-3'
        elif 4 <= num_authors < 10:
            cat = '4-9'
        elif 10 <= num_authors < 20:
            cat = '10-19'
        elif 20 <= num_authors < 30:
            cat = '20-29'
        elif 30 <= num_authors < 40:
            cat = '30-39'
        elif 40 <= num_authors < 51:
            cat = '40-50'

        # # CHECKS IF THE FIRST AUTHOR WAS THE MAX AUTHOR
        if maxauthor_pos not in range(num_lastauthors_threshold+1) and maxauthor_pos+1 == num_authors:
            maxauthor_pos = 'First Author'

        if maxauthor_pos == 'First Author' or maxauthor_pos <= num_lastauthors_threshold:
            df[cat][maxauthor_pos] += 1
        elif maxauthor_pos > 5:
            df[cat]['>5'] += 1

    h.close()

    plotting_df = make_plotting_df(df)
    plotting(plotting_df)
    
    
def plotting(df):
    
    colors = sns.color_palette('pastel')

    sns.barplot(x='Author Position', y='Percent of Publications', data=df, hue='Category', palette=colors, saturation=1, edgecolor='0.5')

    labels = ['Last', '2nd to Last', '3rd to Last', '4th to Last', '5th to Last', '>5th to Last\n(cumulative)', 'First\nAuthor']
    plt.xticks([x for x in range(max(df['Author Position']))], labels=labels, fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Position of the Max.\nSelf-Referencing Author', fontname='Arial', fontsize=12)
    plt.ylabel('Percentage of Publications', fontname='Arial', fontsize=12)

    fig = plt.gcf()
    fig.set_size_inches(9, 4)
    
    leg = plt.legend(title='Total Number\nof Authors', prop={'family':'Arial'}, handletextpad=0.3)

    plt.setp(leg.get_title(), multialignment='center')
    
    plt.savefig('Fig4A_PercentageOfPapersWithMaxSelfRef_by_AuthorPosition.tif', bbox_inches='tight', dpi=600)
    plt.close()


def make_plotting_df(df):

    plotting_df = {'Percent of Publications':[],
                    'Category':[],
                    'Author Position':[]}
    for cat in df:
        total_papers = sum([df[cat][key] for key in df[cat]])
        for author_pos in df[cat]:
            perc = df[cat][author_pos] / total_papers *100
            if author_pos == '>5':
                author_pos = 6
            elif author_pos == 'First Author':
                author_pos = 7
            plotting_df['Percent of Publications'].append(perc)
            plotting_df['Category'].append(cat)
            plotting_df['Author Position'].append(author_pos)
            
    return plotting_df

    
if __name__ == '__main__':
    main()
