from franz.openrdf.connect import ag_connect
conn = ag_connect('NGO', host='localhost', port='10035',
                               user='XXXXXX', password='XXXXXX')
label_prop = conn.createURI('http://www.w3.org/2000/01/rdf-schema#label')

# There is probably a better way to do this but this should work 
# Assuming that each object has a unique rdfs:label which should be true
def find_object(label_string):
    statements = conn.getStatements(None, label_prop, label_string)
    with statements:
        for statement in statements:
            for subject in statement:
                return(subject)


#print(find_object("Gender Equality"))
