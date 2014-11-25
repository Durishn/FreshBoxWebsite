
from pyramid.config import Configurator

import psycopg2

def Example():
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT * from public.\"Things\"")
	rows = cur.fetchall()

# userExists 
#
#  Check if an email is already used by a user in the database.
#
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
	
# authUser
#
#  Authenticate the users account
#  		
#  Check if the given password for a user matches what's in 
#  		the database for them
#def authUser(email, password):
#	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
#	cur = conn.cursor()
#	cur.execute("SELECT email, password FROM public.\"Users\"")
#	rows = cur.fetchall()
#	for row in rows:
#		if email == row[0]:
#			return password == row[1]
#	return false

# addUser 
#
#  Adds a new user to the database.
#  		This is used by administrators to create new user accounts 
#		for host site coordinators and for other administrators
def addUser(credentials, email, password, firstName, lastName, phoneNumber):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"Users\" (email, password, first_name, last_name, phone_number) VALUES (\'" + email + "\', \'" + password + "\', \'" + firstName + "\', \'" + lastName + "\', \'" + phoneNumber + "\')")
	conn.commit();
	return userExists(email)
	
# updateUser
#  
#  Update user information for a given account.
#
#  @return - true if the user existed and information was
#        	successfully updated, false otherwise
def updateUser(email, newEmail, newPassword, newFirstName, newLastName, newPhoneNumber, credential_id):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("UPDATE public.\"Users\" SET (email, password, first_name, last_name, phone_number, \"credentials_idFK\") = ('" 
					+ newEmail + "', '" + newPassword + "', '" + newFirstName + "', '" + newLastName + "', '" + newPhoneNumber + "', '" + credential_id + "') WHERE email = '" + email + "'")
	conn.commit();
	return userExists(email)
	
# getUsers
# 
#  Lets administrators get a list of all user accounts in the 
# 		database
#	Returns an array of dictionaries, each dictionary corresponds to a User row.
def getUsers():
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT u.email, u.first_name, u.last_name, u.phone_number, c.label from public.\"Users\" u INNER JOIN public.\"Credentials\" c on c.id = u.\"credentials_idFK\"")
	rows = cur.fetchall()

	dictionary = []
	for row in rows:
		user = {'email': row[0], 'first_name': row[1], 'last_name': row[2], 'phone': row[3], 'credentials': row[4]}
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
	cur.execute("SELECT u.email, u.first_name, u.last_name, u.phone_number, c.label, u.id, u.password from public.\"Users\" u INNER JOIN public.\"Credentials\" c on c.id = u.\"credentials_idFK\" WHERE u.email = '" + email + "'")
	rows = cur.fetchall()
	
	if len(rows) == 1:
		return {'email': rows[0][0], 'first_name': rows[0][1], 'last_name': rows[0][2], 'phone_number': rows[0][3], 'credentials': rows[0][4], 'id': rows[0][5], 'password':rows[0][6]}
	return None
	
# addHostSite
#
#  Add a new host site
#  @return - true if successful database entry, false otherwise
def addHostSite(name, address, city, province, hoursOfOperation):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"HostSites\" (name) VALUES (\'" + name + "\')")
	conn.commit()
	return None
	
def addCoordToHostSite(user_id, hostsite_id):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"CoordinatorHostSiteRel\" (\"user_idFK\", \"hostsite_idFK\") VALUES (\'" + user_id + "', '" + hostsite_id + "')")
	conn.commit()
	return None
	
def removeCoordFromHostSite(user_id, hostsite_id):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("DELETE FROM public.\"CoordinatorHostSiteRel\" WHERE \"user_idFK\" = " + user_id + " AND \"hostsite_idFK\" = " + hostsite_id + "")
	conn.commit()
	return None
	
# getHostSiteList
#
# 	Returns all host sites for the given coordinator by returning 
#	an array of dictionaries 
#	@return - Array.<Dictionary> Each dictionary contains a host 
#			site with all host site values listed in the schema 
#			above
def getHostSiteList(coordinatorID):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT hs.id, hs.name from public.\"HostSites\" hs INNER JOIN public.\"CoordinatorHostSiteRel\" c ON c.\"hostsite_idFK\" = hs.\"id\" WHERE c.\"user_idFK\" = " + coordinatorID)
	rows = cur.fetchall()

	dictionary = []
	for row in rows:
		hostSite = {'id':row[0], 'name':row[1]}
		dictionary.append(hostSite);
	return dictionary

