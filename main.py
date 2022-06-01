import csv
import ctypes  # to get screen size
import os
import urllib.request

import gitignore_autoupdate
import matplotlib.pyplot as plt
import numpy as np
import readme_autoupdate
import twitter

# set SHOW_CHARTS_ENABLED = 1 to show all the charts
SHOW_CHARTS_ENABLED = 0

# set SAVING_ENABLED = 0 if you don't want to save the charts
SAVING_CHARTS_ENABLED = 1

# the folder that contains the saved charts
DESTINATION_PATH = "Charts/"

def download(fileName, url):	
	print('Downloading CSV dataset from '+url)
	urllib.request.urlretrieve(url, fileName)
	print('CSV dataset \"'+fileName+'\" downloaded')

def csv_reader(fileName):	
	with open(fileName, mode = 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		list = []
		for row in csv_reader:
			if line_count == 0:
				# join all items in a tuple into a string, using a ", " character as separator:
				column_names = ", ".join(row)
				metadata = column_names.split(", ")
				# print(f'Column names are {", ".join(row)}')
				line_count += 1
				# list.append(row)
			else:
				# append row to the list
				list.append(row)
				# line_count += 1
		#print(f'Processed {line_count} lines.')	
	return list, metadata
	
def sum_data(list, metadata, dataType):
	total = 0
	for i in range (0, len (metadata)):
		if (metadata[i] == dataType):
			index = i
	for i in range (0, len (list)):
		total += int(list[i][index])
	return total

def get_screen_size():
	user32 = ctypes.windll.user32
	screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	return screensize

def get_string_list(list, column_index):
	data = [list[0][column_index]] # initialize list
	for i in range (1, len (list)):	
		if list[i][column_index] not in data:
			data.append(list[i][column_index])
	return data
	
def get_data_list(list, column_index):
	data = [] # initialize list
	for i in range (0, len (list)):
		try:
			data.append(float(list[i][column_index]))
		except ValueError as e:
			#print(e)
			return None
	return data
	
def get_cumulative_data(data, new_element, days, day_of_administration):
	if (len(data) == 0):
		data = [new_element]
		days.append(day_of_administration)
	else:
		if (days[len(days) - 1] == day_of_administration):
			data[len(data) - 1] += new_element
		else:
			data.append(data[len(data) - 1] + new_element)
			days.append(day_of_administration)
			
	return data, days
	
def	get_daily_data_from_cumulative_data(cumulative_data):
	daily_data = [cumulative_data[0]]	# initialize daily_data
	for element in np.diff(cumulative_data):
		daily_data.append(element)
	return daily_data
	
def get_index_from_column_name(metadata, column_name):
	for i in range (0, len(metadata)):
		if (metadata[i] == column_name):
			return i
	
def get_xticks(data, num):
	# create num ticks samples evenly spaced from 0 to len(data)
	if (len(data) < num):
		ticks = np.linspace(start = 0, stop = len(data) - 1, num = len(data))
	else:
		ticks = np.linspace(start = 0, stop = len(data) - 1, num = num)
	return ticks
	
def	get_labels(data, ticks):
	# create labels for each xticks
	labels = []
	for tick in ticks:
		labels.append(data[int(tick)])
	return labels
	
def initialize_figure(xdata, xlabel, ylabel, xticks_num):
	# get screen size to plot graphs full screen
	screenSize = get_screen_size()
	fig, ax = plt.subplots(figsize = [screenSize[0]/100, screenSize[1]/100])
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ticks = get_xticks(xdata, xticks_num)
	ax.set_xticks(ticks)
	ax.set_xticklabels(get_labels(xdata, ticks))
	return fig, ax
	
def bar_plot(figure, axes, xdata, ydata, ylabel, bar_width, offset, bottom, bar_label_enable):
	if (ydata == None):
		return None
	else:
		x = get_xticks(xdata, len(xdata)) 
		rect = axes.bar(x + offset, ydata, bar_width, label = ylabel, bottom = bottom)
		if (bar_label_enable == True):
			axes.bar_label(rect, horizontalalignment = 'center', verticalalignment = 'bottom', fmt = '%g')
		#axes.ticklabel_format(axis = 'y', style = 'plain')
		return figure
		
def place_text_in_charts(ticks, data):
	for tick in ticks:
		plt.text(x = tick, y = data[int(tick)], s = str(int(data[int(tick)])),\
		horizontalalignment = 'center', verticalalignment = 'bottom')
	
def plot_line_1data(xdata, ydata, xlabel, ylabel):
	screenSize = get_screen_size()
	fig = plt.figure(figsize = [screenSize[0]/100, screenSize[1]/100])
	plt.plot(ydata)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	xticks = get_xticks(data = xdata, num = 8)
	plt.xticks(ticks = xticks, labels = get_labels(xdata, xticks))
	place_text_in_charts(ticks = xticks, data = ydata)
	if (max(ydata) != ydata[len(ydata) - 1]):
		plt.text(x = ydata.index(max(ydata)), y = max(ydata), s = "MAX: "+str(int(ydata[ydata.index(max(ydata))])),\
		horizontalalignment = 'center', verticalalignment = 'bottom')
	return fig
	
def plot_line_2data(xdata1, xdata2, ydata1, ydata2, xlabel, ylabel1, ylabel2):
	screenSize = get_screen_size()
	fig = plt.figure(figsize = [screenSize[0]/100, screenSize[1]/100])
	if (len(ydata1) == len(ydata2)):
		plt.plot(ydata1)
		plt.plot(ydata2)
		xticks = get_xticks(data = xdata1, num = 8)
		plt.xticks(ticks = xticks, labels = get_labels(xdata1, xticks))
	
	if (len(ydata1) > len(ydata2)):
		plt.plot(ydata1)
		initial_zeros = list(np.zeros(len(ydata1) - len(ydata2)))
		plt.plot(initial_zeros.extend(ydata2))
		xticks = get_xticks(data = xdata1, num = 8)
		plt.xticks(ticks = xticks, labels = get_labels(xdata1, xticks))
	
	if (len(ydata2) > len(ydata1)):
		plt.plot(ydata2)
		initial_zeros = list(np.zeros(len(ydata2) - len(ydata1)))
		plt.plot(initial_zeros.extend(ydata1))
		xticks = get_xticks(data = xdata2, num = 8)
		plt.xticks(ticks = xticks, labels = get_labels(xdata2, xticks))
	
	place_text_in_charts(ticks = xticks, data = ydata1)
	place_text_in_charts(ticks = xticks, data = ydata2)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel1 + ", " + ylabel2)
	plt.legend([ylabel1, ylabel2])
	return fig
	
