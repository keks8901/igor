
import random

Prefects = ["Oscar", "Mo", "Magnus", "Rory", "Fin", "Hector", "Misha"]
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
Roll_Call = ["Morning", "Evening", "Night"]
Time = []



def make_list(list_days,list_r_c):
    for days in range (7):
        for time in range (3):
            Time.append(list_days[days] + " " + list_r_c[time])
    return(Time)  
    print(Time)

def random_schedul(list_prefects):
    random.shuffle(list_prefects)
    print('The Prefects', list_prefects)
    return list_prefects


Sessions = make_list(Days,Roll_Call)

Rand1 = random_schedul(Prefects)
Rand2 = random_schedul(Prefects)
Rand3 = random_schedul(Prefects)

RandPrefs = Rand1 + Rand2 + Rand3
print(RandPrefs)

# using list comprehension + zip() 
# interlist element concatenation 
Rota = [i + " " + j for i, j in zip(Time, RandPrefs)] 
print(', '.join(Rota))
