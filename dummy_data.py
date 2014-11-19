
from pyramid.config import Configurator

import psycopg2

def Example():
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")

	cur = conn.cursor()

	cur.execute("SELECT * from public.\"Things\"")

	rows = cur.fetchall()


COMPANY = "Garden Fresh Box"

def getUsers():
	returnVal = []
	
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT first_name from public.\"Users\"")
	rows = cur.fetchall()

	for row in rows:
		user = {'first_name': row[0]}
		returnVal.append(user);
	
	return returnVal

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
	
	
SITE_MENU = [
        {'href': '', 'title': 'Home'},
        {'href': 'contact', 'title': COMPANY},
]