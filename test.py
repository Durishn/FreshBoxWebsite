

from pyramid.config import Configurator

import psycopg2


conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")

cur = conn.cursor()

cur.execute("SELECT first_name from public.\"Users\"")

rows = cur.fetchall()



print ("\nShow me some stuff:\n")
for row in rows:
    print ("   ", row)