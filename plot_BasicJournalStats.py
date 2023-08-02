
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Patch

journal_args = ['PlosPath', 'PlosBiol', 'PlosGenet', 'PlosCompBiol', 'PlosMed', 'Cell', 'Nature', 'Science', 'Genetics', 'Bioinformatics', 'BMCmed', 'mBio', 'MCB', 'JCellBiol', 'CurrBiol']
journal_labels = ['PLOS Pathogens', 'PLOS Biology', 'PLOS Genetics', 'PLOS Computational\nBiology', 'PLOS Medicine', 'Cell', 'Nature', 'Science', 'Genetics', 'Bioinformatics', 'BMC Medicine', 'mBio', 'Molecular and\nCellular Biology', 'J Cell Biology', 'Current Biology']
j_to_jlabel = {journal_arg:journal_labels[i] for i, journal_arg in enumerate(journal_args)}
j_order = ['PLOS Biology', 'PLOS Genetics', 'PLOS Pathogens', 'PLOS Medicine', 'PLOS Computational\nBiology', 'Cell', 'Nature', 'Science', 'Genetics', 'mBio', 'BMC Medicine', 'Bioinformatics', 'Molecular and\nCellular Biology', 'J Cell Biology', 'Current Biology']
    
def main():

    xlocs = {'PLOS Biology':0, 'Current Biology':0,
            'PLOS Genetics':1, 'Genetics':1,
            'PLOS Pathogens':2, 'mBio':2,
            'PLOS Medicine':3, 'BMC Medicine':3,
            'PLOS Computational Biology':4, 'Bioinformatics':4,
            'Molecular and Cellular Biology':5, 'J Cell Biology':6,
            'Cell':7, 'Nature':8, 'Science':9}

    cats = {'PLOS Biology':0, 'Current Biology':1,
            'PLOS Genetics':0, 'Genetics':1,
            'PLOS Pathogens':0, 'mBio':1,
            'PLOS Medicine':0, 'BMC Medicine':1,
            'PLOS Computational Biology':0, 'Bioinformatics':1,
            'Cell':2, 'Nature':2, 'Science':2,
            'Molecular and Cellular Biology':2, 'J Cell Biology':2}

    label_order = ['PLOS Biology', 'PLOS Genetics', 'PLOS Pathogens', 'PLOS Medicine', 'PLOS Comput. Biol.',
            'Current Biology', 'Genetics', 'mBio', 'BMC Medicine', 'Bioinformatics',
            'Molecular and\nCellular Biology', 'J Cell Biology',
            'Cell', 'Nature', 'Science']
                    
    authors_df, refs_df, numpubs_df = get_main_data(cats, xlocs)
    plot_num_pubs(numpubs_df, xlocs, cats, label_order)
    
    IF_df = get_IF_data()
    plot_IFs_main(IF_df, xlocs, cats, label_order)
    plot_IFs_cellnaturescience(IF_df, xlocs, cats, label_order)

    boxplots_TotalRefs_NumAuthors(refs_df, cats, label_order, 'Total Number of References', 'FigS2C', (-5, 135))
    boxplots_TotalRefs_NumAuthors(authors_df, cats, label_order, 'Number of Authors', 'FigS2D', (-2, 35))
    
    
def get_main_data(cats, xlocs):

    authors_df = {'Number of Authors':[],
        'Journal':[],
        'Category':[]}
        
    refs_df = {'Total Number of References':[],
        'Journal':[],
        'Category':[]}
        
    pubs_df = {}
    
    h = open('TableS1_SelfReferencingRate_Estimates.tsv')
    header = h.readline()
    
    for line in h:
        items = line.rstrip().split('\t')
        journal = items[0]
        journal_label = j_to_jlabel[journal]
        pmid = items[1]
        authors = items[2].split(';')
        num_authors = len(authors)
        total_refs = int(items[7])
        
        authors_df['Number of Authors'].append(num_authors)
        authors_df['Journal'].append(xlocs[journal_label.replace('\n', ' ')])
        authors_df['Category'].append(cats[journal_label.replace('\n', ' ')])
        
        refs_df['Total Number of References'].append(total_refs)
        refs_df['Journal'].append(xlocs[journal_label.replace('\n', ' ')])
        refs_df['Category'].append(cats[journal_label.replace('\n', ' ')])
        
        pubs_df[journal_label] = pubs_df.get(journal_label, set())
        pubs_df[journal_label].add(pmid)

    numpubs_df = {'Number of Publications':[],
                'Journal':[]}
        
    for journal_label in pubs_df:
        numpubs = len(pubs_df[journal_label])
        numpubs_df['Number of Publications'].append(numpubs)
        numpubs_df['Journal'].append(journal_label)
        
    return authors_df, refs_df, numpubs_df
    
    
