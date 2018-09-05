import json
import os
import io

def jsonEditor(wantMessagesSigned,wantAssertionsSigned,signMetadata,validMessage,validAssertion,cve201711427):

    filename = 'saml/advanced_settings.json'
    # Read JSON file
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

    # Read JSON file
    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_file.close()

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

def complaintReader():
    complaintFilename = 'complaints/complaints.json'

    with open(complaintFilename) as complaint_file:
        complaint_loaded = json.load(complaint_file)
        complaintDescription = complaint_loaded['description']
        complaintComplainer = complaint_loaded['complainer']
        complaintSeverity = complaint_loaded['severity']
    complaint_file.close()
	
    complaintValues = {'complaintDescription':str(complaintDescription),'complaintComplainer':str(complaintComplainer),'complaintSeverity':str(complaintSeverity)}
    return complaintValues
    