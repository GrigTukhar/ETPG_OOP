import json

days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
times = ("morning", "lunch", "day", "evening", "exit")
choices = ("athlete", "coach", "exit")
coach_choices = ("week", "workout", "feedback", "exit")
athlete_choices=("creation","check","exit")
replies_week = ("add", "remove", "exit")
loads = ("easy", "medium", "hard")
replies_workout = ("edit", "remove", "exit")
sports = {"swimming", "cycling", "running"}


class Placeholder:

    def __init__(self):
        pass

    @classmethod
    def loadData(cls, file):
        with open(file) as data_file:
            cls.data = json.load(data_file)
        return cls.data

    @classmethod
    def uploadData(clsc,data):
        file = open("main.json", "w")
        file.write(json.dumps(data))
        file.close()


class Athlete():
    file = "main.json"

    def __init__(self, ID, name, surname, age, gender, workout, feedback):
        self.ID = ID
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.workout = workout
        self.feedback = feedback
        self.count = 0
        for key in self.feedback:
            self.count = self.count + 1

    @staticmethod
    def getInfo():
        users = Placeholder.loadData(Athlete.file)
        userids = []
        for key in users["ID"]:
            userids.append(key)
        while True:
            athleteID = input(
                "\nList of Athletes |Choose a username to check info (" + (", ").join(userids) + ", or exit): ")
            if athleteID in users["ID"]:
                person = users["ID"][athleteID]
                name = person["name"]
                surname = person["surname"]
                age = person["age"]
                gender = person["gender"]
                workout = person["workout"]
                feedback = person["feedback"]
                print("\nProfile of", athleteID, "\n-------------------------""\nName:", name, surname, "\nAge:", age,
                      "\nGender:", gender)
                x = True
                while x == True:
                    answer = input("\nWould you like to check workouts (yes, no): ")
                    if answer == "yes":
                        data = {athleteID: {}}
                        data[athleteID] = users["ID"][athleteID]
                        return data
                    elif answer == "no":
                        x = False
                    else:
                        print("Please try again")
            elif athleteID == "exit":
                return 0
            else:
                print("No such username, please try again")

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
                    data = Placeholder.loadData(Athlete.file)
                    data["ID"][self.ID]["feedback"] = self.feedback
                    Placeholder.uploadData(data)

    @classmethod
    def createAthlete(cls):
        data = Placeholder.loadData(Athlete.file)
        while True:
            answer = input("\nAthlete Profile Creation | Choose an option for users? (create, delete, exit): ")
            if answer == "create":
                ID=input("\nInput a username: ")
                name = input("Input your first name: ")
                surname = input("Input your surname: ")
                age = input("Input your age: ")
                z = True
                while z == True:
                    gender = input("Input your gender (male, female): ")
                    if gender !="male" and gender !="female":
                        print("Invalid input, please use either male or female")
                    else:
                        z = False
                data["ID"][ID]={"name":name, "surname": surname, "age": age, "workout": {"week1":{}},"feedback":{}}
                data["ID"][ID]["name"]=name
                data["ID"][ID]["surname"]=surname
                data["ID"][ID]["age"]=age
                data["ID"][ID]["gender"]=gender
                data["ID"][ID]["workout"]["week1"] = {"day1": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day2": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day3": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day4": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day5": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day6": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
                                                   "day7": {"morning": -1, "lunch": -1, "day": -1, "evening": -1}}
                print("\nAthlete",ID,"(",name,surname,") who is a",age,"year old",gender,"has been created")
                Placeholder.uploadData(data)
            elif answer =="delete":
                b = True
                while b == True:
                    temp = input("\nChose a username to remove(" + (", ").join(data["ID"].keys()) + ", exit): ")
                    if temp not in data["ID"].keys() and temp !="exit":
                        print("Invalid input, try again")
                    elif temp == "exit":
                        break
                    else:
                        del data["ID"][temp]
                        Placeholder.uploadData(data)
            elif answer == "exit":
                break
            else:
                print("Invalid input, please try again")

