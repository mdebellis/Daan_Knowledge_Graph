from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
# import xml.xsdatatypes as xsi

conn = ag_connect('minitest', host='localhost', port='10035',
                  user='test', password='xyzzy')
ngostr = 'http://www.semanticweb.org/mdebe/ontologies/NGO#'
ngo_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient')
sdg_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGGoal')
sdg_desc_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#goalDescription')
sdg_statements = conn.getStatements(None, RDF.TYPE, sdg_class)
ngo_statements = conn.getStatements(None, RDF.TYPE, ngo_class)
ngo_num = len(ngo_statements)
sdg_num = len(sdg_statements)
score_array = np.zeros([sdg_num,ngo_num],float)
alignment_index_property = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#sdgAlignmentIndex')
stop_words1 = {'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
stop_words2 = {'Goal','Target', 'Indicator', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.'}
all_stop_words = stop_words1.union(stop_words2)
sample_string = 'Elimninate poverty on now'
sample_string_list = sample_string.split()
sample_string_set = set(sample_string_list)
sample_set_no_stops = sample_string_set.difference(all_stop_words)
sdg1 = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#No_Poverty')
description_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#description')
mission_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement')
vision_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#vision')
objective_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives')
conn.createFreeTextIndex("NGO-INDEX", predicates=[description_prop,mission_prop,vision_prop,objective_prop], stopWords=all_stop_words)

def get_value(ind, prop):
    # Returns the property value for a property that is functional
    statements = conn.getStatements(ind, prop, None)
    if len(statements) > 1:
        print(f"Error get_value called for individual {ind} on multi-valued property {prop} returning first value")
    with statements:
        for statement in statements:
            return statement[2]



def processor(sdg):
    sdg_description_set = {""}
    sdg_description = conn.getStatements(sdg, sdg_desc_prop, None)
    with sdg_description:
        for statement in sdg_description:
            # print(statement)
            sdg_description_str = str(statement[2])
            # print(sdg_description_str)
            sdg_description_list = sdg_description_str.split()
            # print(sdg_description_list)
            for word in sdg_description_list:
                sdg_description_set.add(word.strip('"'))
            sdg_description_set.remove("")
            sdg_description_set = list(sdg_description_set.difference(all_stop_words))
            return sdg_description_set
    return []
            
def calcMatch(words):
    count = 1
    data = {}
    for word in words:
        log = []
        for triple in conn.evalFreeTextSearch(word):
            ngo = triple[0][1:len(triple[0])-1]
            count += 1
            if ngo not in log:
                if ngo in data:
                    data[ngo] += 1
                else:
                    data[ngo] = 1
                log.append(ngo)
                
    for key in data:    
        data[key] /=  len(words)

    # print(count)
    return data
                    

allData = []
allSDG = []
for s in sdg_statements:
    allData.append(calcMatch(processor(s[0])))
    allSDG.append(s[0])

df = pd.DataFrame(allData, index=allSDG)
df1 = df.T #switch columns and rows
# df1 = df1.dropna()
# print(stats.shapiro(df1.iloc[:,0].fillna(0)))
# print(stats.shapiro(df1.iloc[:,1].fillna(0)))
# print(stats.shapiro(df1.iloc[:,2].fillna(0)))
# print(stats.shapiro(df1.iloc[:,3].fillna(0)))
# print(stats.shapiro(df1.iloc[:,4].fillna(0)))
# print(stats.shapiro(df1.iloc[:,5].fillna(0)))
# print(stats.shapiro(df1.iloc[:,6].fillna(0)))
# print(stats.shapiro(df1.iloc[:,7].fillna(0)))
# print(stats.shapiro(df1.iloc[:,8].fillna(0)))
# print(stats.shapiro(df1.iloc[:,9].fillna(0)))
# print(stats.shapiro(df1.iloc[:,10].fillna(0)))
# print(stats.shapiro(df1.iloc[:,11].fillna(0)))
# print(stats.shapiro(df1.iloc[:,12].fillna(0)))
# print(stats.shapiro(df1.iloc[:,13].fillna(0)))
df['mean'] = df.mean(axis=1)
df['max'] = df.max(axis=1)
df['std'] = df.std(axis=1)
df['count'] = df.count(axis=1)
print(df[['mean','max','std', 'count']])
for s in range(len(allSDG)):
    print(s)
    print(df1[allSDG[s]].value_counts())
    
sns.histplot(data=df1[allSDG[6]], bins = 20)
plt.show()


# calcMatch(count_sdg_hits(sdg1))
