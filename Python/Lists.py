data=["python","python","version","3.8","is","great"]

for words in data:
    print(words)


languages=["not specified"]

languages.append("python")
languages.append("java")

print("Languages list:", languages)

print("Count of 'python' in data:", data.count("python"))


word="python"
counter=0
for words in data:
    if word==words:
        counter+=1
print("Count of 'python' in data using loop:", counter)

### Tuples
names=("alice","bob","charlie","diana",2)

print("Names tuple:", names)

## we use tuples because it is safe that it cannot be changed, and it is faster than lists. Tuples are immutable.

languages_tuple=("python","java","c++","c#")

languages.append(languages_tuple)


print("Languages list after appending tuple:", languages)


print("Languages list:", languages)
print("Third language:", languages[3])


drivedset=languages[3]


print("Drived set:", drivedset)


arr = {'Mhamad', 'Rony', 'Rima', 'Sara'} 

print("Set:", arr)





data={1:"python", 2:"java", 3:"c++", 4:"c#", 5:"javascript"}
print("Data dictionary:", data)

print(data[3])

print(data.get(3))

data[6]="php"


data[3]="c"


print(data)


steam={"steam1":"game1","steam2":"game2","steam3":"game3"}


print("Steam dictionary:", steam)

def majo