class Coach():
    file = "main.json"

    def __init__(self, ID):
        self.ID = ID

    @staticmethod
    def getInfo(placeholder):
        users = Placeholder.loadData(Coach.file)
        userids = []
        for key in users["ID"]:
            userids.append(key)
        while True:
            athleteID = input(
                "\nEditing for " + placeholder + " | Choose a username to check info (" + (", ").join(
                    userids) + ", or exit): ")
            if athleteID in users["ID"]:
                person = users["ID"][athleteID]
                name = person["name"]
                surname = person["surname"]
                age = person["age"]
                gender = person["gender"]
                workout = person["workout"]
                feedback = person["feedback"]
                print("\nProfile of", athleteID, "\n-------------------------""\nName:", name, surname, "\nAge:",
                      age, "\nGender:", gender)
                x = True
                while x == True:
                    answer = input("\nWould you like to edit (yes, no): ")
                    if answer == "yes":
                        return athleteID
                    elif answer == "no":
                        x = False
                    else:
                        print("Invalid input, please try again")

            elif athleteID == "exit":
                return 0
            else:
                print("No such username, please try again")

    def coachWeek(self):
        placeholder = Placeholder.loadData(Coach.file)
        data = placeholder["ID"][self.ID]
        reply = "x"
        print("\nCurrent weeks in schedule :(" + (", ").join(data["workout"].keys()) + ")")
        while (reply not in replies_week) or reply != "exit":
            count = 1
            for key in data["workout"]:
                count = count + 1
            reply = str(input("What would you like to do with the weeks (" + (", ").join(replies_week) + "): "))
            if (reply not in replies_week):
                print("Invalid input, try again")

            if (reply == "add"):
                count = str(count)
                print("\nweek" + count, "has been added\n")
                data["workout"]["week" + count] = {"day1": {"morning": -1, "lunch": -1, "day": -1, "evening": -1},
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
                del data["workout"]["week" + count]
            placeholder["ID"][self.ID]=data
            Placeholder.uploadData(placeholder)

    def coachWorkout(self):
        placeholder = Placeholder.loadData(Coach.file)
        data = placeholder["ID"][self.ID]
        week = "x"
        while week not in data["workout"].keys():
            week = input(str("\nInput week (" + (", ").join(data["workout"].keys()) + "): "))
            if week not in data["workout"].keys():
                print("That does not exist, try again")
            else:
                day = "x"
                while day not in days:
                    day = input(str("Input day (" + (", ").join(days) + "): "))
                    if day not in days:
                        print("That does not exist, try again")

        week_schedule = data["workout"][week][day]
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
                            data["workout"][week][day][time] = -1
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
                        data["workout"][week][day][time] = {"type": sport, "minutes": minutes,"distance": distance, "load": load}
                        print("Workout created during", time, "on", day, "in", week, ":",data["workout"][week][day][time]["type"], "for",data["workout"][week][day][time]["minutes"], "minutes and",data["workout"][week][day][time]["distance"], "kilometers, at a",data["workout"][week][day][time]["load"], "load")
                    placeholder["ID"][self.ID] = data
                    Placeholder.uploadData(placeholder)

    def coachFeedback(self):
        placeholder = Placeholder.loadData(Coach.file)
        feedback_data = placeholder["ID"][self.ID]["feedback"]
        numbers = []
        print("\nFeedback Menu | Following data sent by athlete\n")
        count = 1
        for key in feedback_data:
            week = list(feedback_data[key].keys())[0]
            day = list(feedback_data[key][week].keys())[0]
            time = list(feedback_data[key][week][day].keys())[0]
            type = feedback_data[key][week][day][time]["type"]
            minutes = feedback_data[key][week][day][time]["minutes"]
            distance = feedback_data[key][week][day][time]["distance"]
            load = feedback_data[key][week][day][time]["load"]
            hasCompleted = feedback_data[key][week][day]["hasCompleted"]
            feedback = feedback_data[key][week][day]["feedback"]
            resolved = feedback_data[key][week][day]["resolved"]

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
                placeholder2 = list(feedback_data.keys())[int(number) - 1]
                week = list(feedback_data[placeholder2].keys())[0]
                day = list(feedback_data[placeholder2][week].keys())[0]
                feedback_data[placeholder2][week][day]["resolved"] = "yes"
                print("Workout in", week, "on", day, "during the", time, "of", type, "for",
                      minutes, "minutes and", distance, "kilometers on a", load, "load, has been resolved")
                numbers.remove(number)
                placeholder["ID"][self.ID]["feedback"] = feedback_data
                Placeholder.uploadData(placeholder)

def main():
    choice = "x"
    print("\nETPG® | The training schedule program for any endurance trainer and athletes")
    while (choice not in choices) or choice != "exit":
        choice = str(input("\nGeneral Menu | Choose any of the following options (" + (", ").join(choices) + "): "))
        if (choice not in choices):
            print("Invalid input, try again")
        elif (choice == "athlete"):
            y=True
            while y == True:
                answer =input("\nAthlete Menu | Choose an option to edit (" + (", ").join(athlete_choices) + "): ")
                if answer =="check":
                    x = True
                    while x == True:
                        info = Athlete.getInfo()
                        if info != 0:
                            for key in info:
                                ID = key
                            holder = info[ID]
                            name = holder["name"]
                            surname = holder["surname"]
                            age = holder["age"]
                            gender = holder["gender"]
                            workout = holder["workout"]
                            feedback = holder["feedback"]
                            person_object = Athlete(ID, name, surname, age, gender, workout, feedback)
                            feedback_answer = Athlete.getWorkout(person_object)
                            if feedback_answer == 1:
                                Athlete.createFeedback(person_object)
                        else:
                            x = False
                elif answer =="creation":
                    Athlete.createAthlete()
                elif answer =="exit":
                    y = False
                else:
                    print("Invalid input, please try again")

        elif (choice == "coach"):
            x = True
            while x == True:
                answer = input("\nCoach Menu | Choose an option to edit (" + (", ").join(coach_choices) + "): ")
                if answer == "week":
                    y = True
                    while y == True:
                        info = Coach.getInfo(answer)
                        if info != 0:
                            coach_object = Coach(info)
                            Coach.coachWeek(coach_object)
                        else:
                            y = False
                elif answer == "workout":
                    y = True
                    while y == True:
                        info = Coach.getInfo(answer)
                        if info != 0:
                            coach_object = Coach(info)
                            Coach.coachWorkout(coach_object)
                        else:
                            y = False
                elif answer == "feedback":
                    y = True
                    while y == True:
                        info = Coach.getInfo(answer)
                        if info != 0:
                            coach_object = Coach(info)
                            Coach.coachFeedback(coach_object)
                        else:
                            y = False
                elif answer == "exit":
                    x = False
                else:
                    print("Invalid input, try again")


main()