def	create_destination_folder(folder_name):
	# create destination folder to save figures
	try:
		os.mkdir(folder_name)
	except FileExistsError:
		#print("Folder " + folder_name + " already exists")
		None
		
def save_figure(figure_name, latest_update, figure, count):
	create_destination_folder(folder_name = DESTINATION_PATH + latest_update)
	if (figure != None and SAVING_CHARTS_ENABLED):
		figManager = plt.get_current_fig_manager()
		figManager.full_screen_toggle()
		figure.savefig(fname = DESTINATION_PATH + latest_update + "/" + latest_update + "-" + figure_name, format = 'png')
		count += 1
	plt.close(figure)
	return count
	
def main():
	# download the datasets
	download(fileName = 'vaccini-summary-latest.csv', url = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv')
	download(fileName = 'somministrazioni-vaccini-latest.csv', url = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')
	download(fileName = 'anagrafica-vaccini-summary-latest.csv', url = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv')
	
	# read vaccini-summary-latest.csv
	vaccini_summary_latest, metadata_vaccini_summary_latest = csv_reader('vaccini-summary-latest.csv')	
	
	# get the latest update of the csv 'vaccini-summary-latest.csv'
	latest_update = vaccini_summary_latest[len(vaccini_summary_latest) - 1][get_index_from_column_name(metadata_vaccini_summary_latest, "ultimo_aggiornamento")]
	
	# get the total number of administered doses 
	total_doses_administered = sum_data(vaccini_summary_latest, metadata_vaccini_summary_latest, dataType = 'dosi_somministrate')	
	print ("Total administered doses: " + str(total_doses_administered))
	
	# get the total number of delivered doses 
	total_doses_delivered = sum_data(vaccini_summary_latest, metadata_vaccini_summary_latest, dataType = 'dosi_consegnate')
	print ("Total delivered doses: " + str(total_doses_delivered))
	
	# get total vaccinations for each metadata of the csv 'vaccini-summary-latest.csv'
	count = 0
	xdata = get_string_list(vaccini_summary_latest, get_index_from_column_name(metadata_vaccini_summary_latest, "area"))
	for i in range (1, len(metadata_vaccini_summary_latest)):
		if (metadata_vaccini_summary_latest[i] != "codice_regione_ISTAT"):	
			ydata = get_data_list(vaccini_summary_latest, i)
			
			# plot data for each area
			figure, axes = initialize_figure(xdata, 'area', metadata_vaccini_summary_latest[i], len(xdata))
			figure = bar_plot(figure, axes, xdata, ydata, metadata_vaccini_summary_latest[i], 0.8, 0, list(np.zeros(len(xdata))), True)
			count = save_figure(figure_name = "area-" + metadata_vaccini_summary_latest[i] + ".png",\
					latest_update = latest_update, figure = figure, count = count)
					
	# read anagrafica-vaccini-summary-latest.csv
	anagrafica_vaccini, metadata_anagrafica_vaccini = csv_reader('anagrafica-vaccini-summary-latest.csv')
	
	# get the latest update of the csv 'anagrafica-vaccini-summary-latest.csv'
	latest_update = anagrafica_vaccini[len(anagrafica_vaccini) - 1][get_index_from_column_name(metadata_anagrafica_vaccini, "ultimo_aggiornamento")]
	
	# get total vaccinations for each metadata of the csv 'anagrafica-vaccini-summary-latest.csv'
	xdata = get_string_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, "fascia_anagrafica"))
	for i in range (1, len(metadata_anagrafica_vaccini)):
		ydata = get_data_list(anagrafica_vaccini, i)
		
		# plot data for each age group
		figure, axes = initialize_figure(xdata, 'fascia_anagrafica', metadata_anagrafica_vaccini[i], len(xdata))
		figure = bar_plot(figure, axes, xdata, ydata, metadata_anagrafica_vaccini[i], 0.8, 0, list(np.zeros(len(xdata))), True)
		count = save_figure(figure_name = "fascia_anagrafica-" + metadata_anagrafica_vaccini[i] + ".png",\
					latest_update = latest_update, figure = figure, count = count)	
					
	# get total vaccinations for male and female for each age group
	xdata = get_string_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'fascia_anagrafica'))	
	total_vaccination_male = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'sesso_maschile'))
	total_vaccination_female = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'sesso_femminile'))
	
	# plot total vaccinations for male and female
	figure, axes = initialize_figure(xdata, 'fascia_anagrafica', 'sesso_maschile, sesso_femminile', len(xdata))
	figure = bar_plot(figure, axes, xdata, total_vaccination_male, 'sesso_maschile', 0.35, 0.35/2, list(np.zeros(len(xdata))), True)
	figure = bar_plot(figure, axes, xdata, total_vaccination_female, 'sesso_femminile', 0.35, -0.35/2, list(np.zeros(len(xdata))), True)	
	axes.legend()
	count = save_figure(figure_name = "fascia_anagrafica-sesso_maschile-sesso_femminile.png",\
					latest_update = latest_update, figure = figure, count = count)	
	'''
	# get first and second doses for each age group
	xdata = get_string_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'fascia_anagrafica'))	
	total_first_doses = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'prima_dose'))
	total_second_doses = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'seconda_dose'))
	
	# plot first and second doses for each age group
	figure = plot_bar_2data(xdata, total_first_doses, total_second_doses, 'fascia_anagrafica', 'prima_dose', 'seconda_dose')
	count = save_figure(figure_name = "fascia_anagrafica-prima_dose-seconda_dose.png",\
					latest_update = latest_update, figure = figure, count = count)	
	
	# get total vaccinations for social health workers, non-health personnel and guests of residential care homes
	xdata = get_string_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'fascia_anagrafica'))	
	total_vaccination_social_health_workers = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_operatori_sanitari_sociosanitari'))
	total_vaccination_non_health_personnel = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_personale_non_sanitario'))
	total_vaccination_guests_residential_care_home = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_ospiti_rsa'))
	
	# plot total vaccinations for social health workers, non-health personnel and guests of residential care homes
	figure = plot_bar_3data(xdata, total_vaccination_social_health_workers, \
							total_vaccination_non_health_personnel, total_vaccination_guests_residential_care_home,\
							'fascia_anagrafica', 'categoria_operatori_sanitari_sociosanitari', 'categoria_personale_non_sanitario', 'categoria_ospiti_rsa', )
	count = save_figure(figure_name = "fascia_anagrafica-categoria_operatori_sanitari_sociosanitari-categoria_personale_non_sanitario-categoria_ospiti_rsa.png",\
						latest_update = latest_update, figure = figure, count = count)	
	
	# get total vaccinations for other people, armed forces and school personnel
	xdata = get_string_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'fascia_anagrafica'))	
	total_vaccination_other_people = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_altro'))
	total_vaccination_armed_forces = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_forze_armate'))
	total_vaccination_school_personnel = get_data_list(anagrafica_vaccini, get_index_from_column_name(metadata_anagrafica_vaccini, 'categoria_personale_scolastico'))
	
	# plot total vaccinations for other people, armed forces and school personnel
	figure = plot_bar_3data(xdata, total_vaccination_other_people, \
							total_vaccination_armed_forces, total_vaccination_school_personnel,\
							'fascia_anagrafica', 'categoria_altro', 'categoria_forze_armate', 'categoria_personale_scolastico')
	count = save_figure(figure_name = "fascia_anagrafica-categoria_altro-categoria_forze_armate-categoria_personale_scolastico.png",\
						latest_update = latest_update, figure = figure, count = count)	
	'''		

	# read somministrazioni-vaccini-latest.csv
	somministrazioni_vaccini, metadata_somministrazioni_vaccini = csv_reader('somministrazioni-vaccini-latest.csv')
	
	# get latest update of the csv 'somministrazioni-vaccini-latest.csv'
	latest_update = somministrazioni_vaccini[len(somministrazioni_vaccini) - 1][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")]

	# get name of supplier, area and age_group
	supplier = get_string_list(somministrazioni_vaccini, get_index_from_column_name(metadata = metadata_somministrazioni_vaccini, column_name = "fornitore"))
	area = get_string_list(somministrazioni_vaccini, get_index_from_column_name(metadata = metadata_somministrazioni_vaccini, column_name = "area"))
	age_group = get_string_list(somministrazioni_vaccini, get_index_from_column_name(metadata = metadata_somministrazioni_vaccini, column_name = "fascia_anagrafica"))
	
	# get total administered doses over time
	cumulative_data_italy = []
	days = []
	for i in range(1, len(somministrazioni_vaccini)):
		cumulative_data_italy, days = get_cumulative_data(data = cumulative_data_italy, \
														  new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_maschile")])\
														  + (float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_femminile")])), \
														  days = days, \
														  day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
	
	# plot total administered doses over time
	if (cumulative_data_italy[len(cumulative_data_italy)-1] != 0):
		figure = plot_line_1data(xdata = days, ydata = cumulative_data_italy, xlabel = 'Giorni', ylabel = "Totale dosi somministrate")
		count = save_figure(figure_name = "giorni-dosi_totali.png",\
					latest_update = latest_update, figure = figure, count = count)	
	
	# get daily administered doses over time
	daily_data_italy = get_daily_data_from_cumulative_data(cumulative_data_italy)
	
	# plot daily administered doses over time
	if (daily_data_italy[len(daily_data_italy)-1] != 0):
		figure = plot_line_1data(xdata = days, ydata = daily_data_italy, xlabel = 'Giorni', ylabel = "Dosi somministrate quotidianamente")
		count = save_figure(figure_name = "giorni-dosi_giornaliere.png",\
					latest_update = latest_update, figure = figure, count = count)	
					
	# get the number of doses administered today
	doses_administered_today = int(daily_data_italy[len(daily_data_italy)-1])	# last daily_data_italy are the doses administered today
	print("Administered doses today (" + latest_update+"): " + str(doses_administered_today))
	
	# get total administered doses for each age group over time
	for j in range (0, len(age_group)):
		cumulative_data_italy_by_age_group = []
		days = []
		for i in range(1, len(somministrazioni_vaccini)):
			if(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "fascia_anagrafica")]\
			   == age_group[j]):
				cumulative_data_italy_by_age_group, days = get_cumulative_data(data = cumulative_data_italy_by_age_group, \
																		   new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_maschile")])\
																		   + (float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_femminile")])), \
																		   days = days, \
																		   day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
		
		# plot total administered doses for each age group over time
		if (cumulative_data_italy_by_age_group[len(cumulative_data_italy_by_age_group)-1] != 0):
			figure = plot_line_1data(xdata = days, ydata = cumulative_data_italy_by_age_group, xlabel = 'Giorni', ylabel = "Dosi somministrate fascia anagrafica " + age_group[j])
			count = save_figure(figure_name = "giorni-fascia_anagrafica-" + age_group[j] + ".png",\
					latest_update = latest_update, figure = figure, count = count)	
		
	# get total administered doses for each supplier over time
	for j in range (0, len(supplier)):
		cumulative_data_italy_by_supplier = []
		days = []
		for i in range(1, len(somministrazioni_vaccini)):
			if(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "fornitore")]\
			   == supplier[j]):
				cumulative_data_italy_by_supplier, days = get_cumulative_data(data = cumulative_data_italy_by_supplier, \
																		   new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_maschile")])\
																		   + (float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "sesso_femminile")])), \
																		   days = days, \
																		   day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
		
		# plot total administered doses for each supplier over time
		if (cumulative_data_italy_by_supplier[len(cumulative_data_italy_by_supplier)-1] != 0):
			figure = plot_line_1data(xdata = days, ydata = cumulative_data_italy_by_supplier, xlabel = 'Giorni', ylabel = "Dosi somministrate fornitore " + supplier[j])
			count = save_figure(figure_name = "giorni-fornitore-" + supplier[j].replace('/', '-') + ".png",\
					latest_update = latest_update, figure = figure, count = count)	
		
	# get total first doses over time
	first_doses_italy = []
	days_first_doses_italy = []
	for i in range(1, len(somministrazioni_vaccini)):
		first_doses_italy, days_first_doses_italy = get_cumulative_data(data = first_doses_italy, \
													  new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "prima_dose")]),\
													  days = days_first_doses_italy,\
													  day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
	
	# get total second doses over time
	second_doses_italy = []
	days_second_doses_italy = []
	for i in range(1, len(somministrazioni_vaccini)):
		second_doses_italy, days_second_doses_italy = get_cumulative_data(data = second_doses_italy, \
													  new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "seconda_dose")]),\
													  days = days_second_doses_italy, \
													  day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])

	# plot total first and second doses administered over time
	if ((first_doses_italy[len(first_doses_italy)-1] != 0) and (second_doses_italy[len(second_doses_italy)-1] != 0)):
		figure = plot_line_2data(xdata1 = days_first_doses_italy, xdata2 = days_second_doses_italy,\
								 ydata1 = first_doses_italy, ydata2 = second_doses_italy,\
								 xlabel = 'Giorni', ylabel1 = 'prima dose', ylabel2 = 'seconda dose')
								 
		count = save_figure(figure_name = "giorni-prima_dose-seconda_dose.png",\
							latest_update = latest_update, figure = figure, count = count)	
		
		figure, axes = initialize_figure(days_first_doses_italy, 'Giorni', 'prima dose, seconda dose', len(xdata))
		figure = bar_plot(figure, axes, days_first_doses_italy, first_doses_italy, 'prima dose', 0.8, 0, list(np.zeros(len(days_first_doses_italy))), False)
		figure = bar_plot(figure, axes, days_first_doses_italy, second_doses_italy, 'seconda dose', 0.8, 0, first_doses_italy, False)	
		axes.legend()
		axes.text(x = len(days_first_doses_italy), \
				  y = first_doses_italy[len(days_first_doses_italy) - 1], \
				  s = str(int(first_doses_italy[len(days_first_doses_italy) - 1])))
		axes.text(x = len(days_first_doses_italy), \
				  y = first_doses_italy[len(days_first_doses_italy) - 1] + second_doses_italy[len(days_first_doses_italy) - 1], \
				  s = str(int(first_doses_italy[len(days_first_doses_italy) - 1] + second_doses_italy[len(days_first_doses_italy) - 1])))
		
		count = save_figure(figure_name = "giorni-prima_dose-seconda_dose-barre.png",\
								latest_update = latest_update, figure = figure, count = count)	
	
	# get total additional doses over time
	additional_doses_italy = []
	days_additional_doses_italy = []
	for i in range(1, len(somministrazioni_vaccini)):
		additional_doses_italy, days_additional_doses_italy = get_cumulative_data(data = additional_doses_italy, \
													  new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "dose_addizionale_booster")]),\
													  days = days_additional_doses_italy, \
													  day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
	# plot total additional doses over time
	if (additional_doses_italy[len(additional_doses_italy)-1] != 0):
		figure = plot_line_1data(xdata = days_additional_doses_italy, ydata = additional_doses_italy, xlabel = 'Giorni', ylabel = "Dosi aggiuntive somministrate")
		count = save_figure(figure_name = "giorni-dose-aggiuntiva.png",\
				latest_update = latest_update, figure = figure, count = count)	
					
	# get previous infections over time
	previous_infections_italy = []
	days_previous_infections_italy = []
	for i in range(1, len(somministrazioni_vaccini)):
		previous_infections_italy, days_previous_infections_italy = get_cumulative_data(data = previous_infections_italy, \
													  new_element = float(somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "pregressa_infezione")]),\
													  days = days_previous_infections_italy, \
													  day_of_administration = somministrazioni_vaccini[i][get_index_from_column_name(metadata_somministrazioni_vaccini, "data_somministrazione")])
	# plot total previous infections over time
	if (previous_infections_italy[len(previous_infections_italy)-1] != 0):
		figure = plot_line_1data(xdata = days_previous_infections_italy, ydata = previous_infections_italy, xlabel = 'Giorni', ylabel = "Pregressa infezione")
		count = save_figure(figure_name = "giorni-pregressa-infezione.png",\
				latest_update = latest_update, figure = figure, count = count)	
					
	if SAVING_CHARTS_ENABLED:
		print (count, "charts saved.")
		
	if SHOW_CHARTS_ENABLED:
		plt.show()
	
	if (readme_autoupdate.create_readme("base_readme.txt", latest_update) == True):
		print("README.md updated.")
		
	if (gitignore_autoupdate.update_gitignore(".gitignore", latest_update) == True):
		print (".gitignore updated.")
		
	tweet_link = twitter.post_tweet("twitter_key.txt", latest_update, total_doses_administered, total_doses_delivered, doses_administered_today)
	print("Your tweet has been posted: " + str(tweet_link))
	
if __name__ == "__main__":
    main()
