import json
choices = ("athlete", "coach", "exit")
days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
times = ("morning", "lunch", "day", "evening", "exit")
replies_week = ("add", "remove", "exit")
loads = ("easy", "medium", "hard")
replies_workout = ("edit", "remove", "exit")
sports = {"swimming", "cycling", "running"}

class LinkedList:

    def __init__(self):
        self.head= None

    def addAsLast(self,node):
        if self.head ==None:
            self.head = node
        else:
            tmp =self.head
            while(tmp.next != None):
                tmp = tmp.next

            tmp.next = node

    def find(self,ID):
        tmp = self.head
        while (tmp!=None):
            if tmp.isEqual(ID):
                return tmp
            tmp = tmp.next
        return None

    def convertToJson(self):
        json_all = {}
        json_all["ID"] = {}
        tmp = self.head
        while (tmp != None):
            json_all["ID"][tmp.ID] = tmp.getJSON()
            tmp = tmp.next
        return json_all

    def saveIDs(self):
        athleteIDs = []
        tmp = self.head
        while (tmp != None):
            athleteIDs.append(tmp.ID)
            tmp = tmp.next
        return athleteIDs

    def removeUser(self, ID):
            previous_node = None
            current_node = self.head
            while current_node:
                if current_node.ID == ID:
                    if previous_node:
                        previous_node.next = current_node.next
                    else:
                        self.head = current_node.next
                    return True
                previous_node = current_node
                current_node = current_node.next
            return False

class AthleteManager:
    def __init__(self):
        self.athletes = LinkedList()

    def loadAthletesDataFromJSON(self):
        with open("main.json") as data_file:
            data = json.load(data_file)["ID"]
            for key in data:
                athlete = Athlete(key, data[key])
                self.athletes.addAsLast(athlete)

    def saveAthletesDataToJSON(self):
        json_all = self.athletes.convertToJson()
        file = open("main.json", "w")
        file.write(json.dumps(json_all))
        file.close()

    def getAthlete(self, ID):
        athlete = self.athletes.find(ID)
        if athlete.ID == ID:
            return athlete
        elif ID == "exit":
            return None

        print("The athlete does not exist")
        return None

    def getAthleteIDs(self):
        athleteIDs=self.athletes.saveIDs()
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
        self.athletes.addAsLast(athlete)

    def deleteAthlete(self,ID):
        found = self.athletes.removeUser(ID)
        if found:
            print(ID,"has been removed")
            return None
        else:
            print("The athlete does not exist")
            return None

