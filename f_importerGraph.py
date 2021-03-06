import pymysql.cursors

def import_graph():
	"""
	Imports information from database and orders it in a dictionary that the dijkstra algorithm can work with.
	:return:
	A dictionary with for each node another dictionary with the nodes connected to that node and the distance between them.
	"""
	connection = pymysql.connect(host='192.168.0.2',
				     user='monitor',
				     password='navgap',
				     db='navgapdb',
				     charset='utf8mb4')
	curs = connection.cursor()

	#Imports data from db into python dictionary
	locations = []
	curs.execute("SELECT * FROM Locations")
	connection.commit()
	for row in curs.fetchall():
		locations.append(row[0])
	graph = {}

	for each in locations:
		curs.execute("SELECT * FROM LocationConnections")
		connection.commit()
		graph[each] = {}
		temp = []
		for row in curs.fetchall():
			if row[0] == each:
				temp.append([str(row[1]), str(row[2])])
		for neighbor in temp:
			graph[each][neighbor[0]] = neighbor[1] 
	connection.close()
	return graph
print(import_graph())
