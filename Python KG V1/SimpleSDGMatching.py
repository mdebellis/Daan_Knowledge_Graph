from typing import Dict, Any

from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF

conn = ag_connect('NGO', host='localhost', port='10035',
                  user='mdebellis', password='df1559')
ngostr = 'http://www.semanticweb.org/mdebe/ontologies/NGO#'
ngo_keyword_property = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#keyword')
goal_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGGoal')
target_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGTarget')
csr_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#CSRProgram')
rdf_type = conn.createURI("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
sdg_description = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGGoal')
stop_words1 = {'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
stop_words2 = {'goal','Target', 'Indicator', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.'}
all_stop_words = stop_words1.union(stop_words2)

def get_instances(owl_class):
    # Retrieves the instances for an owl_class
    owl_classes: set = {}
    i_statements = conn.getStatements(None, rdf_type, owl_class)
    for i_statement in i_statements:
        owl_classes.add(i_statement[0])
    return owl_classes

def make_fti_string(kw):
    kw = str(kw)
    kw = kw.replace(" ","*")
    kw = "*" + kw + "*"
    return kw


mission_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement')
vision_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#vision')
objective_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives')
sdg_desc_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#goalDescription')
description_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#description')
has_SDG_goal_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal')
is_SDG_goal_for_prop = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#isSDGGoalFor')
conn.createFreeTextIndex("NGO-INDEX", predicates=[description_prop,mission_prop,vision_prop,objective_prop], stopWords=all_stop_words, wordFilters=["stem.english"])

def create_sdg_links_for_goals():
    print(has_SDG_goal_prop)
    print(is_SDG_goal_for_prop)
    for sdg_statement in conn.getStatements(None, rdf_type, goal_class):
        sdg = sdg_statement[0]
        print(sdg)
        kw_results = conn.getStatements(sdg, ngo_keyword_property, None)
        for kw_result in kw_results:
            kw = kw_result[2]
            kw = make_fti_string(kw)
            for ngo_string_list in conn.evalFreeTextSearch(kw):
                # The FTI returns a list of strings, not IRIs so it is necessary to use createURI to find the actual object
                ngo_str = ngo_string_list[0]
                print(ngo_str)
                ngo = conn.createURI(ngo_str)
                conn.add(ngo, has_SDG_goal_prop, sdg)
                conn.add(sdg, is_SDG_goal_for_prop, ngo)

def create_sdg_links_for_targets():
    print(has_SDG_goal_prop)
    print(is_SDG_goal_for_prop)
    for sdg_statement in conn.getStatements(None, rdf_type, target_class):
        sdg = sdg_statement[0]
        kw_results = conn.getStatements(sdg, ngo_keyword_property, None)
        for kw_result in kw_results:
            kw = kw_result[2]
            kw = make_fti_string(kw)
            for ngo_string_list in conn.evalFreeTextSearch(kw):
                # The FTI returns a list of strings, not IRIs so it is necessary to use createURI to find the actual object
                ngo_str = ngo_string_list[0]
                print(ngo_str)
                ngo = conn.createURI(ngo_str)
                conn.add(ngo, has_SDG_goal_prop, sdg)
                conn.add(sdg, is_SDG_goal_for_prop, ngo)




create_sdg_links_for_targets()

#print(get_instances(goal_class))

