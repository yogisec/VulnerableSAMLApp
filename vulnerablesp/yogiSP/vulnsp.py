from __future__ import print_function
import os
import sys
import json
import time
import random
from shutil import copyfile

from flask import (Flask, request, render_template, redirect, session,
                   make_response)

from urlparse import urlparse

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils


## Import all of the complaint functions functions
from jsonparse import jsonComplaintWriter
from jsonparse import jsonComplaintReader
from jsonparse import jsonSingleComplaintDelete

## Import functions for the 'settings' page
from jsonparse import jsonEditor
from jsonparse import jsonReader

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'onelogindemopytoolkit'
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saml')


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth


def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'query_string': request.query_string
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in request.args:
        return redirect(auth.login())
    elif 'sso2' in request.args:
        return_to = '%sprofile/' % request.host_url
        return redirect(auth.login(return_to))
    elif 'slo' in request.args:
        name_id = None
        session_index = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']

        return redirect(auth.logout(name_id=name_id, session_index=session_index))
    elif 'acs' in request.args:
        auth.process_response()
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                return redirect(auth.redirect_to(request.form['RelayState']))
    elif 'sls' in request.args:
        dscb = lambda: session.clear()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                success_slo = True

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    return render_template(
        'index.html',
        errors=errors,
        not_auth_warn=not_auth_warn,
        success_slo=success_slo,
        attributes=attributes,
        paint_logout=paint_logout
    )

#### Page loads the users profile information
@app.route('/profile/')
def profile():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
    return render_template('profile.html', paint_logout=paint_logout,
                           attributes=attributes)

#### Application meta data for idp
@app.route('/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp

#### Form to Adjust the security levels of the application
@app.route('/settings/')
def settingsPage():
    paint_logout = False
    attributes = False

    #### if the user account isn't a member of the 'PlatformConfiguration' group redirect to the root page
    #### this prevents direct references to the settings page
    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
            print(attributes)
            for attr in attributes:
                if attr[0] == 'memberOf':
                    if attr[1][0] == 'PlatformConfiguration':
                        currentSettings = jsonReader()

                        return render_template('settings.html', paint_logout=paint_logout,
                                attributes=attributes,currentSettings=currentSettings)
    
    return redirect('/')

#### Post action to Adjust the security levels of the application
@app.route('/update', methods=['POST'])
def update():
    attributes = False
    #### check group membership before processing post data if not in the 'PlatformConfiguration' group
    #### redirect to the root page. This prevents direct POST requests to adjust the security of the app
    if 'samlUserdata' in session:
        attributes = session['samlUserdata'].items()
        if len(session['samlUserdata']) > 0:
            for attr in attributes:
                if attr[0] == 'memberOf':
                    if attr[1][0] == 'PlatformConfiguration':
                        wantMessagesSigned = 'wantMessagesSigned' in request.form
                        wantAssertionsSigned = 'wantAssertionsSigned' in request.form
                        signMetadata = 'signMetadata' in request.form
                        validMessage = 'validMessage' in request.form
                        validAssertion = 'validAssertion' in request.form
                        cve201711427 = 'cve-2017-11427' in request.form 
        
                        jsonEditor(wantMessagesSigned,wantAssertionsSigned,signMetadata,validMessage,validAssertion,cve201711427)

                        return redirect('/settings/')
    return redirect('/')

#### Static page that displays helpful information about SAML, terminiology, and resources.
@app.route('/learn/')
def learnPage():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
	    paint_logout = True

    return render_template('learn.html', paint_logout=paint_logout, attributes=attributes)

#### Page that rendors the complaints
@app.route('/complaints/')
def complaints():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
                attributes = session['samlUserdata'].items()
    complaintDic = jsonComplaintReader()
    return render_template('complaints.html', paint_logout=paint_logout,attributes=attributes,dictionary=complaintDic)

#### Form page for taking in complaint details
@app.route('/filecomplaint/')
def filecomplaint():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
	    paint_logout = True

    return render_template('filecomplaint.html', paint_logout=paint_logout, attributes=attributes)

#### Post route that processes the results from the complaint form.
@app.route('/newcomplaint', methods=['POST'])
def newcomplaint():
    complaint = request.form['complaintDescription']
    severity = request.form['severity']
    victim = request.form['victim']
    
    #Generate a 'unique' event id
    complaintID = int(round(time.time() * 1000))
    complaintID = str(complaintID)
    complaintID = ''.join(random.sample(complaintID,len(complaintID)))

    jsonData = {'id':str(complaintID),'description':str(complaint),'complainer':str(victim),'severity':str(severity)}
    jsonComplaintWriter(jsonData)
    return redirect('/complaints/')

### Restore all of the complaints back to the original
@app.route('/restorecomplaints/')
def restoreComplaints():
    if 'samlUserdata' in session:
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
            for attr in attributes:
                if attr[0] == 'memberOf':
                    if attr[1][0] == 'PlatformConfiguration':
                        copyfile('complaints/complaints.json.bak', 'complaints/complaints.json')
            
    return redirect('/complaints/')

### Delete single complaint
@app.route('/deletecomplaint')
def deletecomplaint():
    complaintID = request.args.get('id')
    jsonSingleComplaintDelete(complaintID)
    return redirect('/complaints')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
