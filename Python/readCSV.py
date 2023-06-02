from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import csv
conn = ag_connect('NGO',  host='localhost', port='10035',
                  user='mdebellis', password='df1559')

NGOClass = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient")
ngoIDProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#ngoID")
ngoNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#ngoName")
orgEmailProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#orgEmail")
officePhoneProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#officePhone")
primaryPocProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#primaryPoc")
primaryPocPhoneProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#primaryPocPhone")

secondaryPocProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#secondaryPoc")
secondaryPocPhone = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#secondaryPocPhone")
mailingAddressProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#mailingAddress")
physicalAddressProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#physicalAddress")
fieldOfficesProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#fieldOffices")
orgTypeProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#orgType")

orgWebsiteProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#orgWebsite")
websiteIsValidProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#websiteIsValid")
facebookProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#facebook")
twitterProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#twitter")
instagramProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#instagram")
youtubeProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#youtube")

whatsappProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#whatsapp")
otherSocialsProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#otherSocials")
scrapeSourceProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#scrapeSource")
executiveDirectorProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#executiveDirector")
technicalSupportProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#technicalSupport")
chairmanNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanName")

chairmanMobileProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanMobile")
chairmanEmailProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanEmail")
viceChairmanNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#viceChairmanName")
viceChairmanMobileProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#viceChairmanMobile")
viceChairmanEmailProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#viceChairmanEmail")
secretaryNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#secretaryName")
secretaryMobileProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#secretaryMobile")
secretaryEmailProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#secretaryEmail")
assistantSecretaryNameProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#assistantSecretaryName")

assistantSecretaryMobileProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#assistantSecretaryMobile")
assistantSecretaryEmailProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#assistantSecretaryEmail")
ngoTypeProp = conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#ngoType")


with open('NgoContact_final.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    row_count = 0
    i = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            row_count = len(row)
            print(f'Length of header is: {row_count}')
            line_count += 1
        else:
            NewNGOString = "http://www.semanticweb.org/mdebe/ontologies/NGO#NGO" + str(line_count)
            ngoID = row[0]
            ngoName = row[1]
            orgEmail = row[2]
            officePhone = row[3]
            primaryPoc = row[4]
            primaryPocPhone = row[5]
            secondaryPoc = row[6]
            secondaryPocPhone = row[7]
            mailingAddress = row[8]
            physicalAddress = row[8]
            fieldOffices = row[10]
            orgType = row[11]
            orgWebsite = row[12]
            websiteIsValid = row[13]
            facebook = row[14]
            twitter = row[15]
            instagram = row[16]
            youtube = row[17]
            whatsapp = row[18]
            otherSocials = row[19]
            scrapeSource = row[20]
            executiveDirector = row[21]
            technicalSupport = row[22]
            chairmanName = row[23]
            chairmanMobile = row[24]
            chairmanEmail = row[25]
            viceChairmanName = row[26]
            viceChairmanMobile = row[27]
            viceChairmanEmail = row[28]
            secretaryName = row[29]
            secretaryMobile = row[30]
            secretaryEmail = row[31]
            assistantSecretaryName = row[32]
            assistantSecretaryMobile = row[33]
            assistantSecretaryEmail = row[34]
            ngoType = row[35]
            NewNGO = conn.createURI(NewNGOString)
            conn.add(NewNGO, RDF.TYPE, NGOClass)
            if ngoID != "":
                conn.add(NewNGO, ngoIDProp, ngoID)
            if ngoName != "":
                conn.add(NewNGO, ngoNameProp, ngoName)
            if orgEmail != "":
                conn.add(NewNGO, orgEmailProp, orgEmail)
            if ngoName != "":
                conn.add(NewNGO, ngoNameProp, ngoName)
            if officePhone != "":
                conn.add(NewNGO, officePhoneProp, officePhone)

            if primaryPoc != "":
                conn.add(NewNGO, primaryPocProp, primaryPoc)
            if primaryPocPhone != "":
                conn.add(NewNGO, primaryPocPhoneProp, primaryPocPhone)
            if secondaryPoc != "":
                conn.add(NewNGO, secondaryPocProp, secondaryPoc)
            if secondaryPocPhone != "":
                conn.add(NewNGO, secondaryPocPhoneProp, secondaryPocPhone)
            if mailingAddress != "":
                conn.add(NewNGO, mailingAddressProp, mailingAddress)

            if physicalAddress != "":
                conn.add(NewNGO, physicalAddressProp, physicalAddress)
            if fieldOffices != "":
                conn.add(NewNGO, fieldOfficesProp, fieldOffices)
            if orgType != "":
                conn.add(NewNGO, orgTypeProp, orgType)
            if orgWebsite != "":
                conn.add(NewNGO, orgWebsiteProp, orgWebsite)
            if websiteIsValid != "":
                conn.add(NewNGO, websiteIsValidProp, websiteIsValid)

            if facebook != "":
                conn.add(NewNGO, facebookProp, facebook)
            if twitter != "":
                conn.add(NewNGO, twitterProp, twitter)
            if instagram != "":
                conn.add(NewNGO, instagramProp, instagram)
            if youtube != "":
                conn.add(NewNGO, youtubeProp, youtube)
            if whatsapp != "":
                conn.add(NewNGO, whatsappProp, whatsapp)

            if otherSocials != "":
                conn.add(NewNGO, otherSocialsProp, otherSocials)
            if scrapeSource != "":
                conn.add(NewNGO, scrapeSourceProp, scrapeSource)
            if executiveDirector != "":
                conn.add(NewNGO, executiveDirectorProp, executiveDirector)
            if technicalSupport != "":
                conn.add(NewNGO, technicalSupportProp, technicalSupport)
            if chairmanName != "":
                conn.add(NewNGO, chairmanNameProp, chairmanName)

            if chairmanMobile != "":
                conn.add(NewNGO, chairmanMobileProp, chairmanMobile)
            if chairmanEmail != "":
                conn.add(NewNGO, chairmanEmailProp, chairmanEmail)
            if viceChairmanName != "":
                conn.add(NewNGO, viceChairmanNameProp, viceChairmanName)
            if viceChairmanMobile != "":
                conn.add(NewNGO, viceChairmanMobileProp, viceChairmanMobile)
            if viceChairmanEmail != "":
                conn.add(NewNGO, viceChairmanEmailProp, viceChairmanEmail)

            if secretaryName != "":
                conn.add(NewNGO, secretaryNameProp, secretaryName)
            if secretaryMobile != "":
                conn.add(NewNGO, secretaryMobileProp, secretaryMobile)
            if secretaryEmail != "":
                conn.add(NewNGO, secretaryEmailProp, secretaryEmail)
            if assistantSecretaryName != "":
                conn.add(NewNGO, assistantSecretaryNameProp, assistantSecretaryName)
            if assistantSecretaryMobile != "":
                conn.add(NewNGO, assistantSecretaryMobileProp, assistantSecretaryMobile)
            if ngoType != "":
                conn.add(NewNGO, ngoTypeProp, ngoType)

            print(f'New NGO: {NewNGOString} ')

            line_count += 1
    print(f'Processed {line_count} lines.')
