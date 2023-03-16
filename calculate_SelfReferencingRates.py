

def main():

    minimum_references = 20
    journals = ['PlosBiol', 'PlosGenet', 'PlosPath', 'PlosMed', 'PlosCompBiol', 'Cell', 'Nature', 'Science', 'Genetics', 'Bioinformatics', 'BMCmed', 'mBio', 'JCellBiol', 'MCB', 'CurrBiol']
    output = open('TableS1_SelfReferencingRate_Estimates.tsv', 'w')
    output.write('\t'.join(['Journal', 'Pubmed ID', 'All Authors (original order)', 'All Authors Number of Self-References', 'All Authors Percentage Self-References', 'Highest Self-Referencing Author', 'Number of Self-References (max. author)', 'Total Number of References (max. author)', 'Percentage Self-References (max. author)']) + '\n')

    for journal in journals:

        df = {}
        df_initials = {}
        
        filename = 'Pubmed_AuthorSearch_' + journal + '.tsv'
        df, df_initials = get_authors(filename, minimum_references, df, df_initials)

        output = calc_selfrefs(df_initials, minimum_references, 'InitialsIncluded', journal, output)

    output.close()

    
def calc_selfrefs(df, minimum_references, include_initials, journal, output):

    max_selfrefs = []
    total_references = []
    max_authors = []
    for pmid in df:
        sorted_authors = df[pmid]['AuthorOrder']
        selfref_vals = [df[pmid][author] for author in sorted_authors]
        max_val = max(selfref_vals)
        max_author = [author for i, author in enumerate(sorted_authors) if selfref_vals[i] == max_val]
        max_author = ';'.join(max_author)
        max_selfrefs.append(max_val)
        total_refs = df[pmid]['TotalReferences']
        total_references.append( total_refs )
        max_authors.append(max_author)
        percs = [str(round(val / total_refs * 100, 2)) for val in selfref_vals]
        max_perc = str( round( max_val / total_refs * 100, 2))
        output.write('\t'.join([journal, pmid, ';'.join(sorted_authors), ';'.join([str(x) for x in selfref_vals]), ';'.join(percs), max_author, str(max_val), str(df[pmid]['TotalReferences']), max_perc]) + '\n')
        
    percents = [max_selfrefs[i] / total_references[i] *100 for i in range(len(max_selfrefs))]
    percents_filtered = [max_selfrefs[i] / total_references[i] *100 for i in range(len(max_selfrefs)) if total_references[i] >= minimum_references]
    max_authors_filtered = [max_authors[i] for i in range(len(max_authors)) if total_references[i] >= minimum_references]
    max_selfrefs_filtered = [max_selfrefs[i] for i in range(len(max_selfrefs)) if total_references[i] >= minimum_references]

    percents_filtered, max_selfrefs_filtered, max_authors_filtered = zip(*sorted(zip(percents_filtered, max_selfrefs_filtered, max_authors_filtered), reverse=True))

    return output

    
def get_authors(filename, minimum_references, df, df_initials):

    h = open(filename)
    header = h.readline()

    for line in h:
        items = line.rstrip().split('\t')
        if len(items) == 1:
            continue
        names = items[1]
        main_pmid = items[0]
        df[main_pmid] = df.get(main_pmid, {'TotalReferences':0})
        df_initials[main_pmid] = df_initials.get(main_pmid, {'TotalReferences':0})
        main_combinednames = items[1].split(';')
        ref_combinednames = items[7].split(';')
        
        df[main_pmid]['AuthorOrder'] = main_combinednames
        df_initials[main_pmid]['AuthorOrder'] = main_combinednames
        
        main_initials = items[4].split(';')
        main_lastnames = items[2].split(';')
        ref_lastnames = items[8].split(';')
        ref_initials = items[10].split(';')

        author_tracking = set()

        for i, author in enumerate(main_combinednames):
            num_selfrefs = 0
            if author in author_tracking:   # PREVENTS DOUBLE-COUNTING IN RARE INSTANCES WHERE TWO AUTHORS HAVE THE EXACT SAME NAME
                continue

            main_init_nospace = main_initials[i] + ' ' + main_lastnames[i]
            main_init_withspace = ' '.join(list(main_initials[i])) + ' ' + main_lastnames[i]
            if main_initials[i] == '':
                main_init_firstinit_only = ''
            else:
                main_init_firstinit_only = main_initials[i][0] + ' ' + main_lastnames[i]
            main_initials_names = [main_init_nospace, main_init_withspace, main_init_firstinit_only]
            df[main_pmid][author] = df[main_pmid].get(author, 0)
            df_initials[main_pmid][author] = df_initials[main_pmid].get(author, 0)
            if author in ref_combinednames:
                df[main_pmid][author] += 1
                df_initials[main_pmid][author] += 1
            elif any([True for init in main_initials_names if init in ref_combinednames]):
                df_initials[main_pmid][author] += 1
                
            author_tracking.add(author)
                
        df[main_pmid]['TotalReferences'] += 1
        df_initials[main_pmid]['TotalReferences'] += 1

        
    h.close()
    
    return df, df_initials
        

if __name__ == '__main__':
    main()
    