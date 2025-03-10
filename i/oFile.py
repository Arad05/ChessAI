names = []

file = open("name.txt","w")
for i in range(3):
    names.append(input("whats your name? "))
    file.write(names[i] + "\n")
file.close()
