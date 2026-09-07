counter=1
while counter<=10:
    print(counter)
    if counter==5:
        break
    counter+=1

print("Loop ended at counter value:", counter)



for i in range(1,10):
   
    if i==5:
        continue
    print(i)
    
events=[1,2,3,4,5,6,7,8,9,10]


## This is a simple for loop that iterates through the list of events and prints out the even numbers. and similar to foreach i C#
for i in events:
    if i%2==0:
        print("this is an even number:", i)



