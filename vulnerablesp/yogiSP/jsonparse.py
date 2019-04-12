import csv
import codecs
import io
import random
import json
import time


#### Update the settings stored in the settings file.
#### This is the file that controls the security levels for the application
def jsonEditor(wantMessagesSigned,wantAssertionsSigned,signMetadata,validMessage,validAssertion,cve201711427):

    filename = 'saml/advanced_settings.json'
    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_file.close()

    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_loaded['security']['wantMessagesSigned'] = wantMessagesSigned
        data_loaded['security']['wantAssertionsSigned'] = wantAssertionsSigned
        data_loaded['security']['signMetadata'] = signMetadata
        data_loaded['security']['wantValidMessageSignature'] = validMessage
        data_loaded['security']['wantValidAssertionsSignature'] = validAssertion
        data_loaded['security']['cve-2017-11427'] = cve201711427
        print(data_loaded['security']['wantMessagesSigned'])
    data_file.close()

    with open(filename, 'w') as file:
        json.dump(data_loaded, file, indent=2)
    data_file.close()

    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_file.close()

#### Read in the current settings and display them on the page
def jsonReader():
    filename = 'saml/advanced_settings.json'

    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        wantMessagesSigned = data_loaded['security']['wantMessagesSigned']
        wantAssertionsSigned = data_loaded['security']['wantAssertionsSigned']
        signMetadata = data_loaded['security']['signMetadata']
        validMessage = data_loaded['security']['wantValidMessageSignature']
        validAssertion = data_loaded['security']['wantValidAssertionsSignature']
        cve201711427 = data_loaded['security']['cve-2017-11427']
        print(str(wantMessagesSigned))
    data_file.close()
	
    settingValues = {'wantMessagesSigned':str(wantMessagesSigned),'wantAssertionsSigned':str(wantAssertionsSigned),'signMetadata':str(signMetadata),'validMessage':str(validMessage),'validAssertion':str(validAssertion),'cve-2017-11427':str(cve201711427)}
    return settingValues

#### ---- Everything below this is responsibile for the Complaints page and associated functionality ---- ####

#### Porting from CSV to JSON for greater flexibility.....glen might have been right, this one time
#### Read in all of the current complaints
def jsonComplaintReader():
    complaintFilename = 'complaints/complaints.json'
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
        return data

#### Write a new complaint to the json db file
def jsonComplaintWriter(newComplaint):
    complaintFilename = 'complaints/complaints.json'

    #read in the entire file stick it into a variable
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
    complaint_file.close()

    data.append(newComplaint)
    stringBlob = json.dumps(data)
    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write(stringBlob)

#### Delete 1 entry based on the 'id' number
def jsonSingleComplaintDelete(complaintID):
    complaintFilename = 'complaints/complaints.json'
    
    #read in the entire file stick it into a variable
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
    complaint_file.close()

    for entry in data:
        if entry['id'] == complaintID:
            data.remove(entry)
    
    stringBlob = json.dumps(data)
    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write(stringBlob)