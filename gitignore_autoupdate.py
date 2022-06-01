# update .gitignore
	
def	read_gitignore(file_name):
	file = open(file_name, "r")
	lines = file.readlines()
	file.close()
	return lines

def update_gitignore(file_name, latest_update):
	lines = read_gitignore(file_name = ".gitignore")
	file = open(file_name, "w")
	for i in range (0, len(lines) - 1):
		file.write(lines[i])
	file.write("!/Charts/" + latest_update)
	file.close()
	return True