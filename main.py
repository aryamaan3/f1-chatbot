import requests
import json
import spacy

# Define a function to extract the relevant information from the JSON data
def extract_data():
    url = "https://ergast.com/api/f1/current.json"
    response = requests.get(url)
    data = json.loads(response.text)

    races = data["MRData"]["RaceTable"]["Races"]

    circuits = []
    for race in races:
        circuit = race["Circuit"]
        circuits.append([circuit["circuitId"], circuit["circuitName"], circuit["Location"]["locality"], circuit["Location"]["country"]])

    url = "http://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    data = json.loads(response.text)

    standings = []
    drivers = []
    teams = {}
    for driver in data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:
        standings.append([driver["position"], driver["Driver"]["givenName"], driver["Driver"]["familyName"], driver["Constructors"][0]["name"], driver["points"]])
        drivers.append([driver["Driver"]["driverId"], driver["Driver"]["givenName"], driver["Driver"]["familyName"], driver["Constructors"][0]["name"]])
        if driver["Constructors"][0]["name"] in teams:
            teams[driver["Constructors"][0]["name"]].append([driver["Driver"]["driverId"], driver["Driver"]["givenName"], driver["Driver"]["familyName"]])
        else:
            teams[driver["Constructors"][0]["name"]] = [[driver["Driver"]["driverId"], driver["Driver"]["givenName"], driver["Driver"]["familyName"]]]

    return races, standings, drivers, teams, circuits

# Extract the race schedule from the JSON data
races, standings, drivers, teams, circuits = extract_data()

# print("Races :", races)
# print("\n------------------------\n")
# print("Standings :", standings)
# print("\n------------------------\n")
# print("Drivers :", drivers)
# print("\n------------------------\n")
# print("Teams :", teams)
# print("\n------------------------\n")
# print("Circuits :", circuits)

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")


# Define a function to extract the relevant information from a user request
def extract_info(text):
    doc = nlp(text)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    # Check if the user is asking for the race schedule
    if "schedule" in [token.text.lower() for token in doc]:
        return get_race_schedule()
    # Check if the user is asking for race results
    elif "standings" in [token.text.lower() for token in doc]:
        return standings()

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text:
                return get_driver_info(ent.text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            if ent.text:
                return get_team_info(ent.text)
    
    for ent in doc.ents:
        if ent.label_ in ["LOC", "FAC"]:
            if ent.text:
                return get_circuit_info(ent.text)

    # If the user's request doesn't match any of the above categories, return a default response
    else:
        return "I'm sorry, I didn't understand your request. Please try again."

# Define a function to generate a response to a user query
def get_race_schedule():
    # Construct a string with information on each upcoming race
    race_info = ""
    for race in races:
        round_number = race["round"]
        race_name = race["raceName"]
        date = race["date"]
        time = race["time"]
        location = race["Circuit"]["Location"]["country"]
        race_info += f"Round {round_number}: {race_name} on {date} at {time} in {location}\n"

    # Construct the final response string
    response = f"The race schedule for the current season is:\n{race_info}"
    return response

# Define a function to generate a response to a user query for race results
def standings():
    race_results = "Race results todo"
    return race_results

# Define a function to generate a response to a user query for driver information
def get_driver_info(driver_name):
    txt = driver_name.split()

    for t in txt:
        for d in drivers:
            if t in d:
                return f"Driver name: {d[1]} {d[2]}\nTeam: {d[3]}"
            
    return f"{driver_name} is not a Formula 1 driver in 2023."

# Define a function to generate a response to a user query for team information
def get_team_info(team_name):
    txt = team_name.split()

    for t in txt:
        for team in teams:
            if t in team:
                return f"Team name: {team}\nDrivers: {teams[team]}"
            
    return f"{team_name} is not a Formula 1 team in 2023."

# Define a function to generate a response to a user query for circuit information
def get_circuit_info(circuit_name):
    circuit_info = f"Circuit name: {circuit_name}"
    return circuit_info

print(extract_info("is Sebastian Vettel a Ferrari driver?"))