def get_IF_data():

    h = open('JournalImpactFactors.txt')
    h.readline()
    h.readline()
    
    df = {'Journal':[],
        'Impact Factor':[]}
    
    for line in h:
        journal, impact_factor = line.rstrip().split('\t')
        impact_factor = float(impact_factor)
        df['Journal'].append(journal)
        df['Impact Factor'].append(impact_factor)
        
    h.close()
    
    return df
    
    
def plot_num_pubs(df, xlocs, cats, label_order):

    colors = ['#4C8055', '#68A4A5', '#967969']  # GREEN, TEAL, MOCHA
    df['Xposition'] = [xlocs[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]
    df['Categories'] = [cats[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]

    temp_df = pd.DataFrame.from_dict(df)
    df = temp_df[temp_df['Xposition'] < 5]
    
    sns.barplot(x='Xposition', y='Number of Publications', hue='Categories', data=df, palette=colors, order=[x for x in range(5)])

    df = temp_df[temp_df['Xposition'] >= 5]
    xvals, yvals = zip(*sorted(zip(df['Xposition'], df['Number of Publications'])))
    plt.bar(xvals, yvals, color=colors[2], width=0.4)

    label_locs = []
    ax = plt.gca()
    bars = [x for x in ax.patches]
    for i, b in enumerate(bars):
        w,h = b.get_width(), b.get_height()
        x0, y0 = b.xy
        xpos = x0 + (w / 2)
        label_locs.append(xpos)

    ax.set_xticks(label_locs, rotation=90)
    ax.set_xticklabels(label_order)
    
    leg_labels = ['PLOS journal', 'PLOS-paired journal', 'Non-paired journal']
    legend_elements = [Patch(facecolor=colors[i], label=leg_label) for i, leg_label in enumerate(leg_labels)]

    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1,1), handletextpad=0.3, prop={'family':'Arial', 'size':10})
    
    plt.xticks(fontname='Arial', fontsize=12, rotation=90)
    plt.yticks([x for x in range(0, 11000, 1000)], fontname='Arial', fontsize=12)
    plt.xlabel('Journal', fontname='Arial', fontsize=14)
    plt.ylabel('Number of Publications', fontname='Arial', fontsize=14)
    plt.ylim(0, 10900)
    plt.savefig('FigS2A_NumberOfPublications_by_Journal.tif', bbox_inches='tight', dpi=600)
    plt.close()
    

def plot_IFs_main(df, xlocs, cats, label_order):

    colors = ['#4C8055', '#68A4A5', '#967969']  # GREEN, TEAL, MOCHA
    df['Xposition'] = [xlocs[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]
    df['Categories'] = [cats[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]

    temp_df = pd.DataFrame.from_dict(df)
    temp_df = temp_df[temp_df['Xposition'].isin([0, 1, 2, 3, 4, 5, 6])]
    label_order_copy = label_order[:]
    label_order_copy.remove('Cell')
    label_order_copy.remove('Nature')
    label_order_copy.remove('Science')
    
    df = temp_df[temp_df['Xposition'] < 5]
    ax = sns.barplot(x='Xposition', y='Impact Factor', hue='Categories', data=df, palette=colors)

    df = temp_df[temp_df['Xposition'] >= 5]
    ax.bar(df['Xposition'], df['Impact Factor'], color=colors[2], width=0.4)
    
    label_locs = []
    bars = [x for x in ax.patches]
    for i, b in enumerate(bars):
        w,h = b.get_width(), b.get_height()
        x0, y0 = b.xy
        xpos = x0 + (w / 2)
        label_locs.append(xpos)

    ax.set_xticks(label_locs, rotation=90)
    ax.set_xticklabels(label_order_copy)

    leg_labels = ['PLOS journal', 'PLOS-paired journal', 'Non-paired journal']
    legend_elements = [Patch(facecolor=colors[i], label=leg_label) for i, leg_label in enumerate(leg_labels)]

    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1,1), handletextpad=0.3, prop={'family':'Arial', 'size':10})

    plt.xticks(fontname='Arial', fontsize=12, rotation=90)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Journal', fontname='Arial', fontsize=14)
    plt.ylabel('Impact Factor', fontname='Arial', fontsize=14)
    plt.ylim(0, 13)
    fig = plt.gcf()
    fig.set_size_inches(6,5)
    plt.savefig('FigS2B-part1_ImpactFactors_Main.tif', bbox_inches='tight', dpi=600)
    plt.close()
    

