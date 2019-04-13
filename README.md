Vulnerable SAML infrastructure.

The purpose of these applications is to showcase how certain vulnerable configurations can be exploited to allow a user to change there permissions, name, etc. within an application. OneLogins python SAML library was utilized for this. In order for some of these vulnerable configurations to work the library was heavily modified.

This configuration contains two docker images. The first one vulnerableidp is an identity provider. It contains a 'database' with two users. One an administrator and another low priviledge user.

To spin up these docker images is fairly easy. Just run:
```
docker-compose up
```

The images will build and then the web application will be hosted at http://127.0.0.1:8000

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

Instructor user that can adjust security levels:
  ```
  Username: instructor
  Password: G0od-LuckGu3ssingThisButHeyItCouldHappenRight?
  ```

To upgrade privileges after logging in as the 'yogi' user change the group membership in the SAML message from 'users' to 'admin'

If you'd like to change the user accounts, or the groups around edit the authsources.php file. All user accounts are statically assigned and created within that file.

Want to set this up on seperate servers or point to an address that isn't localhost? A couple of changes need to be made first:
VulnerableSAMLApp/vulnerableidp/saml20-sp-remote.php
```
In the saml20-sp-remote.php file change every instance of '127.0.0.1:8000' with your web application ip.
```

VulnerableSAMLApp/vulnerablesp/yogiSP/saml/settings.json
```
In the settings.json file within the SP section replace the '127.0.0.1:8000' with your web applications ip.
Within the IDP section you'll also need to replace the '127.0.0.1' address with the address of the IDP server.
```

To change the port the vulnerable application is listening on:
```
In vulnerablesp/yogiSP/vulnsp.py update the port on the last line.
In vulnerablesp/yogiSP/vulnsp.ini update http = :8000 with the new port.
```

More details/instructions are in the works.

TODO: Open User registration
TODO: config script to make app more portable
TODO: Implement vulnerabilities to allow XSW attacks
TODO: Implement patch for cve-2017-11427 so that the vulnerability can be turned on/off

Shout out to E.D. for initial dockerization of the idp.
