

#arr = [4,2,7,5,8,2,2,1,3,2]
arr = [1,1,1,4,5,6,7,8,9,10]
n = len(arr)
print(n)

def countOc(arr, n):
    
    for i in arr:
        res = 0
        for z in arr:
            if i == z:
                res += 1
            print(i, res)

if __name__ == "__main__":
    test_st = 'My string to test as an argument'
    countOc(arr,n)


















#s1 = "R1"

#print(s1[1])
# for element in s1[1]:
#     print(int(element))

# a = 2
# b = 4
# c =2

# print(a|b)

# if a == b or c:
#     print("true")

#print(a.bit_length())
# print('{0:08b}'.format(11))
# print('{0:16b}'.format(11))


#print(~11)
# print(~11)
# print(int('00001011'))
'''
def fw(x):
    return {
        'a': 1,
        'b': 2,
    }[x]

print(fw("a"))






def switcher(opcode):
    return{

        'LI': 1
    }[opcode]


thingy = "LI"

print(switcher(thingy))







z = 5
y = 10
c = z+y

opcodes = {"LI": c}



print(opcodes.get("LI","default"))



###############################################

def add(a,b):
    print(a+b)

my_dict ={"+" : add


}

my_dict["+"](1,2)
'''