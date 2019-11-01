import json
choices = ("athlete", "coach", "exit")

#ToDo: move to Schedule Class
days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
times = ("morning", "lunch", "day", "evening", "exit")

class AthleteManager:
    def __init__(self):
        self.athletes = []

    def loadAthletesDataFromJSON(self):
        with open("main.json") as data_file:
            data = json.load(data_file)["ID"]
            for key in data:
                athlete = Athlete(key, data[key])
                self.athletes.append(athlete)

    def saveAthletesDataToJSON(self):
        json = {}
        json["ID"] = {}
        for athlete in self.athletes:
            json["ID"][athlete.ID] = athlete.getJSON()

        file = open("main.json", "w")
        file.write(json.dumps(json))
        file.close()

    def getAthlete(self, ID):
        for athlete in self.athletes:
            if athlete.ID == ID:
                return athlete

        print("The athlete does not exist")
        return None

    def getAthleteIDs(self):
        athleteIDs = []
        for athlete in self.athletes:
            athleteIDs.append(athlete.ID)

        return athleteIDs

class Athlete:

    athlete_choices = ("creation", "check", "exit")

    def __init__(self, ID, data):
        self.ID = ID
        self.name = data["name"]
        self.surname = data["surname"]
        self.birthdate = data["birthdate"]
        self.gender = data["gender"]
        self.workout = data["workout"]
        self.feedback = data["feedback"]

    def getJSON(self):
        json = {}
        json["name"] = self.name
        json["surname"] = self.surname
        json["birthdate"] = self.birthdate
        json["gender"] = self.gender
        json["workout"] = self.workout
        json["feedback"] = self.feedback
        return json

    def printProfile(self):
        print("\nProfile of", self.ID, "\n-------------------------""\nName:", self.name, self.surname, "\nAge:", self.birthdate,
              "\nGender:", self.gender)

    def checkProfile(self):
        x = True
        while x == True:
            answer = input("\nWould you like to check workouts (yes, no): ")
            if answer == "yes":
                feedback_answer = self.getWorkout()
                if feedback_answer == 1:
                    pass
                    #self.createFeedback()
                #ToDo: callanother method
            elif answer == "no":
                x = False
            else:
                print("Please try again")
        return False

    def getWorkout(self):
        week = "x"
        while week not in self.workout.keys():
            week = input(str("\nInput week (" + (", ").join(self.workout.keys()) + "): "))
            if week not in self.workout.keys():
                print("That does not exist, try again")
            else:
                day = "x"
                while day not in days:
                    day = input(str("Input day (" + (", ").join(days) + "): "))
                    print("")
                    if day not in days:
                        print("That does not exist, try again")
                    else:
                        count = 0
                        for key in self.workout[week][day]:
                            if self.workout[week][day][key] == -1:
                                print(key, ":", "no excerisize for this time of day")
                                count = count + 1
                            else:
                                print(key, ":", self.workout[week][day][key]["type"], "for",
                                      self.workout[week][day][key]["minutes"],
                                      "minutes and",
                                      self.workout[week][day][key]["distance"], "kilometers, at a",
                                      self.workout[week][day][key]["load"],
                                      "load")
                        self.week = week
                        self.day = day
                        if count < 4:
                            x = True
                            while x == True:
                                answer = input("\nWould you like to add feedback (yes, no): ")
                                if answer == "yes":
                                    return 1
                                elif answer == "no":
                                    return 0
                                else:
                                    print("Please try again")
                        else:
                            print("\nNo workouts for this day, cannot add feedback")


def main():
    athleteManager = AthleteManager()
    athleteManager.loadAthletesDataFromJSON()

    choice = "x"
    print("\nETPG® | The training schedule program for any endurance trainer and athletes")
    while (choice not in choices) or choice != "exit":
        choice = str(input("\nGeneral Menu | Choose any of the following options (" + (", ").join(choices) + "): "))
        if (choice not in choices):
            print("Invalid input, try again")
        elif (choice == "athlete"):
            y=True
            while y == True:
                answer =input("\nAthlete Menu | Choose an option to edit (" + (", ").join(Athlete.athlete_choices) + "): ")
                if answer =="check":
                    x = True
                    while x == True:
                        ID = input(
                "\nList of Athletes | Choose a username to check info (" + (", ").join(athleteManager.getAthleteIDs()) + ", or exit): ")
                        athlete = athleteManager.getAthlete(ID)
                        if athlete != None:
                            athlete.printProfile()
                            athlete.checkProfile()
                        else:
                            x = False
                elif answer =="creation":
                    #Athlete.createAthlete()
                    #ToDo:implement later
                    pass
                elif answer =="exit":
                    y = False
                else:
                    print("Invalid input, please try again")

        elif (choice == "coach"):
            pass
            #ToDo:implement later

main()
