import random

Prefects = ["Oscar", "Mo", "Magnus", "Rory", "Fin", "Hector", "Egor"]
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
Roll_Call = ["Morning", "Evening", "Night"]
Time = []
finale = []


def make_list(list_days,list_r_c):
    for days in range (7):
        for time in range (3):
            Time.append(list_days[days] + " " + list_r_c[time])
            
    print(Time)

def random_schedul(list_prefects):
    random.shuffle(list_prefects)
    print('The Prefects', list_prefects)


       
    


make_list(Days,Roll_Call)

random_schedul(Prefects)


