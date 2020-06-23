Vulnerable SAML infrastructure.

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
  Password: password
  ```

User accout for CVE2017-11427
  ```
  Username: adminbutnot
  Password: password
  ```

Instructor user that can adjust security levels:
  ```
  Username: instructor
  Password: G0od-LuckGu3ssingThisButHeyItCouldHappenRight?
  ```

To upgrade privileges after logging in as the 'yogi' user change the group membership in the SAML message from 'users' to 'admin'

If you'd like to change the user accounts, or the groups around edit the `vulnerableidp/authsources.php` file. All user accounts are statically assigned and created within that file.


## Splitting the Deployment to multiple hosts:

Want to set this up on seperate servers or point to an address that isn't localhost? A couple of changes need to be made before you build the images first:

### IDP Configuration Changes and Running:

File: `VulnerableSAMLApp/vulnerableidp/saml20-sp-remote.php`

Change:
```
Replace every instance of '127.0.0.1:8000' with the ip of the host hosting the web application ip.
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

Out put should have something similar to this:
```
189adee1b091  localhost/idp:1.0               apache2ctl -D FOR...  2 seconds ago  Up 2 seconds ago  0.0.0.0:80->80/tcp  idp
```

Confirm idp is listening:

```
curl http://127.0.0.1
```

### Web Application Configuration Changes and Running:

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

Confirm web application is listening:

```
curl http://127.0.0.1
```

You should now be able to access the web application on port 8000 and authenticate through the IDP on port 80. Make sure that you have access to both hosts.

## Changing the listening port for the 'yogi' SP application:
To change the port the vulnerable application is listening on:

```
In vulnerablesp/yogiSP/vulnsp.py update the port on the last line.
In vulnerablesp/yogiSP/vulnsp.ini update http = :8000 with the new port.
In the SP Dockerfile change the EXPOSE port to the new port.
You'll also need to change the port in the docker-compose file (if using it)
```

More details/instructions are in the works.

## TODO: 
- Open User registration
- Config script to make app more portable
- Implement vulnerabilities to allow XSW attacks
- Implement patch for cve-2017-11427 so that the vulnerability can be turned on/off

Shout out to E.D. for initial dockerization of the idp.
