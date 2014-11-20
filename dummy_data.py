
from pyramid.config import Configurator

import psycopg2

COMPANY = "Garden Fresh Box"

def Example():
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT * from public.\"Things\"")
	rows = cur.fetchall()

# userExists 
#
#  Check if an email is already used by a user in the database.
#
#  email -   the email that the user to be checked would have  
#        	signed up with
#  @return - true if a user with the given email is in the  	
#        	database, false otherwise
def userExists(email):

	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT email from public.\"Users\"")
	rows = cur.fetchall()

	for row in rows:
		if (row[0] == email):
			return True
	
	return False;
	
# addUser 
#
#  Adds a new user to the database.
#  		This is used by administrators to create new user accounts 
#		for host site coordinators and for other administrators
#  
#  email - email address of the new user
#  password - the password for the new user (entered manually by 
#  			administrator)
#  firstName -
#  lastName - (optional)
#  phoneNumber - (optional)
#  hostSites - (optional) a list of host sites associated with the   
#  			account, ONLY for coordinator accounts
#  credentials - required to determine what level of account the
#			user is being given
#  @return - true if the user was added successfully, 
#			false otherwise
def addUser(credentials, email, password, firstName, lastName, phoneNumber, hostSites):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"Users\" (email, password, first_name, last_name, phone_number) VALUES (\'" + email + "\', \'" + password + "\', \'" + firstName + "\', \'" + lastName + "\', \'" + phoneNumber + "\')")
	#print ("INSERT INTO public.\"Users\" (email, password, first_name, last_name, phone_number) VALUES (\'" + email + "\', \'" + password + "\', \'" + firstName + "\', \'" + lastName + "\', \'" + phoneNumber + "\')")
	conn.commit();
	return userExists(email)
	
# authUser
#
#  Authenticate the users account
#  		
#  Check if the given password for a user matches what's in 
#  		the database for them
# 
#  email -
#  password -
#  @return - true if auth is valid, false otherwise
def authUser(email, password):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT email, password FROM public.\"Users\"")
	rows = cur.fetchall()
	for row in rows:
		if email == row[0]:
			return password == row[1]
	return false
	
# updateUser
#  
#  Update user information for a given account.
# 
#  email - The email for the user that's in the database
#  newEmail - (optional) the new email the user should have
#  newPassword - (optional) the new password the user should have
#  newFirstName - (optional
#  newLastName - (optional)
#  newPhoneNumber - (optional)
#  hostSites - (optional) a list of hostSiteIDs associated with the   
#  			account, this is ONLY for coordinator accounts
#  credentials - (optional) if no credentials provided, no change 
#  			made
#  @return - true if the user existed and information was
#        	successfully updated, false otherwise
def updateUser(email, newEmail, newPassword, newFirstName, newLastName, newPhoneNumber, hostSites, credentials):
	#TODO all
	return false
	
# getUsers
# 
#  Lets administrators get a list of all user accounts in the 
# 		database
#	Returns an array of dictionaries, each dictionary corresponds to
#	a User row.
#
#  @ return Array.<Dictionar> an array of dictionaries, each 
#  			dictionary corresponds to a user account
#  			MUST include ALL user information given by the 
#			database schema above BUT NOT the plaintext password
def getUsers():
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT u.email, u.first_name, u.last_name, u.phone_number, c.label from public.\"Users\" u INNER JOIN public.\"Credentials\" c on c.id = u.\"credentials_idFK\"")
	rows = cur.fetchall()

	dictionary = []
	for row in rows:
		user = {'email': row[0], 'first_name': row[1], 'last_name': row[2], 'phone_number': row[3], 'credentials': row[4]}
		dictionary.append(user);
	return dictionary
	
# getUser
#  
#  getUser information that we will need since after login all the 
# 		system has is the email used to login (which you should 
#		cache somewhere) and the credential level
#
#  @return - Dictionary, the dictionary value corresponding to the 
#			 user email given.
#  			MUST include ALL user information given by the 
#			database schema above BUT NOT the plaintext password
def getUser(email):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT u.email, u.first_name, u.last_name, u.phone_number, c.label from public.\"Users\" u INNER JOIN public.\"Credentials\" c on c.id = u.\"credentials_idFK\" WHERE u.email = \'" + email + "\'")
	rows = cur.fetchall()
	
	if len(rows) == 1:
		return {'email': rows[0][0], 'first_name': rows[0][1], 'last_name': rows[0][2], 'phone_number': rows[0][3], 'credentials': rows[0][4]}
	return None
	
# addHostSite
#
#  Add a new host site
#
#  name - the name of the new host site
#  address - the street number, apartment number and street name 
#  city - city in which the host site is
#  province - what province is it
#  coordinatorIDs - (optional) an up to date list of all 
#			coordinators associated with the host site
#  hoursOfOperation - (optional) A dictionary where the key is the 
#				day of the week and the value is a string which 
#				looks like: "open,close" and each open and 
#				close are in 24 hour time (4 digit number: 1200 
#				is noon for example), you are responsible 
#				for storing these values.
#  
#  @return - true if successful database entry, false otherwise
def addHostSite(name, address, city, province, hoursOfOperation):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"HostSites\" (name) VALUES (\'" + name + "\')")
	
	user = getUser
	
	#TODO: this method should accept a list of coordinators to add to this host site
	#cur.execute("INSERT INTO public.\"CoordinatorHostSiteRel\" (\"user_idFK\", \"hostsite_idFK\") VALUES (\'" + name + "\'")
	#insert into public."CoordinatorHostSiteRel" ("user_idFK", "hostsite_idFK") values (9,2);
	conn.commit();
	return None
	
def getMenu(self):
    retVal = [ {'href': '', 'title': 'Home'},  {'href': 'contact', 'title': COMPANY}]
    if('userType' in self.request.session):
        if(self.request.session['userType'] == 'none'):
            retVal.append({'href':'login','title': 'Login'});
        else:
            retVal.append({'href':'logout','title': 'Logout'});
    else:
        retVal.append({'href':'login','title': 'Login', 'style':''});
    return retVal
    
def userType(user,password):
    if(user == 'admin' and password == 'pass'):
        return "admin"
    return "none";
