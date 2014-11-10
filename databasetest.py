import sqlite3

def create_db():

	conn = sqlite3.connect('example2.db')

	c = conn.cursor()

	# Create table
	c.execute("DROP TABLE IF EXISTS locations")
	c.execute('''CREATE TABLE locations
				  (location_name text, location_zip real, accronym text)''')
	# Insert a row of data
	loconame = "blah"
	locozip = "zip"
	locoaccr = "meh"

	dbloconame = str("'"+loconame+"'")
	dblocozip = str("'"+locozip+"'")
	dblocoaccr = str("'"+locoaccr+"'")
	c.execute("INSERT INTO locations VALUES (?, ?, ?);", (dbloconame, dblocozip, dblocoaccr))

	# Save (commit) the changes
	conn.commit()


	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
create_db()
print "(create_db())"