class Athlete:

    athlete_choices = ("creation", "check", "exit")
    coach_choices = ("week", "workout", "feedback", "exit")

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
        self.next = None

    def isEqual(self, ID):
        return self.ID == ID

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

    def editProfile(self):
        x = True
        while x == True:
            answer = input("\nWould you like to edit this user (yes, no): ")
            if answer == "yes":
                return 1
            elif answer == "no":
                return 0
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

    def editWeek(self):
        reply = "x"
        print("\nCurrent weeks in schedule :(" + (", ").join(self.workout.keys()) + ")")
        while (reply not in replies_week) or reply != "exit":
            count = 1
            for key in self.workout:
                count = count + 1
            reply = str(input("\nWhat would you like to do with the weeks (" + (", ").join(replies_week) + "): "))
            if (reply not in replies_week):
                print("Invalid input, try again")

            if (reply == "add"):
                count = str(count)
                print("\nweek" + count, "has been added\n")
                self.workout["week" + count] = {"day1": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day2": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day3": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day4": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day5": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day6": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day7": {"morning": -1, "lunch": -1, "day": -1, "evening": -1}}
            if (reply == "remove"):
                count = int(count) - 1
                count = str(count)
                print("\nweek" + count, "has been removed\n")
                del self.workout["week" + count]

    def editWorkout(self):
        week = "x"
        while week not in self.workout.keys():
            week = input(str("\nInput week (" + (", ").join(self.workout.keys()) + "): "))
            if week not in self.workout.keys():
                print("That does not exist, try again")
            else:
                day = "x"
                while day not in days:
                    day = input(str("Input day (" + (", ").join(days) + "): "))
                    if day not in days:
                        print("That does not exist, try again")

        week_schedule = self.workout[week][day]
        print("\nCurrently looking at workouts on", day, "in", week, "\n")
        for key in week_schedule:
            if week_schedule[key] == -1:
                print(key, ":", "no excerisize for this time of day")
            else:
                print(key, ":", week_schedule[key]["type"], "for", week_schedule[key]["minutes"], "minutes and",
                      week_schedule[key]["distance"], "kilometers, at a", week_schedule[key]["load"], "load")
        time = "x"
        while (time not in times) or time != "exit":
            time = input(str("\nInput time of day (" + (", ").join(times) + "): "))
            if time not in times and time != "exit":
                print("That does not exist, try again")
            elif time == "exit":
                continue
            else:
                if (week_schedule[time] == -1):
                    print("No workout planned for", time)
                reply = "x"
                while (reply not in replies_workout):
                    reply = str(
                        input("\nChoose an option to perform on this workout (" + (", ").join(replies_workout) + "): "))
                    if (reply not in replies_workout):
                        print("Invalid input, try again")

                    elif (reply == "remove"):
                        if (week_schedule[time] == -1):
                            print("\nThe time:", time, "is already empty")
                        else:
                            self.workout[week][day][time] = -1
                            print("\nWorkout during", time, "on", day, "in", week, "has been removed")

                    elif (reply == "edit"):
                        sport = "x"
                        load = "x"
                        while (sport not in sports):
                            sport = str(input("\nChoose sport type (" + (", ").join(sports) + "): "))
                            if (sport not in sports):
                                print("Invalid input, try again")

                        isMinutesSet = False
                        while (not isMinutesSet):
                            minutes = input("Input amount of time in minutes from 0 to 240: ")
                            try:
                                minutes = float(minutes)
                                if (minutes > 0 and minutes <= 240):
                                    isMinutesSet = True
                                else:
                                    print(
                                        "Wrong Input: Please type a positive integer number above 0 and below 240")
                            except ValueError:
                                print("Wrong Input: Please input a number")

                        isDistanceSet = False
                        while (not isDistanceSet):
                            distance = input("Input the distance in kilometers from 0 to 200: ")
                            try:
                                distance = float(distance)
                                if (distance > 0 and distance <= 200):
                                    isDistanceSet = True
                                else:
                                    print(
                                        "Wrong Input: Please type a positive integer number above 0 and below 200")
                            except ValueError:
                                print("Wrong Input: Please input a number")

                        while (load not in loads):
                            load = str(input("Choose load (" + (", ").join(loads) + "): "))
                            if (load not in loads):
                                print("Invalid input, try again")
                        self.workout[week][day][time] = {"type": sport, "minutes": minutes,"distance": distance, "load": load}
                        print("Workout created during", time, "on", day, "in", week, ":",self.workout[week][day][time]["type"], "for",self.workout[week][day][time]["minutes"], "minutes and",self.workout[week][day][time]["distance"], "kilometers, at a",self.workout[week][day][time]["load"], "load")

    def checkFeedback(self):
        numbers = []
        print("\nFeedback Menu | Following data sent by athlete\n")
        count = 1
        for key in self.feedback:
            week = list(self.feedback[key].keys())[0]
            day = list(self.feedback[key][week].keys())[0]
            time = list(self.feedback[key][week][day].keys())[0]
            type = self.feedback[key][week][day][time]["type"]
            minutes = self.feedback[key][week][day][time]["minutes"]
            distance = self.feedback[key][week][day][time]["distance"]
            load =self.feedback[key][week][day][time]["load"]
            hasCompleted = self.feedback[key][week][day]["hasCompleted"]
            feedback = self.feedback[key][week][day]["feedback"]
            resolved = self.feedback[key][week][day]["resolved"]

            if (resolved == "no"):
                if hasCompleted == "no":
                    print(count, ")", "In", week, "on", day, "during the", time,
                          "the athlete did not perform the workout of", type, "for",
                          minutes, "minutes and", distance, "kilometers on a", load, "load")
                    print("    Feedback:", feedback)
                    numbers.append(str(count))
                else:
                    print(count, ")", "In", week, "on", day, "during the", time, "the athlete performed the workout of",
                          type, "for",
                          minutes, "minutes and", distance, "kilometers on a", load, "load")
                    print("    Feedback:", feedback)
                    numbers.append(str(count))
                count = count + 1
            if (resolved == "yes"):
                if hasCompleted == "no":
                    print(count, ")", "RESOLVED | ", "In", week, "on", day, "during the", time,
                          "the athlete did not perform the workout of", type, "for",
                          minutes, "minutes and", distance, "kilometers on a", load, "load")
                    print("    Feedback:", feedback)

                else:
                    print(count, ")", "RESOLVED | ", "In", week, "on", day, "during the", time,
                          "the athlete performed the workout of", type, "for",
                          minutes, "minutes and", distance, "kilometers on a", load, "load")
                    print("    Feedback:", feedback)
                count = count + 1
        ask = "x"
        while (ask != "yes" or ask != "no") and ask != "no" and len(numbers) != 0:
            ask = str(input("\nWould you like to resolve a feedback (yes, no): "))
            if (ask != "yes" and ask != "no"):
                print("Invalid input, try again")
            elif (ask == "yes"):
                number = "x"
                while (number not in numbers):
                    number = str(input("\nChoose a workout (" + (", ").join(numbers) + "): "))
                    if (number not in numbers):
                        print("Invalid input, try again")
                placeholder2 = list(self.feedback.keys())[int(number) - 1]
                week = list(self.feedback[placeholder2].keys())[0]
                day = list(self.feedback[placeholder2][week].keys())[0]
                self.feedback[placeholder2][week][day]["resolved"] = "yes"
                print("Workout in", week, "on", day, "during the", time, "of", type, "for",
                      minutes, "minutes and", distance, "kilometers on a", load, "load, has been resolved")
                numbers.remove(number)

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
                        if ID != "exit":
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
                            ID = input(
                                "\nList of Athletes | Choose a username to check info (" + (", ").join(
                                    athleteManager.getAthleteIDs()) + ", or exit): ")
                            if ID not in athleteManager.getAthleteIDs() and ID != "exit":
                                print("Invalid input, try again")
                            elif ID == "exit":
                                break
                            else:
                                athleteManager.deleteAthlete(ID)
                                athleteManager.saveAthletesDataToJSON()
                        elif answer == "exit":
                            break
                        else:
                            print("Invalid input, please try again")
                elif answer =="exit":
                    y = False
                else:
                    print("Invalid input, please try again")

        elif (choice == "coach"):
            x = True
            while x == True:
                ID = input(
                    "\nCoach Menu | Choose a username to edit (" + (", ").join(
                        athleteManager.getAthleteIDs()) + ", or exit): ")
                if ID != "exit":
                    athlete = athleteManager.getAthlete(ID)
                    if athlete != None:
                        athlete.printProfile()
                        edit_answer=  athlete.editProfile()
                        if edit_answer == 1:
                            y = True
                            while y == True:
                                answer = input("\nEdit Athlete Menu | Choose an option to edit (" + (", ").join(Athlete.coach_choices) + "): ")
                                if answer == "week":
                                   athlete.editWeek()
                                   athleteManager.saveAthletesDataToJSON()
                                elif answer == "workout":
                                   athlete.editWorkout()
                                   athleteManager.saveAthletesDataToJSON()
                                elif answer == "feedback":
                                   athlete.checkFeedback()
                                   athleteManager.saveAthletesDataToJSON()
                                elif answer == "exit":
                                    y = False
                                else:
                                    print("Invalid input, try again")
                else:
                    x = False


main()