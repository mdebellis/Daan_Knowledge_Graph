from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import csv

conn = ag_connect('NGO', host='xxxx', port='xxxxx',
                  user='xxxxxx', password='xxxxx')
ngostr = "http://www.semanticweb.org/mdebe/ontologies/NGO#"


def makeNGOIRIstr (inputstr):
    return ngostr + inputstr

owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
owl_datatype_property = conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty")
ngoIDProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#ngoId")
totalAssets = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#totalAssets")
ngoNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#ngoName")
bpath = "NGOContact_final.csv"
NGOClass = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient")


def findNGO(idstr):
    statements = conn.getStatements(None, ngoIDProp, idstr)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Error two or more Individuals with ngoID: {idstr}')
                return statement[0]
            elif len(statements) == 1:
                print(f'Found NGO with ngoID: {idstr}')
                return statement[0]
            else:
                print(f'No NGO with ngoID: {idstr}')
                return None



# def find_property(prop_str):
#     iri_str = makeNGOIRIstr(prop_str)
#     prop = conn.createURI(iri_str)
#     if conn.getStatements(prop, RDF.TYPE, owl_datatype_property) is not None:
#         return prop
#     else:
#         print(f'Error {prop_str} is not a data property')
#         return None

# Reads a CSV file where the first line is a list of properties
# Each subsequent line is an instance of some class that is the domain for each property
# This function can generalize although for now it assumes that the CSV file contains instances
# of the NGORecpient class. Enhancements: 1) write a function to check that the data property exists
# 2) Find the range of the data property if it exists and coerce the literal into that datatype if the
# data property doesn't exist or the literal can't be coerced signal an error.
def read_csv(path):
    with open(path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        proplist = []
        for row in csv_reader:
            row_count = len(row)
            i = 0
            if line_count == 0:
                # Process the first row of property names. Convert each word to a property and put the
                # property in proplist in the same order so for the subsequent rows, row[i] goes in proplist[i]
                # the first column is the ID property that uniquely identifies each instance and determines if an
                # individual already exists for that row, in which case add the data to that existing individual
                while i < row_count:
                    newpropstr = makeNGOIRIstr(row[i])
                    newprop = ngoIDProp
                    if i > 0:
                        newprop = conn.createURI(newpropstr)
                    proplist.append(newprop)
                    # print(f'Proplist: {proplist}')
                    i += 1
                line_count += 1
                print(f'prop list: {proplist}')
            elif findNGO(row[0]) is not None:
                # For subsequent rows there are two conditions: either the Individual already exists (in which case
                # the fingNGO FTI will find it) that is this condition
                print(f'Found NGO Line {line_count}')
                found_ngo = findNGO(row[0])
                while i < row_count:
                    nextval = row[i]
                    if nextval != "":
                        conn.add(found_ngo, proplist[i], nextval)
                    i += 1
                line_count += 1
            else:
                # If the Individual doesn't exist then it will be created
                print(f'New NGO Line {line_count}')
                new_ngo_iri = conn.createURI(
                    'http://www.semanticweb.org/mdebe/ontologies/NGO#NGO' + str(line_count))
                conn.add(new_ngo_iri, RDF.TYPE, NGOClass)
                conn.add(new_ngo_iri, RDF.TYPE, owl_named_individual)
                print(f'New NGO {new_ngo_iri}')
                while i < row_count:
                    nextval = row[i]
                    if nextval != "":
                        conn.add(new_ngo_iri, proplist[i], nextval)
                    i += 1
                line_count += 1
        print(f'Processed {line_count} lines.')



read_csv(bpath)


# findNGO("NGO200000014")

