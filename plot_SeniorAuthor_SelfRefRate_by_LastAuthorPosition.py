
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

def main():

    minimum_references = 20
    num_lastauthors_threshold = 5
    
    minimum_num_authors_list = [3, (4, 10), (10, 20), (20, 30), (30, 40), (40, 51)]
    minimum_num_authors_list = minimum_num_authors_list[::-1]
    categories = ['1-3', '4-9', '10-19', '20-29', '30-39', '40-50']
    categories = categories[::-1]
    plotting_df = {'Percent Self-References':[],
                    'Category':[],
                    'Author Position':[]}
    colors = sns.color_palette('pastel')

    for cat_index, minimum_num_authors in enumerate(minimum_num_authors_list):
    
        category = categories[cat_index]

        h = open('TableS6_SelfReferencingRate_ProgressiveSelfRefsContributed.tsv')
        
        header = h.readline()

        if minimum_num_authors == 3:
            list_cap = 3
        else:
            list_cap = 5

        plotting_df = {'Percent Self-References':[],
                        'Category':[],
                        'Author Position':[]}

        cats_list = [x for x in range(list_cap)] + [5, 6]

        df = {i:[] for i in cats_list}
        
        for line in h:
            items = line.rstrip().split('\t')
            authors = items[2].split(';')
            num_authors = len(authors)
            
            if minimum_num_authors == 3 and num_authors > minimum_num_authors:
                continue
            elif minimum_num_authors != 3 and (num_authors < minimum_num_authors[0] or num_authors >= minimum_num_authors[1]):
                continue
                
            total_refs = int(items[7])
            if total_refs < minimum_references:
                continue
            num_refs_list = items[3].split(';')
            num_refs_list = [int(x) for x in num_refs_list[::-1]]   # NOTE: REVERSES THE ORDER OF THE LIST SO THAT LAST AUTHORS ARE CONSIDERED FIRST
            first_author_numrefs = num_refs_list[-1]

            if minimum_num_authors == 3:
                num_refs_list = num_refs_list[:list_cap]
            else:
                num_refs_list = num_refs_list[:list_cap] + [sum(num_refs_list[list_cap:])] + [first_author_numrefs]
            
            percs = [x/total_refs*100 for x in num_refs_list]

            for i in range(len(percs)):
                plotting_df['Percent Self-References'].append(percs[i])
                plotting_df['Author Position'].append(i)
                plotting_df['Category'].append(category)
                df[i].append(percs[i])

        h.close()
        
        plotting_df['hue'] = [0 for x in range(len(plotting_df['Percent Self-References']))]

        for i in cats_list:
            for cat in categories:
                plotting_df['Percent Self-References'].append(-1000)
                plotting_df['Author Position'].append(i)
                plotting_df['hue'].append(1)
                plotting_df['Category'].append(cat)

        use_kdeplot = False

        for i in range(7):
            sns.violinplot(x='Percent Self-References', y='Author Position', hue='hue', data=plotting_df, inner=None, palette=[colors[cat_index]], width=1.5, showfliers=False, split=True, cut=0, orient='h', linewidth=0.7, saturation=1, alpha=0.5)  #, order=journal_labels

    ax = plt.gca()
    ax.get_legend().remove()

    legend_elements = [Patch(facecolor=colors[i], edgecolor='0.5', label=categories[i]) for i in range(len(categories))]

    leg = ax.legend(handles=legend_elements, loc=2, bbox_to_anchor=(1,1), handletextpad=0.3, title='Total Number\nof Authors', prop={'family':'Arial'})
    plt.setp(leg.get_title(), multialignment='center')
    
    plt.yticks([x-0.3 for x in range(7)], labels=['Last', '2nd to last', '3rd to last', '4th to last', '5th to last', '>5th to last\n(cumulative)', 'First Author'], fontname='Arial', fontsize=12)
    plt.xlim(0, 50)
    plt.ylim(6.2, -0.9)
    plt.xlabel('Percentage Self-References Added', fontname='Arial', fontsize=14)
    plt.ylabel('Author Position', fontname='Arial', fontsize=14)
    plt.xticks(fontname='Arial', fontsize=12)

    fig = plt.gcf()
    fig.set_size_inches(8,5)
    plt.savefig('Fig4B_SeniorAuthor_SelfRefsContributed_Distributions.tif', bbox_inches='tight', dpi=600, pil_kwargs={'compression':'tiff_lzw'})
    plt.close()
        
        
if __name__ == '__main__':
    main()