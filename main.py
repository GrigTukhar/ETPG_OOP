import json

days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
time_of_day =("morning", "lunch", "day", "evening")

class exercise:

    def __init__(self):
        pass

    @classmethod
    def loadData(cls,file):
        with open(file) as data_file:
            cls.data = json.load(data_file)
        return cls.data

class athlete(exercise):

    file = "main.json"
    def __init__(self,ID,name,surname,age,gender,workout,feedback):
        super().loadData(athlete.file)
        self.ID = ID
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.workout = workout
        self.feedback = feedback

    @staticmethod
    def getInfo():
        users = exercise.loadData(athlete.file)
        userids = []
        for key in users["ID"]:
            userids.append(key)
        while True:
            athleteID = input("\nChoose a username to check info (" + (", ").join(userids) + ", or exit): ")
            if athleteID in users["ID"]:
                person = users["ID"][athleteID]
                name = person["name"]
                surname = person["surname"]
                age =person["age"]
                gender = person["gender"]
                workout = person["workout"]
                feedback = person["feedback"]
                print("\nProfile of",athleteID,"\n-------------------------""\nName:",name,surname,"\nAge:",age,"\nGender:",gender)
                x = True
                while x == True:
                    answer = input("\nWould you like to check workouts (yes, no): ")
                    if answer == "yes":
                        data ={athleteID:{}}
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
                        count=0
                        for key in self.workout[week][day]:
                            if self.workout[week][day][key] == -1:
                                print(key, ":", "no excerisize for this time of day")
                                count = count +1
                            else:
                                print(key, ":", self.workout[week][day][key]["type"], "for", self.workout[week][day][key]["minutes"],
                                      "minutes and",
                                      self.workout[week][day][key]["distance"], "kilometers, at a", self.workout[week][day][key]["load"],
                                      "load")
                        self.week =week
                        self.day = day
                        if count <4:
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
        print("code works")



def main():
    x = True
    while x == True:
        info=athlete.getInfo()
        if info != 0:
            for key in info:
                ID= key
            holder =info[ID]
            name = holder["name"]
            surname = holder["surname"]
            age = holder["age"]
            gender = holder["gender"]
            workout = holder["workout"]
            feedback = holder["feedback"]
            person_object = athlete(ID,name,surname,age,gender,workout,feedback)
            feedback_answer=athlete.getWorkout(person_object)
            if feedback_answer == 1:
                athlete.createFeedback(person_object)
        else:
            x = False



main()
