# Problem Statement 2:

# Complete the python function to get the output of below cases :

# i) case 1: n = 1, v = 1
# ii) case 2: n= 2, v = 23 (Note: 23 is derived as 1 + 22)
# iii) case 3: n= 3, v = 356 (Note: 356 is derived as 1+22+333)
# iv) case 4: n= 4, v = 4800 (Note: 356 is derived as 1+22+333+4444)

def mystery(n):
    v = 0
    for i in (range(1, n+1)):
        v += int(str(i) * i)
        
    return v

n = int(input("Enter a value for n: \t"))
print("V for the given value of n is => ", mystery(n))
