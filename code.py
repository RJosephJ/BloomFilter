import array
import csv
import math
"""""
                                        ---- Cache Penetration- Bloom Filters----
By:    Ricardo J. Rivera Sanchez
Class: CIIC4025
Date:  April 28 2023
Description:


    This program aims to create a bloom filter for database containing numerous emails extracted from a csv file.
    A second csv file is used to check weather the emails are in the bloom filter. The bloom filter is implemented as a bit array 
    of size math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2)))), where n is the size of the database (which in this case would be
    the number of emails in the file) and m is the false positive probability of 0.0000001. For adding the emails to the bloom filter a
    hash function is used where it takes the object (email) and uses the built-in Python hash function to create a hash and is then multiplied by a
    seed. The seed is used due to the many iterations the hashing process must go for us to have a better false positive probability. The number
    of how many times we would need to hash a certain object is obtained in the created function nhashes, where the hashes equates to
    round((m / n) * math.log(2)), where m is the bits and n is the size (number of emails). After all the emails have been hashes to the bloom filter, the second
    csv file is opened and read. This files contains different emails and our program will check if the email is in the bloom filter or not.
    



"""""


#Personalize hash function for the many iterations needed for the bloom filter
#The seed is the current iteration the hashing is doing
def hash_function(object, seed):
    return hash(object)+(seed**2)

#Function that returns how many hashes are needed so that our bloom filter performs as needed
def nhashes(m,n):
    return round((m / n) * math.log(2))
#Function that returns how many bits are needed so that our bloom filter has the correct number of bits
def nbits(n,p):
    return  math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2))))

def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])

#Intialization of variables
size=0
hashes=0
bits=0
with open("test.csv", 'r') as csv_file:
    csv_file = csv.reader(csv_file)
    for line in csv_file:
        size+=1

    bits= nbits(size-1,0.0000001)
    hashes = nhashes(bits,size-1)

    bloom=makeBitArray(bits)
with open("test.csv", 'r') as csv_file:
    csv_file = csv.reader(csv_file)
    for line in csv_file:
        for i in range(0,hashes):
            #Adding the object in the correct index by using modulo of how many bits the array has
            index=hash_function(line[0],i)%bits
            setBit(bloom,index)
with open("check.csv","r") as csv_file:
    csv_file = csv.reader(csv_file)
    check=True
    for line in csv_file:
        for i in range(0, hashes):
            #Gets the index
            index = hash_function(line[0], i) % bits
            #Checks if the index is 0 or 1
            #If its 0 it's not on the bloom filter and we can be sure it is not
            #If it's one there is a high chance that it is on the bloom filter
            if(testBit(bloom,index)==0):
                check=False
                break
        if(check==False):
            print(line[0]+",Not in the DB")
        elif(check==True):
            print(line[0]+",Probably in the DB")
        check=True













