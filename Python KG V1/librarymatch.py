from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
from fuzzywuzzy import fuzz

# import xml.xsdatatypes as xsi

conn = ag_connect('minitest', host='localhost', port='10035',
                  user='test', password='xyzzy')
ngo_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient')
sdg_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGGoal')
sdg_desc_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#goalDescription')
sdg_statements = conn.getStatements(None, RDF.TYPE, sdg_class)
ngo_statements = conn.getStatements(None, RDF.TYPE, ngo_class)
stop_words1 = {'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
stop_words2 = {'goal','Target', 'Indicator', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.'}
all_stop_words = stop_words1.union(stop_words2)
description_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#description')
mission_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement')
vision_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#vision')
objective_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives')
conn.createFreeTextIndex("NGO-INDEX", predicates=[description_prop,mission_prop,vision_prop,objective_prop], stopWords=all_stop_words)


def processor(sdg):
    sdg_description_set = {""}
    sdg_description = conn.getStatements(sdg, sdg_desc_prop, None)
    with sdg_description:
        for statement in sdg_description:
            # print(statement)
            sdg_description_str = str(statement[2])
            sdg_description_str = sdg_description_str.replace(',', '').lower()
            # print(sdg_description_str)
            sdg_description_list = sdg_description_str.split()
            # print(sdg_description_list)
            for word in sdg_description_list:
                sdg_description_set.add(word.strip('"'))
            sdg_description_set.remove("")
            sdg_description_set = list(sdg_description_set.difference(all_stop_words))
            return " ".join(sdg_description_set)
    return []
            
def calcMatch(words, sdg):
    t = ''
    count = 0
    for n in ngo_statements:
        t = ''
        for text in conn.getStatements(n[0], description_prop, None):
            t += str(text[2])[1:len(str(text[2]))-1] + ' '
        for text in conn.getStatements(n[0], mission_prop, None):
            t += str(text[2])[1:len(str(text[2]))-1]+ ' '
        for text in conn.getStatements(n[0], vision_prop, None):
            t += str(text[2])[1:len(str(text[2]))-1]+ ' '
        for text in conn.getStatements(n[0], objective_prop, None):
            t += str(text[2])[1:len(str(text[2]))-1]+ ' '
        
        if fuzz.token_set_ratio(t, words) >= 45:
            conn.add(n[0], conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#hasSDGGoal'), sdg)
            count +=1
    return count
                
    

for s in sdg_statements:
    print(s[0], calcMatch(processor(s[0]), s[0]))


