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
  Password: adminpassword
  ```
  
To upgrade priviledges after logging in as the 'yogi' user change the group membership in the SAML message from 'users' to 'admin'

More details/instructions are in the works.

Shout out to E.D. for initial dockerization of the idp.
