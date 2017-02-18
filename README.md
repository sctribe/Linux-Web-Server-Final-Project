# Linux Server Configuration Project

A baseline installation of a Ubuntu Linux server is configured to host a Flask web application on a virtual machine. The server will be secured from a number of attack vectors and includes the configuration of a database server and installation of updates.

The web application is reachable at this [AWS-server instance](http://35.166.120.164/) or [http://35.166.120.164/](http://35.166.120.164/).

**Note:** The web application will not be available after graduating from the Udacity Full Stack Developer Nanocegree Course.


## Step by Step Walkthrough
Below is a detailed guide documenting the steps taken to configure the Ubuntu Linux server to be able to host a web application which is actually the solution to [project 5](https://github.com/sctribe/Udacity-Catalog-Project).

The project details outline 11 steps that must be completed to properly complete this project. These 11 steps are as follows:

1. Launch your Virtual Machine with your Udacity account. Please note that upon graduation from the program your free Amazon AWS instance will no longer be available.
2. Follow the instructions provided to SSH into your server
3. Create a new user named grader
4. Give the grader the permission to sudo
5. Update all currently installed packages
6. Change the SSH port from 22 to 2200
7. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
8. Configure the local timezone to UTC
9. Install and configure Apache to serve a Python mod_wsgi application
10. Install and configure PostgreSQL:
  *Do not allow remote connections
  *Create a new user named catalog that has limited permissions to your catalog application database
11. Install git, clone and setup your Catalog App project (from your GitHub repository from earlier in the Nanodegree program) so that it functions correctly when visiting your server’s IP address in a browser. Remember to set this up appropriately so that your .git directory is not publicly accessible via a browser!

**Note:** Most of the steps outlined below are done as the root user and as such do not need the `sudo` command.


### 1 - Launch Virtual Machine

The VM environment is created by clicking the link in your Udacity account. This Amazaon AWS instance will expire upon graduation from the program.

### 2 - SSH into the Server
Source: [Udacity](https://www.udacity.com/account#!/development_environment)

1. Download private keys and write down your public IP address.
2. Move the private key file into the folder ~/.ssh. If you downloaded the file to the Downloads folder execute the following command:
  `$ mv ~/Downloads/udacity_key.rsa ~/.ssh/`
3. To make sure only the owner can read and write this file open your terminal and type in:
  `$ chmod 600 ~/.ssh/udacity_key.rsa`
4. To SSH in to the development environment type in:
  `$ ssh -i ~/.ssh/udacity_key.rsa root@PUPLIC-IP-ADDRESS`

### 3 - Create New User Named Grader
Source: Configuring Linux Web Servers Udacity Course

1. Create a New User Named grader:
  `$ adduser grader`

### 4 - Give the grader the Permission to sudo
Source: Configuring Linux Web Servers Udacity Course

1. Give new user the permission to sudo:
  1. Create a new file in the /etc/sudoers.d/ directory named grader:
    `$ nano /etc/sudoers.d/grader`
  2. Add the following line to the empty grader file:
    `grader ALL=(ALL) NOPASSWD:ALL`

### 5 - Update Currently Installed Packages and Install New Dependicies
Source: [Ask Ubuntu](http://askubuntu.com/questions/94102/what-is-the-difference-between-apt-get-update-and-upgrade)  and [Udacity Forum](https://discussions.udacity.com/t/how-to-run-a-flask-app-in-aws/213184/7)

1. Update the list of available packages and their versions:
  `$ apt-get update`
2. Install newer vesions of packages you have:
  `$ apt-get upgrade`
3. Type in each of the following lines one by one to install the required packages and dependicies:
  `$ apt-get install postgresql python-psycopg2`
  `$ apt-get install python-flask python-sqlalchemy`
  `$ apt-get install python-pip`
  `$ pip install bleach`
  `$ pip install oauth2client`
  `$ pip install requests`
  `$ pip install httplib2`
  `$ pip install redis`
  `$ pip install passlib`
  `$ pip install itsdangerous`
  `$ pip install flask-httpauth`

### 6 - Change the SSH Port From 22 to 2200 and Configure SSH Access
Source: Configuring Linux Web Servers Udacity Course

1. Change ssh config file:
  1. Open the config file:
    `$ nano /etc/ssh/sshd_config`
  2. Change from Port 22 to Port 2200.
  3. Change PasswordAutentication to no.
  4. On your local machine run the following command to generate a key pair:
    `$ ssh-keygen`
  5. At the prompt give the following file name:
    `~/.ssh/graderkey`
  6. Enter passphrase.
  7. Two files will be generated - graderkey and graderkey.pub. The .pub file will be placed on the web server to enable key based authentication.
  8. Change to the grader user:
    `$ su grader`
  9. Create .ssh directory in home directory:
    `$ mkdir .ssh`
  10. Create a file named authorized_keys:
    `$ touch .ssh/authorized_keys`
  11. Open the file and copy the contents of graderkey.pub from the local machine in to the authorized_keys file:
    `$ nano authorized_keys`
  12. For security change the file permissions so other users cannot gain access to the grader account:
    `$ chmod 700 .ssh` and `$ chmod 644 .ssh/authorized_keys`
  13. Restart the service:
    `$ service ssh restart`
  14. Exit the grader user and go back to root:
    `$ exit`
  15. You can now log in to the grader user using key based authentication.

### 7 - Configure the Uncomplicated Firewall (UFW) to Only Allow Incoming Connections For SSH (port 2200), HTTP (port 80), and NTP (port 123)
Source: Configuring Linux Web Servers Udacity Course

1. Check the status of UFW and make sure it is off:
  `$ ufw status`
2. Deny all incoming connections to the server:
  `$ ufw default deny incoming`
3. Allow all outgoing connections from the server:
  `$ ufw default allow outgoing`
4. Allow incoming TCP packets on port 2200 (SSH):
  `$ ufw allow 2200`
5. Allow incoming TCP packets on port 80 (HTTP):
  `$ ufw allow www`
6. Allow incoming UDP packets on port 123 (NTP):
  `$ ufw allow 123`
7. Turn UFW on:
  `$ ufw enable`

### 8 - Configure the local timezone to UTC
Source: [Ubuntu documentation](https://help.ubuntu.com/community/UbuntuTime#Using_the_Command_Line_.28terminal.29)

1. Open the timezone selection dialog:
  `$ dpkg-reconfigure tzdata`
2. Then chose 'None of the above', then UTC.

### 9 - Install and Configure Apache to Serve a Python mod_wsgi Application
Source: [Udacity](http://blog.udacity.com/2015/03/step-by-step-guide-install-lamp-linux-apache-mysql-python-ubuntu.html)

1. Install Apache web server:
  `$ apt-get install apache2`
2. Open a browser and open your public ip address, e.g. http://35.166.120.164/. The Apache2 Ubuntu Default Page should load.
3. Install **mod_wsgi** for serving Python apps from Apache and the helper package **python-setuptools**:
  `$ apt-get install libapache2-mod-wsgi`
4. Restart the Apache server for mod_wsgi to load:
  `$ service apache2 reload`

### 10 - Install and Configure PostgreSQL
Source: [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

1. Install PostgreSQL if not installed as part of step 5:
  `$ apt-get install postgresql postgresql-contrib`
2. Check that no remote connections are allowed (default):
  `$ nano /etc/postgresql/9.3/main/pg_hba.conf`
3. Create needed linux user for psql:
  `$ adduser catalog` (choose a password)
4. Switch to the postgres user:
  `$ su postgres`
5. Launch PostgreSQL:
  `$ psql`
10. Add psql user with password:
  Sources: [Trackets Blog](http://blog.trackets.com/2013/08/19/postgresql-basics-by-example.html) and [Super User](http://superuser.com/questions/769749/creating-user-with-password-or-changing-password-doesnt-work-in-postgresql)
  1. Create user with LOGIN role and set a password:
    `# CREATE USER catalog WITH PASSWORD 'PW-FOR-DB';` (# stands for the command prompt in psql)
  2. Allow the user to create database tables:
    `# ALTER USER catalog CREATEDB;`
  3. List current roles and their attributes:
    `# \du`
11. Create database:
  `# CREATE DATABASE catalog WITH OWNER catalog;`
12. Connect to the database catalog
  `# \c catalog`
13. Revoke all rights:
  `# REVOKE ALL ON SCHEMA public FROM public;`
14. Grant only access to the catalog role:
  `# GRANT ALL ON SCHEMA public TO catalog;`
15. Exit out of PostgreSQl and the postgres user:
  `# \q`, then `$ exit`

### 11 - Install Git, Clone and Setup your Catalog App Project

#### 11.1 - Install and configure git
Source: [GitHub](https://help.github.com/articles/set-up-git/#platform-linux)

1. Install Git:
  `$ apt-get install git`
2. Set your name, e.g. for the commits:
  `$ git config --global user.name "YOUR NAME"`
3. Set up your email address to connect your commits to your account:
  `$ git config --global user.email "YOUR EMAIL ADDRESS"`

#### 11.2 - Setup for deploying a Flask Application on Ubuntu VPS
Source: [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

1. Extend Python with additional packages that enable Apache to serve Flask applications:
  `$ apt-get install libapache2-mod-wsgi python-dev`
2. Enable mod_wsgi (if not already enabled):
  `$ sudo a2enmod wsgi`
3. Create a Flask app:
  1. Move to the www directory:
    `$ cd /var/www`
  2. Setup a directory for the app:
    1. `$ sudo mkdir catalog`
    2. `$ cd catalog` and `$ sudo mkdir catalog`
    3. `$ cd catalog` and `$ sudo mkdir static templates`
    4. Create the file that will contain the flask application logic:
      `$ nano __init__.py`
    5. Paste in the following code:
    ```python
      from flask import Flask
      app = Flask(__name__)
      @app.route("/")
      def hello():
        return "This is my Flask App"
      if __name__ == "__main__":
        app.run()
    ```
4. Install Flask
  1. Install virtualenv:
    `$ pip install virtualenv`
  2. Set virtual environment to name 'venv':
    `$ virtualenv venv`
  3. Enable all permissions for the new virtual environment (no sudo should be used within):
    Source: [Stackoverflow](http://stackoverflow.com/questions/14695278/python-packages-not-installing-in-virtualenv-using-pip)
    `$ sudo chmod -R 777 venv`
  5. Activate the virtual environment:
    `$ source venv/bin/activate`
  6. Install Flask inside the virtual environment:
    `$ pip install Flask`
  7. Run the app:
    `$ python __init__.py`
  8. Deactivate the environment:
    `$ deactivate`

5. Configure and Enable a New Virtual Host#
  1. Create a virtual host config file:
    `$ nano /etc/apache2/sites-available/catalog.conf`
  2. Paste in the following lines of code and change names and addresses regarding your application:
  ```
    <VirtualHost *:80>
        ServerName PUBLIC-IP-ADDRESS
        ServerAdmin admin@PUBLIC-IP-ADDRESS
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/catalog/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

  ```
  3. Enable the virtual host:
    `$ a2ensite catalog`
6. Create the .wsgi File and Restart Apache:
  1. Create wsgi file:
    `$ cd /var/www/catalog` and `$ nano catalog.wsgi`
  2. Paste in the following lines of code:
  ```
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/catalog/")

    from catalog import app as application
    application.secret_key = 'Add your secret key'

  ```
  **Note:** The secret key provided in this file must match the secret key in your application.py/__init.py file.
  7. Restart Apache:
    `$ service apache2 reload`

#### 11.3 - Clone GitHub repository and make it web inaccessible
1. Clone project 5 solution repository on GitHub:
  `$ git clone https://github.com/sctribe/Udacity-Catalog-Project.git`
2. Copy all content (including hidden files) of created Udacity-Catalog-Project directory to `/var/www/catalog/catalog/` directory and delete the Udacity-Catalog-Project directory:
  `$ cp -r /var/www/catalog/catalog/Udacity-Catalog-Project/* /var/www/catalog/catalog`
  `$ rm -r /var/www/catalog/catalog/Udacity-Catalog-Project`
3. Make the GitHub repository inaccessible:
  Source: [Stackoverflow](http://stackoverflow.com/questions/6142437/make-git-directory-web-inaccessible)
  1. Create and open .htaccess file in /var/www/catalog/ directory:
    `$ cd ..` and `$ nano .htaccess`
  2. Paste in the following:
    `RedirectMatch 404 /\.git`

#### 11.4 - Install needed modules & packages
1. Install SQLAlchemy:
  `$ pip install sqlalchemy`
2. **Note:** For how this particular application is coded an earlier version of Flask is needed. Type in the following commands to downgrade Flask. This is not needed for all applications:
  `$ sudo pip install werkzeug==0.8.3`
  `$ sudo pip install flask==0.9`
  `$ sudo pip install Flask-Login==0.1.3`


#### 11.5 - Run application
1. Open the database setup file:
  `$ nano database_setup.py`
2. Change the line starting with "engine" to (fill in a password):
  `engine = create_engine('postgresql://catalog:PW-FOR-DB@localhost/catalog')`
3. Change the same line in the project.py file respectively.
4. Rename project.py:
  `$ mv project.py __init__.py`
  * The original project called for the app.secret_key code to be placed in an if block (if__name__=="__main__"). Since this is a WSGI application __name__ will not equal to __main__ and this code will never run. Remove the if block and leave the app.secret_key line at the end of your __init__.py file.
5. Create postgreSQL database schema:
  `$ python database_setup.py`
6. Populate the database with some data:
  1. Open genre_populator.py file and the line starting with "engine" to (fill in a password):
    `engine = create_engine('postgresql://catalog:PW-FOR-DB@localhost/catalog')`
  2. Run genre_populator.py:
    `$ genre_populator.py`
6. Restart Apache:
  `$ service apache2 reload`
7. Open a browser and put in your public ip-address as url, e.g. 52.25.0.41 - if everything works, the application should come up.
8. If getting an internal server error, check the Apache error files:
  1. View the last 20 lines in the error log:
    `$ tail -20 /var/log/apache2/error.log`
  2. If a file like 'client_secrets.json' couldn't been found open __init__.py and provide the full path to the file instead of the relative path.
    Source: [Stackoverflow](http://stackoverflow.com/questions/12201928/python-open-method-ioerror-errno-2-no-such-file-or-directory)

#### 11.6 - Get OAuth-Logins Working
  Source: [Udacity](http://discussions.udacity.com/t/oauth-provider-callback-uris/20460) and [Apache](http://httpd.apache.org/docs/2.2/en/vhosts/name-based.html)

1. Open http://www.hcidata.info/host2ip.cgi and receive the Host name for your public IP-address, e.g. for 35.166.120.164, its ec2-35-166-120-164.us-west-2.compute.amazonaws.com
2. Open the Apache configuration files for the web app:
  `$ nano /etc/apache2/sites-available/catalog.conf`
3. Paste in the following line below ServerAdmin:
  `ServerAlias HOSTNAME`, e.g. ec2-35-166-120-164.us-west-2.compute.amazonaws.com
4. Enable the virtual host:
  `$ a2ensite catalog`

#####To get the Google+ authorization working:
  1. Go to the project on the Developer Console: https://console.developers.google.com
  2. Navigate to APIs & auth > Credentials > Edit Settings
  3. Add the public IP-address and host name to the Authorized JavaScript origins and your host name + oauth2callback to Authorized redirect URIs, e.g. ec2-35-166-120-164.us-west-2.compute.amazonaws.com/oauth2callback
  4. Download the new client_secrets.json file and copy its contents into the client_secrets.json file on your webserver.

#####To get the Facebook authorization working:
  1. Go on the Facebook Developers Site https://developers.facebook.com/apps/
  2. Click on your App, go to Settings and fill in your public IP-Address including prefixed http:// as well as the hostname in the Site URL field
  3. To leave the development mode, so others can login as well, also fill in a contact email address in the respective field, "Save Changes".


