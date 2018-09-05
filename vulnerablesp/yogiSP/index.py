from __future__ import print_function
import os
import sys


from flask import (Flask, request, render_template, redirect, session,
                   make_response)

from urlparse import urlparse

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from jsonparse import jsonEditor
from jsonparse import jsonReader
from jsonparse import complaintReader
from csvparse import csvComplaintReader
from csvparse import csvComplaintWriter
from csvparse import csvComplaintDelete
#from customforms import SamlSettings

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
        return_to = '%sattrs/' % request.host_url
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


@app.route('/attrs/')
def attrs():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
    return render_template('attrs.html', paint_logout=paint_logout,
                           attributes=attributes)


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

@app.route('/config/')
def configPage():
    form = SamlSettings()
    return render_template('config.html', form=form)

@app.route('/settings/')
def settingsPage():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
                attributes = session['samlUserdata'].items()

    currentSettings = jsonReader()

    return render_template('settings.html', paint_logout=paint_logout,
			attributes=attributes,currentSettings=currentSettings)

@app.route('/update', methods=['POST'])
def update():
    wantMessagesSigned = 'wantMessagesSigned' in request.form
    wantAssertionsSigned = 'wantAssertionsSigned' in request.form
    signMetadata = 'signMetadata' in request.form
    validMessage = 'validMessage' in request.form
    validAssertion = 'validAssertion' in request.form
    cve201711427 = 'cve-2017-11427' in request.form 
        
    jsonEditor(wantMessagesSigned,wantAssertionsSigned,signMetadata,validMessage,validAssertion,cve201711427)

    return redirect('/settings/')

@app.route('/filecomplaint/')
def filecomplaint():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
	    paint_logout = True

    return render_template('filecomplaint.html', paint_logout=paint_logout, attributes=attributes)

@app.route('/newcomplaint', methods=['POST'])
def newcomplaint():
    complaint = request.form['complaintDescription']
    severity = request.form['severity']
    victim = request.form['victim']
    
    csvData = str(complaint) + ','  + str(severity) + ',' + str(victim)
    csvComplaintWriter(csvData)

    return redirect('/complaints/')

@app.route('/deletecomplaints/')
def deletcomplaints():
    if 'samlUserdata' in session:
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
            for attr in attributes:
                if attr[0] == 'memberOf':
                    if attr[1][0] == 'administrators':
                        csvComplaintDelete()
                if attr[0] == 'username':
                    if attr[1][0] == 'admin':
                        csvComplaintDelete()
            #print(str(attributes), file=sys.stderr)
    return redirect('/complaints/')

@app.route('/learn/')
def learnPage():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
	    paint_logout = True

    return render_template('learn.html', paint_logout=paint_logout, attributes=attributes)

@app.route('/complaints/')
def complaints():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
                attributes = session['samlUserdata'].items()
    complaintDic = csvComplaintReader()

    return render_template('complaints.html', paint_logout=paint_logout,attributes=attributes,complaintDic=complaintDic)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
