import requests
import xmltodict


def actuele_vertrektijden_api(stationToQuery):
    'takes a station, calls to the API and returns the response'
    'The response will be all the departing trains of the station with time and railtrack'

    # making contact with the API
    auth_details = ('pixelpulp4@gmail.com', 'zdRThsCcDsXBFsIxycTU2uWcctPd1W_50xRICdSN6vZUIfAm987U5g')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station={0}'.format(stationToQuery)

    try:
        # Tries to get the information from the API and return it.
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML
    except Exception as e:
        print("Something has gone wrong: {0}".format(e))


def reisadvies_api(beginStation, endStation, isDeparture, dateManual, dateTime):
    'Takes info of the desired route, calls the API and returns the response'
    '@:parameter if dateManual = True, set a manual time e.g.(2012-02-21T15:50); else wise dateTime is set automatically'
    '@:parameter isDeparture is True if you\'re dealing with a departure, False elsewise'

    # making contact with the API
    auth_details = ('pixelpulp4@gmail.com', 'zdRThsCcDsXBFsIxycTU2uWcctPd1W_50xRICdSN6vZUIfAm987U5g')
    api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={0}&toStation={1}&Departure={2}&nextAdvices=8'.format(beginStation, endStation, isDeparture)
    try:
        if dateManual:
        # put a different time at the end of the url
            api_url += "&".format(dateTime)
        response = requests.get(api_url, auth=auth_details)
    except:
        print("dateTime is not correct")
        response = requests.get(api_url, auth=auth_details)

    try:
        # tries to saves the response in 'vertrekXML' and return it
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML
    except Exception as e:
        print("Something has gone wrong: {0}".format(e))


def storingen_api(stationToQuery):
    'Takes a beginStation and calls the API for all the actual storingen'

    # making contact with the API
    auth_details = ('pixelpulp4@gmail.com', 'zdRThsCcDsXBFsIxycTU2uWcctPd1W_50xRICdSN6vZUIfAm987U5g')
    api_url = 'http://webservices.ns.nl/ns-api-storingen?station={0}&actual=True&unplanned=False'.format(stationToQuery)
    response = requests.get(api_url, auth=auth_details)

    try:
        # tries to save the response in 'prijsXML' and return it
        storingenXML = xmltodict.parse(response.text)
        return storingenXML
    except Exception as e:
        print("Something has gone wrong: {0}".format(e))


def stationLijst_api():
    'Calls to the API for all the stationnames and the response will be all existing stations with its info'

    # making contact with the API
    auth_details = ('pixelpulp4@gmail.com', 'zdRThsCcDsXBFsIxycTU2uWcctPd1W_50xRICdSN6vZUIfAm987U5g')
    api_url = 'http://webservices.ns.nl/ns-api-stations-v2'
    response = requests.get(api_url, auth=auth_details)

    try:
        # tries to save the response in 'stationsXML' and return it
        stationsXML = xmltodict.parse(response.text)
        return stationsXML
    except Exception as e:
        print("Something has gone wrong: {0}".format(e))
