Vulnerable SAML infrastructure.

A high level getting started guide is below, if you would like a more detailed guide, that covers the app, features, settings, and walkthroughs please check out:

- [Application Overview and Walkthrough](https://jellyparks.com/Web_Things/vulnerable_saml_app.html)
- [SAML Refresher](https://jellyparks.com/Web_Things/saml_overview.html)

The purpose of these applications is to showcase how certain vulnerable configurations can be exploited to allow a user to change there permissions, name, etc. within an application. OneLogins python SAML library was utilized for this. In order for some of these vulnerable configurations to work the library was heavily modified.

This configuration contains two docker images. The `vulnerableidp` is an identity provider. It contains a 'database' with a few different users.

To spin up these docker images is fairly easy. Just run:

```
docker-compose up
```

The images will build and then the web application will be hosted at http://127.0.0.1:8000

## Login Credentials

To login as an unpriviledged user:
  ```
  Username: yogi
  Password: bear
  ```

Admin user:
  ```
  Username: admin
  Password: this-is-the-administrator-pasword-oh-no-is-that-a-typo-in-password
  ```

User accout for CVE2017-11427
  ```
  Username: brubble
  Password: password
  ```

Instructor user that can adjust security levels:
  ```
  Username: instructor
  Password: G0od-LuckGu3ssingThisButHeyItCouldHappenRight?
  ```

To upgrade privileges after logging in as the 'yogi' user change the group membership in the SAML message from 'users' to 'admin'

If you'd like to change the user accounts, or the groups around edit the `vulnerableidp/authsources.php` file. All user accounts are statically assigned and created within that file.


## Splitting the Deployment to Multiple Hosts:

Want to set this up on seperate servers or point to an address that isn't localhost? A couple of changes need to be made before you build the images first. **The easiest thing to do is to run the configure_platform.py as a privileged user and follow the prompts for each of the hosts.** If you allow it to run privileged the script will edit the configuration files for you, build the docker images, and launched them for you.

### Want to edit the files manually, continue below:

#### IDP Configuration Changes and Running:

File: `VulnerableSAMLApp/vulnerableidp/saml20-sp-remote.php`

Change:
```
Replace every instance of '127.0.0.1:8000' with the ip of the host hosting the web application.
```

Lets build the Docker image:

```
sudo docker build -t idp:1.0 .
```

Run the container:

```
sudo docker run -it --rm --name idp -d -p 80:80 idp:1.0
```

Confirm container is running:
```
sudo docker ps
```

Output should have something similar to this:
```
189adee1b091  localhost/idp:1.0  apache2ctl -D FOR...  2 seconds ago  Up 2 seconds ago  0.0.0.0:80->80/tcp  idp
```

Confirm idp is listening:

```
curl http://127.0.0.1
```

#### Web Application Configuration Changes and Running:

File: `VulnerableSAMLApp/vulnerablesp/yogiSP/saml/settings.json`

Change: 
```
In the settings.json file within the SP section replace the '127.0.0.1:8000' with your web applications ip.
Within the IDP section you'll also need to replace the '127.0.0.1' address with the address of the IDP server.
```

Lets build the Docker image:

```
sudo docker build -t sp:1.0 .
```

Run the container:

```
sudo docker run -it --rm --name sp -d -p 8000:8000 sp:1.0
```

Confirm container is running:
```
sudo docker ps
```

Output should be similar to this:
```
94476aee1abf    sp:1.1    "uwsgi --ini vulnsp.…"   4 minutes ago    Up 4 minutes    0.0.0.0:8000->8000/tcp    sp
```

Confirm web application is listening:

```
curl http://127.0.0.1
```

You should now be able to access the web application on port 8000 and authenticate through the IDP on port 80. Make sure that you have access to both hosts.

## Want to change default security settings?
Before building the container edit the /vulnerablesp/yogiSP/saml/advanced_settings.json file.

Set values to True that you want to have loaded when the application runs. Once these settings are in, build the image and run it.

## TODO: 
- Open User registration
- Config script to make app more portable
- Implement vulnerabilities to allow XSW attacks
- Implement patch for cve-2017-11427 so that the vulnerability can be turned on/off

Shout out to E.D. for initial dockerization of the idp.