# getAllHostSites
#
# 	Administrators will need to see all host sites and so will 
#	users of the site when they are looking to see where they want 
#	to pick up their boxes
#
#	@return - Array.<Dictionary> Each dictionary contains a host 
#			site with all host site values listed in the schema 
#			above
def getHostSites(): 
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT hs.id, hs.name from public.\"HostSites\" hs")
	rows = cur.fetchall()

	dictionary = []
	for row in rows:
		hostSite = {'id':row[0], 'name':row[1]}
		dictionary.append(hostSite);
	return dictionary

# getHostSite
#
#	Sometimes you want to get information based on just a host site   
#	ID value
# 	@return - Array.<Dictionary> Each dictionary contains a host 
#			site with all host site values listed in the schema 
#			above
def getHostSite(hostSiteID):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT hs.id, hs.name from public.\"HostSites\" hs WHERE hs.id = \'" + hostSiteID + "\'")
	rows = cur.fetchall()
	
	if len(rows) == 1:
		return {'id':rows[0][0], 'name':rows[0][1]}
	return None
	
def addOrder(customer_first_name, customer_last_name, customer_email, customer_phone, large_quant, small_quant, donation, total_paid, hostsite):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("INSERT INTO public.\"Orders\" (customer_first_name, customer_last_name, customer_email, customer_phone, large_quantity, small_quantity, donation, total_paid, \"hostsitepickup_idFK\") VALUES (" 
	+ "'" + customer_first_name + "', '" + customer_last_name + "', '" + customer_email + "', '" + customer_phone + "', '" + large_quant + "', '" + small_quant + "', '" + donation + "', '" + total_paid + "', '" + hostsite + "')")
	conn.commit()
	
def updateOrder(order_id, customer_first_name, customer_last_name, customer_email, customer_phone, large_quant, small_quant, donation, total_paid, hostsite):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("UPDATE public.\"Orders\" SET (customer_first_name, customer_last_name, customer_email, customer_phone, large_quantity, small_quantity, donation, total_paid, \"hostsitepickup_idFK\") = ("
	+ "'" + customer_first_name + "', '" + customer_last_name + "', '" + customer_email + "', '" + customer_phone + "', '" + large_quant + "', '" + small_quant + "', '" + donation + "', '" + total_paid + "', '" + hostsite + "') WHERE id = '" + order_id + "'")
	conn.commit();
	return None

 
def getOrders(hostSiteID):
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT o.id, o.customer_first_name, o.customer_last_name, o.customer_email, o.customer_phone, o.large_quantity, o.small_quantity, o.donation, o.total_paid FROM public.\"Orders\" o WHERE o.\"hostsitepickup_idFK\" = '" + hostSiteID + "'")
	rows = cur.fetchall()

	dictionary = []
	for row in rows:
		order = {'id':row[0], 'customer_name':row[1] + row[2], 'customer_email':row[3], 'customer_phone':row[4], 'large_quant':row[5], 'small_quant':row[6], 'donation':row[7], 'amount_paid':row[8]}
		dictionary.append(order);
	return dictionary

	
def getMenu(self):
	retVal = []
	
	if ('userType' not in self.request.session):
		retVal.append({'href':'login','title': 'Staff Login', 'style':''})
		return retVal

	if (self.request.session['userType'] == 'Administrator'):
		retVal.append({'href':'logout','title': 'Logout'})
		retVal.append({'href':'users','title': 'Manage Users'})
		retVal.append({'href':'hostsites','title': 'Manage HostSites'})
		retVal.append({'href':'orders','title': 'Manage Orders'})
	elif (self.request.session['userType'] == 'Coordinator'):
		retVal.append({'href':'logout','title': 'Logout'})
		retVal.append({'href':'hostsites','title': 'Manage HostSites'})
		retVal.append({'href':'orders','title': 'Manage Orders'})
	else:
		retVal.append({'href':'login','title': 'Staff Login', 'style':''})
	return retVal
    
def userType(user,password):
	if (userExists(user)):
		if (authUser(user, password)):
			if (getUser(user)['credentials'] == 'Administrator'):
				return "Administrator"
			elif (getUser(user)['credentials'] == 'Coordinator'):
				return "Administrator"
	return "none"

def authUser(email, password):
	if (userExists(email)):
		user = getUser(email)
		if (user['password'] == password):
			return user
		return None
		
		