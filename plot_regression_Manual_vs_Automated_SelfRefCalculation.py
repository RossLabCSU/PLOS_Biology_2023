
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    h = open('TableS2_RandomlyChosenPublications_ManualValidation.tsv')
    header = h.readline()
    
    manual_vals = []
    automated_vals = []
    for line in h:
        items = line.rstrip().split('\t')

        automated_perc = int(items[6]) / int(items[7]) *100
        manual_perc = int(items[9]) / int(items[10]) *100
        
        automated_vals.append(automated_perc)
        manual_vals.append(manual_perc)
        
    h.close()
    
    plotting(manual_vals, automated_vals)
    
    
def plotting(manual_vals, automated_vals):

    ax = sns.regplot(x=automated_vals, y=manual_vals, color='#4C8055', scatter_kws={'alpha':0.5})

    automated_vals = sm.add_constant(automated_vals)
    model = sm.OLS(manual_vals,automated_vals)
    results = model.fit()

    coeff, slope = results.params
    rsquared = results.rsquared
    pvals = results.pvalues
    
    text_str = 'Slope='+str(round(slope, 2)) + '\n$R^2$='+str(round(rsquared, 3))
    plt.text(0.9, 0.9, text_str, ha='right', transform = ax.transAxes, fontname='Arial', fontsize=12)
    
    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Percent Self-References,\nAutomated PubMed Queries', fontname='Arial', fontsize=14)
    plt.ylabel('Percent Self-References,\nManual Calculation', fontname='Arial', fontsize=14)

    plt.savefig('FigS1_Automated_vs_Manual_PercentSelfReferences_Regression.tif', bbox_inches='tight', dpi=600)
    plt.close()
        

if __name__ == '__main__':
    main()
