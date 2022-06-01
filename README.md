# COVID19 Vaccination Italy

## Introduction

This Python script shows and saves some charts that explain how the COVID-19 vaccination in Italy is going. The datasets are available at [italia/covid19-opendata-vaccini](https://github.com/italia/covid19-opendata-vaccini).

## Prereqs (at least)
* [Python 3.7.9](https://www.python.org/) 
* [Matplotlib 3.4.1](https://pypi.org/project/matplotlib/)
* [Numpy 1.20.0](https://numpy.org/)
* [Tweepy 3.10.0](https://docs.tweepy.org/en/latest/)

## How to run 
1. Install matplotlib, numpy and tweepy

Open a command window and type:

`python -m pip install -U pip`

`python -m pip install -U matplotlib`

`pip install numpy`

`pip install tweepy`

2. Run

Open a command window and type `python main.py`. 

The charts are saved in [Charts](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/tree/main/Charts) directory and in a folder named as the day the charts refer to.

## The code

* [main.py](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/main.py) downloads the datasets, produces and saves the [Charts](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/tree/main/Charts).

* [twitter.py](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/twitter.py) posts a thread on Twitter account [@VacciniCovidITA](https://twitter.com/VacciniCovidITA) uploading the charts made.

* [readme_autoupdate.py](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/readme_autoupdate.py) updates the [README.md](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/README.md) with the new charts link.

* [gitignore_autoupdate.py](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/readme_autoupdate.py) updates the [.gitignore](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/.gitignore) in order to commit only the latest chart folder created.


## Charts
If `SHOW_CHARTS_ENABLED = 1`, the charts are shown in the command window. If `SAVING_CHARTS_ENABLED = 0`, the charts will not be saved.

Here are shown some charts that this script created on 2022-02-25.

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-dose-aggiuntiva.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-dosi_giornaliere.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-dosi_totali.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-05-11.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-12-19.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-20-29.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-30-39.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-40-49.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-50-59.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-60-69.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-70-79.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-80-89.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fascia_anagrafica-90+.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fornitore-Janssen.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fornitore-Moderna.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fornitore-Pfizer%20Pediatrico.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fornitore-Pfizer-BioNTech.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-fornitore-Vaxzevria%20(AstraZeneca).png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-pregressa-infezione.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-prima_dose-seconda_dose-barre.png)

![](https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy/blob/main/Charts/2022-02-25/2022-02-25-giorni-prima_dose-seconda_dose.png)

