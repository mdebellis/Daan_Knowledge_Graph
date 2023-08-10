from franz.openrdf.connect import ag_connect
from indian_address_parser import PostalAddress

conn = ag_connect('minitest', host='localhost', port='10035',
                  user='test', password='xyzzy')

conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
NGOClass = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient")
state = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state')
city = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#city')
pin = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#pin')
physadd = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#physicalAddress')

query = conn.prepareTupleQuery(query="""
    SELECT * WHERE {?ngoRecipient a ngo:NGORecipient} LIMIT 100 """)



def doQuery(): #returns object of all NGOs
    with query.evaluate() as result:
        return result


def addloc(ngo, pred): # adds the specified state/city/pin to the corresponding ngo
    loc = ''
    territories = ['Andaman and Nicobar Islands', 'NCT of Delhi', 'Puducherry', 'Jammu and Kashmir', 'Lakshadweep', 'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu']
    if pred.getLocalName() == 'state':
        loc = 'states_found'
    elif pred.getLocalName() == 'city':
        loc = 'village_or_citys_found'
    else:
        loc = 'pin_codes_found'
    addy = ''
    for labelstments in conn.getStatements(ngo, physadd, None):
        addy = str(labelstments[2])
    postal_address = PostalAddress(addy).__dict__
    if loc == 'states_found' and len(postal_address[loc]) == 1 and postal_address[loc][0] in territories:
        print('TERRITORY')
        # pred = conn.createURI('')
    # if loc == 'states_found':
        # print(loc, postal_address[loc])
    # print(postal_address[loc], pred.getLocalName())
    if len(postal_address[loc]) == 1:
        conn.add(ngo, pred, postal_address[loc][0])
    return(addy)
    
    
def check(ngo): # checks if there is already a state/city/pin for an ngo, if not calls the addloc functions
    iris = [state, city, pin]
    # print(ngo.getLocalName())
    a = ''
    for pred in iris:
        #print(ngo.getLocalName(), pred.getLocalName())
        contents = []
        for stat in conn.getStatements(ngo, pred, None):
            contents.append(stat[2])
        if contents != []:
            print(" already exists for " + ngo.getLocalName() + " " + pred.getLocalName())
            # conn.remove(ngo, pred, contents[0])
        else:
            a = addloc(ngo,pred)
    # print(a)
 
allNGO = []
for statement in doQuery():
    ngorecip = statement[0]
    allNGO.append(ngorecip)
    # print(ngorecip)
    # for labelstments in conn.getStatements(ngorecip, physadd), None):
    #     print(str(labelstments[2]))   
for n in allNGO:
    check(n)
