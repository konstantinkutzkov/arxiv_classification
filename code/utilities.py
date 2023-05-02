import json
import os

# Generator that loads the research papers jsons into 
def paper_generator(datapath):
    with open(datapath, 'r') as f:
        for paper in f:
            yield json.loads(paper)
    
# Pairwise random hashing to an integer in [0, 100) using a linear function.
# In order to assure consistency when sampling on different platforms or Python versions.
def pairwise_ind_hash(x):
    return (((7313*x + 601)%1019))%100

# extract the year and month from a string with a given format
def get_year_month(dt):
    try:
        return (int(dt.split('-')[0]), int(dt.split('-')[1]))
    except:
        return (-1,-1)

# from a given paper record, get its abstract and the label category     
def add_abstract_and_labels(paper, abstracts, labels, labelmap, update_map=True):
    abstracts.append(paper['abstract'])
    cats = paper['categories']
    paper_labels = set()
    for j, cat in enumerate(cats.split()): 
        cat = cat.split('.')[0]
        if update_map:
            labelmap.setdefault(cat, len(labelmap))
        paper_labels.add(labelmap.get(cat, len(labelmap)))
    labels.append(list(paper_labels))

    
# iterate over the dataset, sample papers for a given time period and get the corresponding abstract and labels
def get_data_and_labels(datapath, year, month_start, month_end, labelmap, update_map, sample_rate):
    abstracts = []
    labels = []
    for i, paper in enumerate(paper_generator(datapath)):
        if i % 500000 == 0:
            print('# processed papers', i)
        if pairwise_ind_hash(i) >= sample_rate: # sampling 10% of the papers
            continue
        yr, mn = get_year_month(paper.get('update_date', ''))
        if yr != year or mn == -1:
            continue
        if mn >= month_start and mn <= month_end:
            add_abstract_and_labels(paper, abstracts, labels, labelmap, update_map)
    assert len(abstracts) == len(labels) 
    return abstracts, labels, labelmap