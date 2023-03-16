
def main():

    minimum_references = 20
    journals = ['PlosBiol', 'PlosGenet', 'PlosPath', 'PlosMed', 'PlosCompBiol', 'Cell', 'Nature', 'Science', 'Genetics', 'Bioinformatics', 'BMCmed', 'mBio', 'JCellBiol', 'MCB', 'CurrBiol']

    output = open('TableS6_PubmedSearch_SelfReferencingRate_ProgressiveSelfRefsContributed.tsv', 'w')
    output.write('\t'.join(['Journal', 'Pubmed ID', 'All Authors (original order)', 'All Authors Number of Self-References', 'All Authors Percentage Self-References', 'Highest Self-Referencing Author (most senior author only)', 'Number of Self-References (max. author)', 'Total Number of References (max. author)', 'Percentage Self-References (max. author)']) + '\n')

    for journal in journals:

        df = {}
        df_initials = {}
        
        filename = 'Pubmed_AuthorSearch_' + journal + '.tsv'
        df, df_initials = get_authors(filename, minimum_references, df, df_initials)

        output = calc_selfrefs_progressive_ReverseOrder(df_initials, minimum_references, 'InitialsIncluded', journal, output)

    output.close()

    
def calc_selfrefs_progressive_ReverseOrder(df, minimum_references, include_initials, journal, output):
    max_selfrefs = []
    total_references = []
    max_authors = []
    for pmid in df:
        sorted_authors = df[pmid]['AuthorOrder'][::-1]  # REVERSES AUTHOR LIST TO PROGRESSIVELY ANALYZE STARTING WITH LAST AUTHOR.
        sorted_selfref_pmids = df[pmid]['Self-ref PMIDs'][::-1]
        cumulative_selfref_pmids = []
        num_new_selfrefs_added = []   # REPRESENTS THE NUMBER OF NEW SELF-REFERENCES THAT EACH AUTHOR ADDS (I.E. THOSE NOT ALREADY ENCOUNTERED BY THE PRECEDING AUTHORS). AGAIN THIS IS PERFORMED IN REVERSE ORDER, STARTING WITH THE LAST AUTHOR, THEN THE PENULTIMATE AUTHOR, ETC.
        percent_new_selfrefs_added = []
        total_refs = df[pmid]['TotalReferences']
        for i, author in enumerate(sorted_authors):
            selfref_pmids = sorted_selfref_pmids[i]
            unencountered_selfref_pmids = [x for x in selfref_pmids if x not in cumulative_selfref_pmids]
            
            num_new_selfrefs = len(unencountered_selfref_pmids)
            num_new_selfrefs_added.append( num_new_selfrefs )
            percent_new_selfrefs_added.append( num_new_selfrefs / total_refs * 100 )
            
            cumulative_selfref_pmids += unencountered_selfref_pmids
            
        max_val = max(num_new_selfrefs_added)
        max_perc = str( round( max_val / total_refs * 100, 2))
        percs_str = [str(round(perc, 2)) for perc in percent_new_selfrefs_added[::-1]]  # CHANGES THE ORDER BACK TO ORIGINAL AUTHOR LIST ORDER FOR OUTPUT ONLY
        
        max_author = [author for i, author in enumerate(sorted_authors) if num_new_selfrefs_added[i] == max_val]
        max_author = max_author[0]  # STORE ONLY THE FIRST AUTHOR IN THE REVERSED-ORDER AUTHOR LIST WITH THE HIGHEST VALUE (i.e. THE MOST SENIOR AUTHOR WITH THE MAX VALUE, IN CASE OF TIES).
        max_selfrefs.append(max_val)
        total_references.append( total_refs )
        max_authors.append(max_author)
        
        sorted_authors = sorted_authors[::-1]
        num_new_selfrefs_added = num_new_selfrefs_added[::-1]
        
        output.write('\t'.join([journal, pmid, ';'.join(sorted_authors), ';'.join([str(x) for x in num_new_selfrefs_added]), ';'.join(percs_str), max_author, str(max_val), str(df[pmid]['TotalReferences']), max_perc]) + '\n')

    percents = [max_selfrefs[i] / total_references[i] *100 for i in range(len(max_selfrefs))]
    percents_filtered = [max_selfrefs[i] / total_references[i] *100 for i in range(len(max_selfrefs)) if total_references[i] >= minimum_references]
    max_authors_filtered = [max_authors[i] for i in range(len(max_authors)) if total_references[i] >= minimum_references]
    max_selfrefs_filtered = [max_selfrefs[i] for i in range(len(max_selfrefs)) if total_references[i] >= minimum_references]

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
        main_combinednames = items[1].split(';')
        df[main_pmid] = df.get(main_pmid, {'TotalReferences':0, 'AuthorOrder':main_combinednames, 'Self-ref PMIDs':[[] for i in range(len(main_combinednames))]})
        df_initials[main_pmid] = df_initials.get(main_pmid, {'TotalReferences':0, 'AuthorOrder':main_combinednames, 'Self-ref PMIDs':[[] for i in range(len(main_combinednames))]})

        ref_pmid = items[6]
        ref_combinednames = items[7].split(';')

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
                df[main_pmid]['Self-ref PMIDs'][i].append(ref_pmid)
                df_initials[main_pmid]['Self-ref PMIDs'][i].append(ref_pmid)
            elif any([True for init in main_initials_names if init in ref_combinednames]):
                df_initials[main_pmid][author] += 1
                df_initials[main_pmid]['Self-ref PMIDs'][i].append(ref_pmid)
                
            author_tracking.add(author)

        df[main_pmid]['TotalReferences'] += 1
        df_initials[main_pmid]['TotalReferences'] += 1

        
    h.close()
    
    return df, df_initials
        

if __name__ == '__main__':
    main()
    