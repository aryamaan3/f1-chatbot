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
        circuits.append(
            [
                circuit["circuitId"],
                circuit["circuitName"],
                circuit["Location"]["locality"],
                circuit["Location"]["country"],
            ]
        )

    url = "http://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    data = json.loads(response.text)

    leaderboard = []
    drivers = []
    teams = {}
    for driver in data["MRData"]["StandingsTable"]["StandingsLists"][0][
        "DriverStandings"
    ]:
        leaderboard.append(
            [
                driver["position"],
                driver["Driver"]["givenName"],
                driver["Driver"]["familyName"],
                driver["Constructors"][0]["name"],
                driver["points"],
            ]
        )
        drivers.append(
            [
                driver["Driver"]["driverId"],
                driver["Driver"]["givenName"],
                driver["Driver"]["familyName"],
                driver["Constructors"][0]["name"],
            ]
        )
        if driver["Constructors"][0]["name"] in teams:
            teams[driver["Constructors"][0]["name"]].append(
                [
                    driver["Driver"]["driverId"],
                    driver["Driver"]["givenName"],
                    driver["Driver"]["familyName"],
                ]
            )
        else:
            teams[driver["Constructors"][0]["name"]] = [
                [
                    driver["Driver"]["driverId"],
                    driver["Driver"]["givenName"],
                    driver["Driver"]["familyName"],
                ]
            ]

    return races, leaderboard, drivers, teams, circuits


# Extract the race schedule from the JSON data
races, leaderboard, drivers, teams, circuits = extract_data()

# print("Races :", races)
# print("\n------------------------\n")
# print("leaderboard :", leaderboard)
# print("\n------------------------\n")
# print("Drivers :", drivers)
# print("\n------------------------\n")
# print("Teams :", teams)
# print("\n------------------------\n")
# print("Circuits :", circuits)

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")


def extract_fuzzy_info(text):
    for word in text.split():
        if word in drivers:
            return f"Driver name: {drivers[1]} {drivers[2]}\nTeam: {drivers[3]}"
        elif word in teams:
            d1 = teams[word][0][1:]
            d2 = teams[word][1][1:]
            d1 = " ".join(d1)
            d2 = " ".join(d2)
            return f"Team name: {word}\nDrivers: {d1} and {d2}"
        elif word in circuits:
            return f"Circuit name: {circuits[1]}"

    return "I'm sorry, I didn't understand your request. Please try again."


# Define a function to extract the relevant information from a user request
def extract_info(text):
    doc = nlp(text)
    # Check if the user is asking for the race schedule
    words = text.lower().split()

    if "schedule" in words or "date" in words or "time" in words or "when" in words:
        return get_race_schedule()
    # Check if the user is asking for race results
    elif "winner" in words or "win" in words or "results" in words or "race" in words:
        return standings()

    elif "standing" in words or "standings" in words or "leaderboard" in words:
        return standings()

    for ent in doc.ents:
        # print(ent.text, ent.label_)
        if ent.label_ == "PERSON":
            if ent.text:
                return get_driver_info(ent.text)

        if ent.label_ in ["NORP", "GPE"]:
            if ent.text:
                return get_team_info(ent.text)

        if ent.label_ in ["LOC", "FAC", "GPE", "ORG"]:
            if ent.text:
                return get_circuit_info(ent.text)

        if ent.label_ == "DATE":
            # If the user asks for the race schedule for the next Grand Prix
            if "next" in words:
                # Make a request to the Ergast API to get the schedule for the next race
                response = "The race schedule for the next Grand Prix is : "
                for race in races:
                    if race["date"] >= ent.text:
                        return (
                            "The race schedule for the next Grand Prix is: "
                            + race["raceName"]
                            + " on "
                            + race["date"]
                            + "\n"
                        )

            else:
                for race in races:
                    if race["date"] >= ent.text:
                        return (
                            "The next race is : "
                            + race["raceName"]
                            + " on "
                            + race["date"]
                        )

    return extract_fuzzy_info(text)


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
        race_info += (
            f"Round {round_number}: {race_name} on {date} at {time} in {location}\n"
        )

    # Construct the final response string
    response = f"The race schedule for the current season is:\n{race_info}"
    return response


# Define a function to generate a response to a user query for race results
def standings():
    race_results = "F1 2023 Standings:\n"

    for driver in leaderboard:
        race_results += (
            f"{driver[0]}: {driver[1]} {driver[2]} - {driver[3]} - {driver[4]} points\n"
        )

    return race_results


# Define a function to generate a response to a user query for driver information
def get_driver_info(driver_text):
    url = (
        "http://ergast.com/api/f1/drivers/"
        + driver_text.lower().replace(" ", "_")
        + "/career.json"
    )
    response_json = requests.get(url).json()
    seasons = response_json["MRData"]["CareerTable"]["Seasons"]
    for season in seasons:
        response += season["season"] + ": " + season["Constructor"]["name"] + "\n"

    return response


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
    for t in circuit_name.split():
        for c in circuits:
            if t in c:
                return f"Circuit name: {c[1]}\nLocation: {c[2]}, {c[3]}"

    return f"{circuit_name} is not a Formula 1 circuit in 2023."


def handle_input():
    print(
        "Welcome to F1 chatbot! Ask me about the current season's schedule, standings, drivers, teams or circuits."
    )
    while True:
        # Prompt the user to input a message
        message = input("You: ")
        # Check if the user has said goodbye
        if message in ["bye", "goodbye", "exit"]:
            print("Chatbot: Bye!")
            break
        # Extract the relevant information from the user's message
        response = extract_info(message)
        # Print the chatbot's response
        print("Chatbot:", response)


if __name__ == "__main__":
    handle_input()
