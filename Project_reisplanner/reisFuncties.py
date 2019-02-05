import requests
import xmltodict
import tkinter as Tkint
from tkinter import *


def reisPlannen(beginStation, eindStation):
    'Ask the API for the treinplanning between two stations'
    # making contact with the API
    auth_details = ('pixelpulp4@gmail.com', 'zdRThsCcDsXBFsIxycTU2uWcctPd1W_50xRICdSN6vZUIfAm987U5g')
    api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={0}&toStation={1}&departure=True'.format(
        beginStation, eindStation)
    response = requests.get(api_url, auth=auth_details)

    # saves the response in 'vertrekXML'
    vertrekXML = xmltodict.parse(response.text)
    return vertrekXML


class ReisInfo:
    def __init__(self, beginStat, eindStat, vertrekTijd, aankomstTijd, overStap, reisTijd):
        self.beginStat = beginStat
        self.eindStat = eindStat
        self.vertrekTijd = vertrekTijd
        self.aankomstTijd = aankomstTijd
        self.overStap = overStap
        self.reisTijd = reisTijd

    def writeInfo(self, direction):
        'sets up the frames with the info of reismogelijkheden'
        infoFrame = Tkint.Frame(master=direction,  # setting the frame
                                background="white",
                                borderwidth=1,
                                relief="solid")
        infoFrame.pack(side=TOP, padx=4, pady=(30, 0))

        # writes the  to the frame
        travelTime = Tkint.Label(master=infoFrame,
                                 text='reistijd: {0}'.format(self.reisTijd),
                                 foreground='#003067',
                                 background="white",
                                 font=('Helvetica', 12))
        travelTime.pack(side="right", pady=10, padx=10)

        # writes the vertrekTijd en aankomstTijd to the frame
        dateTime = Tkint.Label(master=infoFrame,
                               text='{0} -> {1}'.format(self.vertrekTijd, self.aankomstTijd),
                               foreground='#003067',
                               background="white",
                               font=('Helvetica', 12))
        dateTime.pack(side="right", pady=5, padx=10)

        # writes the begin and end station to the frame
        stations = Tkint.Label(master=infoFrame,
                               text='{0} -> {1}'.format(self.beginStat, self.eindStat),
                               foreground='#003067',
                               background="white",
                               font=('Helvetica', 12))
        stations.pack(side="left", pady=5, padx=10)

        # vertrek en aankomsttation kort samengevat
        planning = Tkint.Label(infoFrame,
            text='Reis van {0} naar {1}:'.format(self.beginStat, self.eindStat),
            foreground='#003067',
            background="white",
            font=('Helvetica', 14))
        planning.pack(side="left", pady=5, padx=10)
        planning.place(x=130, y=267)