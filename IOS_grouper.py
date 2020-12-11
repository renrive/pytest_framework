f = open("../CI-Name.csv", "r")
list_of_models = []
CIs = []
for line in f:
    line_CI = line.split(",")
    CIs.append(line_CI)

#print(CIs)
single_Models = []
first_time = "Yes"
add_model = "NO"
tree = []
for ci_line in CIs:
    #print(ci_line[1])
    add_model = "Yes"
    found_line = "No"
    if first_time == "Yes":
        #print("18:",ci_line[3])
        single_Models.append(ci_line[3])
        first_time = "No"
        continue

    for model in single_Models:
        
        if ci_line[3] == model[3]:
            add_model = "No"
            found_line = "Yes"
            break

    if add_model == "Yes" and found_line == "No":
        x = ci_line[0],ci_line[1],ci_line[2],ci_line[3],ci_line[4]
        single_Models.append(x)

for line in single_Models:
    print(line[0].replace("\n",""),",",line[1].replace("\n",""),",",line[2].replace("\n",""),",",line[3].replace("\n",""),",",line[4].replace("\n",""))
