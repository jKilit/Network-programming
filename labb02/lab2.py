keytovalue = {}
highestscore = 0

with open("labb02/score2.txt", "r") as file:
    for line in file:#iterrerar genom varje rad
        columns = line.split()#splittar columnerna
        if len(columns) == 5: #dubbelkollar
            upg, number, firstName, lastName, points = columns #ger namn till varje column
            points = int(points) #till int
            namn = f"{firstName} {lastName}" 

            if namn in keytovalue:#om namnet finns, lägg den i arrayen. annars öka poängen för namnet
                keytovalue[namn] += points
            else:
                keytovalue[namn] = points

    hogstpoang = max(keytovalue.values())
    hogstatagarna = [name for name, poang in keytovalue.items() if poang == hogstpoang]



    print(f"Person with the highest points is")
for i in hogstatagarna:
    print(f"{i} with {hogstpoang} poäng" )
