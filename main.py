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
        json_all = {}
        json_all["ID"] = {}
        for athlete in self.athletes:
            json_all["ID"][athlete.ID] = athlete.getJSON()

        file = open("main.json", "w")
        file.write(json.dumps(json_all))
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

    def addNewAthlete(self):
        ID = input("\nInput a username: ")
        name = input("Input your first name: ")
        surname = input("Input your surname: ")
        birthdate = input("Input your birthdate: ")
        z = True
        while z == True:
            gender = input("Input your gender (male, female): ")
            if gender != "male" and gender != "female":
                print("Invalid input, please use either male or female")
            else:
                z = False

        data= {"ID":{ID:{"name": name, "surname": surname, "birthdate": birthdate, "workout": {"week1": {}},
                          "feedback": {}}}}
        data["ID"][ID]["name"] = name
        data["ID"][ID]["surname"] = surname
        data["ID"][ID]["birthdate"] = birthdate
        data["ID"][ID]["gender"] = gender
        data["ID"][ID]["workout"]["week1"] = {"day1": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day2": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day3": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day4": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day5": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day6": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                              "day7": {"morning": -1, "lunch": -1, "day": -1, "evening": -1}}
        print("\nAthlete", ID, "(", name, surname, ") who is a", birthdate, "year old", gender, "has been created")
        athlete = Athlete(ID, data["ID"][ID])
        self.athletes.append(athlete)

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
        self.count = 0
        for key in self.feedback:
            self.count +=1

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
                    self.createFeedback()
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

    def createFeedback(self):
        time_answer = "x"
        while time_answer not in times or time_answer != exit:
            time_answer = input(
                "\nChoose one of the following options for " + self.day + " in " + self.week + " (" + (", ").join(
                    times) + "): ")
            if time_answer not in times:
                print("That does not exist, try again")
            elif time_answer == "exit":
                return 0
            else:
                if self.workout[self.week][self.day][time_answer] == -1:
                    print("No workout for this time of day, cannot provide feedback")
                else:
                    ifDone = "x"
                    while (ifDone != "yes" and ifDone != "no"):
                        ifDone = str(input("Have you completed the workout? yes/no: "))
                        if (ifDone != "yes" and ifDone != "no"):
                            print("Invalid input, try again")
                    text_feedback = input(
                        "Input feedback (if you did the workout how you felt, if not why): ")
                    self.count = self.count + 1
                    self.feedback[self.count] = {
                        self.week: {self.day: {time_answer: {}, "hasCompleted": {}, "feedback": {}}}}
                    self.feedback[self.count][self.week][self.day][time_answer] = self.workout[self.week][self.day][
                        time_answer]
                    self.feedback[self.count][self.week][self.day]["hasCompleted"] = ifDone
                    self.feedback[self.count][self.week][self.day]["feedback"] = text_feedback
                    self.feedback[self.count][self.week][self.day]["resolved"] = "no"
                    print("\nFeedback added for", time_answer, "during", self.day, "in", self.week)

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
                            athleteManager.saveAthletesDataToJSON()
                        else:
                            x = False
                elif answer =="creation":
                    while True:
                        answer = input(
                            "\nAthlete Profile Creation | Choose an option for users? (create, delete, exit): ")
                        if answer == "create":
                            athleteManager.addNewAthlete()
                            athleteManager.saveAthletesDataToJSON()
                        elif answer == "delete":
                            #athleteManager.deleteAthlete()
                            #athleteManager.saveAthletesDataToJSON()
                            break
                        elif answer == "exit":
                            break
                        else:
                            print("Invalid input, please try again")
                elif answer =="exit":
                    y = False
                else:
                    print("Invalid input, please try again")

        elif (choice == "coach"):
            pass
            #ToDo:implement later

main()