def plot_IFs_cellnaturescience(df, xlocs, cats, label_order):

    colors = ['#4C8055', '#68A4A5', '#967969']  # GREEN, TEAL, MOCHA
    df['Xposition'] = [xlocs[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]
    df['Categories'] = [cats[journal.replace('\n', ' ')] for i, journal in enumerate(df['Journal'])]

    temp_df = pd.DataFrame.from_dict(df)
    df = temp_df[temp_df['Xposition'].isin([7, 8, 9])]
    label_order = ['Cell', 'Nature', 'Science']
    
    plt.bar(df['Xposition'], df['Impact Factor'], color=colors[2])
    
    label_locs = []
    ax = plt.gca()
    bars = [x for x in ax.patches]
    for i, b in enumerate(bars):
        w,h = b.get_width(), b.get_height()
        x0, y0 = b.xy
        xpos = x0 + (w / 2)
        label_locs.append(xpos)

    ax.set_xticks(label_locs, rotation=90)
    ax.set_xticklabels(label_order)
    
    plt.xticks(fontname='Arial', fontsize=12, rotation=90)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Journal', fontname='Arial', fontsize=14)
    plt.ylabel('Impact Factor', fontname='Arial', fontsize=14)
    plt.ylim(0, 72)
    fig = plt.gcf()
    fig.set_size_inches(1.5,5)
    plt.savefig('FigS2B-part2_ImpactFactors_CellNatureScience.tif', bbox_inches='tight', dpi=600)
    plt.close()
    
    
def boxplots_TotalRefs_NumAuthors(df, cats, label_order, category, fig_label, xaxis_lims):

    label_order = ['PLOS Biology', 'Current Biology',
        'PLOS Genetics', 'Genetics',
        'PLOS Pathogens', 'mBio',
        'PLOS Medicine', 'BMC Medicine',
        'PLOS Comput. Biol.', 'Bioinformatics',
        'Molecular and\nCellular Biology', 'J Cell Biology',
        'Cell', 'Nature', 'Science']
        
    xlocs = {'PLOS Biology':'0', 'Current Biology':'0',
            'PLOS Genetics':'1', 'Genetics':'1',
            'PLOS Pathogens':'2', 'mBio':'2',
            'PLOS Medicine':'3', 'BMC Medicine':'3',
            'PLOS Computational Biology':'4', 'Bioinformatics':'4',
            'Cell':'7', 'Nature':'8', 'Science':'9',
            'Molecular and Cellular Biology':'5', 'J Cell Biology':'6'}

    colors = ['#4C8055', '#68A4A5', '#967969']  # GREEN, TEAL, MOCHA
    df['Journal'] = [str(x) for x in df['Journal']]
    temp_df = pd.DataFrame.from_dict(df)

    df = temp_df[temp_df['Journal'].isin(list('01234'))]
    sns.boxplot(x=category, y='Journal', data=df, hue='Category', showfliers=False, palette=colors)

    df = temp_df[temp_df['Journal'].isin(list('56789'))]
    dummy_rows = {'Journal':list('01234'),
                category:[-1000, -1000, -1000, -1000, -1000],
                'Category':[2,2,2,2,2]}
    dummy_rows = pd.DataFrame.from_dict(dummy_rows)
    df = pd.concat([df, dummy_rows], ignore_index = True)
    sns.boxplot(x=category, y='Journal', order=list('0123456789'), data=df, showfliers=False, palette=[colors[2]], width=0.4)

    ax = plt.gca()

    label_locs = [-0.2, 0.2,
                0.8, 1.2,
                1.8, 2.2,
                2.8, 3.2,
                3.8, 4.2,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0]

    ax.set_yticks(label_locs)
    ax.set_yticklabels(label_order)
    ax.get_legend().remove()

    plt.xlim(xaxis_lims)
    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=10)
    plt.ylabel('Journal', fontname='Arial', fontsize=14)
    plt.xlabel(category, fontname='Arial', fontsize=14)
    fig = plt.gcf()
    fig.set_size_inches(4.5, 6)
    plt.savefig(fig_label + '_' + category.title().replace(' ', '') + '_by_Journal.tif', bbox_inches='tight', dpi=600)
    plt.close()


if __name__ == '__main__':
    main()
