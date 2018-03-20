import json
import os
import io

def jsonEditor(wantMessagesSigned,wantAssertionsSigned,signMetadata,validMessage,validAssertion):

    filename = 'saml/advanced_settings.json'

    '''with open(filename, 'w+') as f:
        data = json.load(f)
        print(data['security']['wantMessagesSigned'])
        print(data['security']['wantAssertionsSigned'])

        data['security']['wantMessagesSigned'] = "True"
        print(data['security']['wantMessagesSigned'])

        f.write(json.dumps(data))
        f.close()'''



    # Read JSON file
    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_file.close()
    #print(data_loaded)
    #print(data_loaded['security']['wantMessagesSigned'])


    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_loaded['security']['wantMessagesSigned'] = wantMessagesSigned
        data_loaded['security']['wantAssertionsSigned'] = wantAssertionsSigned
        data_loaded['security']['signMetadata'] = signMetadata
	data_loaded['security']['wantValidMessageSignature'] = validMessage
	data_loaded['security']['wantValidAssertionsSignature'] = validAssertion
        print(data_loaded['security']['wantMessagesSigned'])
        data_file.close()

    with open(filename, 'w') as file:
        json.dump(data_loaded, file, indent=2)
    data_file.close()

    # Read JSON file
    with open(filename) as data_file:
        data_loaded = json.load(data_file)
        data_file.close()
    print(data_loaded)
    #print(data_loaded['security']['wantMessagesSigned'])

def jsonReader():
    filename = 'saml/advanced_settings.json'

    with open(filename) as data_file:
	data_loaded = json.load(data_file)
        wantMessagesSigned = data_loaded['security']['wantMessagesSigned']
	wantAssertionsSigned = data_loaded['security']['wantAssertionsSigned']
	signMetadata = data_loaded['security']['signMetadata']
	validMessage = data_loaded['security']['wantValidMessageSignature']
	validAssertion = data_loaded['security']['wantValidAssertionsSignature']
        print(str(wantMessagesSigned))
    data_file.close()
	
    settingValues = {'wantMessagesSigned':str(wantMessagesSigned),'wantAssertionsSigned':str(wantAssertionsSigned),'signMetadata':str(signMetadata),'validMessage':str(validMessage),'validAssertion':str(validAssertion)}
    return settingValues
