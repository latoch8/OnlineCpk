slownik = {}
names = [1,2,3,4]
for name in names:
    slownik.update({name:{"data":[], "limits":[1,2]}})
slownik[1]["data"].append(2)
print(slownik[1])
print(slownik[1]["limits"])