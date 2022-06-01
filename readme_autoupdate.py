# update readme
import os

def read_base_readme(file_name):
	file = open(file_name, "r")
	base_readme = file.read()
	file.close
	return base_readme
	
def get_charts_name(file_name):
	file = open(file_name, "r")
	charts_name = []
	for line in file:
		charts_name.append(line.rstrip("\n"))
	file.close() 
	return charts_name
	
def readme_update(readme_name, base_readme, latest_update):
	base_readme = base_readme + latest_update +".\n\n"
	readme = open(readme_name, "w")
	readme.write(base_readme)
	files = os.scandir("./Charts/" + latest_update)
	for file in files:
		readme.write("![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/"+latest_update+"/"+file.name.replace(' ','%20')+")\n\n")
	readme.close
	
def create_readme(base_readme_file_name, latest_update):
	base_readme = read_base_readme(base_readme_file_name)
	readme_update("README.md", base_readme, latest_update)
	return True