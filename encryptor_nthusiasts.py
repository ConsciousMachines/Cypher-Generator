'''Super Cypher'''

import numpy as np
import time

cypher_type = '<U28' # These may need to be adjusted to hold larger exponents
cypher_type2 = '<U28' # increase for bigger strings




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPERS ~~~~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\


def binary(num, bits = 6 ):
    start = list( bits*'0' )
    for i in range(bits):
        power = bits-1-i
        if 2**power <= num:
            start[i] = '1'
            num -= 2**power
    return ''.join(start)


def decimal(num, exp = 6 ):
    number = 0
    for i in range(exp):
        number += (2**i)*int( num[-1-i] )
    return number
        

def find_min_pow(n, power = 0):
    while 2**power <= n:
        power += 1
    return power


def vocabulary(): # step 1
    '''Step 1, initiates the keyboard and character sets to be used
    a is the same as keyboard except i removed the \ and placed \\ in the beginning,
    also added \n in th front. '''
    keyboard = """`123456789 0-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
    a = """\n\\`123456789 0-=qwertyui op[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
    aa = list(a)
    length = len(aa) # length refers to len of character set
    print('Vocabulary Length:',length)
    return aa


def flip(x):
    '''Quick Fix for the last elelemnt of binary appending without encryption'''
    return x[::-1]


def byter(x, exp):
    parsed = []
    while len(x) != 0:
        parsed.append( x[:exp] )
        x = x[exp:]
    return parsed

    
def binary_enumerator(exp):
    binaries = []
    for i in range(2**exp):
        binaries.append( binary(i,bits = exp))
    return binaries




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ENCRYPTORS ~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Level 1 ~~~~~~~~~~~~~\


def word_cypher(depth, security_mag, vocabulary): # later on make a matrix version 
    '''Start of encoding: sets security level and generates random numbers;
    Creates spherical cypher for encoding using X-bit numbers.
    X-bit specifies how many bits are used to represent the numbers
    depth is the length of the cypher, how many encodings there are per
    character until it loops back to start again'''
    length = len(vocabulary)
    num_codes = depth*length # can add a few magnitudes for security
    exp_needed = find_min_pow(num_codes) + security_mag
    b = np.random.choice( 2**exp_needed , size = num_codes, replace = False)
    b = np.reshape(b, [length,depth])
    print( 'Depth: %s Binary Exponent: %s' % (depth, exp_needed))
    c = np.array( b,dtype = cypher_type)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            c[i,j] = binary(b[i,j], exp_needed)
    print('Cypher Row Example:\n',c[-1,:])
    return c


def encode(message, vocabulary, cypher):
    mm = list(message)
    depth = cypher.shape[1]
    encoding = ''
    modulars = np.zeros([len(vocabulary)],dtype = int)
    for letter in mm:
        ind = vocabulary.index( letter ) # character index out of the 97
        encoding += cypher[ ind, modulars[ind]]
        modulars[ind] += 1
        modulars[ind] %= depth
    return encoding


def decode(m, vocabulary, cypher):
    ''' Works like a turning cypher that encodes a letter differently every
    iteration '''
    word = ''
    depth = cypher.shape[1]
    d = cypher
    bit_len = len(d[0,0])
    while m != '':
        letter = m[:bit_len]
        m = m[bit_len:]
        ind = np.where(d[:,0]==letter)[0][0]
        word += vocabulary[ind]
        d[ind,:] = np.append( d[ind,1:] , d[ind,0] )
    return word


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Level 2 ~~~~~~~~~~~~~\


def cypher(exp,depth,complexity):
    height = 2**exp
    num_codes = height*depth
    exponent = find_min_pow( num_codes ) + complexity
    cypha = np.random.choice( 2**exponent , size = num_codes, replace = False)
    cypha = np.reshape( cypha, [height, depth])
    max_value = np.max( cypha ) # convert to binary
    new_exp = find_min_pow( max_value )
    print('Cypher Bit-Length:' , new_exp)
    bin_cypha = np.array( cypha ,dtype = cypher_type2 )
    for i in range(cypha.shape[0]):
        for j in range(cypha.shape[1]):
            bin_cypha[i,j] = binary( cypha[i,j], bits = new_exp)
    print('First Row of Binary Cypher:\n',bin_cypha[0,:])
    return bin_cypha


        
def bin_encoder(x,bins,bin_cypha): #input is list
    depth = bin_cypha.shape[1]
    new_encoding = ''
    cyph_modulars = np.zeros(len(bins),dtype = int)
    for element in x:
        try:
            ind = bins.index( element )
            new_encoding += bin_cypha[ ind, cyph_modulars[ind]]
            cyph_modulars[ind] += 1
            cyph_modulars[ind] %= depth
        except:
            new_encoding += element # this appends the remainder
    print('Encoding Level %s Complete\n>~~~~~~~~~~~~~~~~~~~~~~~~~<\n'%len(bins[0]))
    return new_encoding


def bin_decoder(x, bins, bin_cypha):
    word_len = len(bin_cypha[0,0])
    original = ''
    d = bin_cypha
    while x != '':
        letter = x[:word_len]
        x = x[word_len:]
        if len(letter) == word_len:
            ind = np.where(d[:,0]==letter)[0][0]
            original += bins[ind]
            d[ind,:] = np.append( d[ind,1:] , d[ind,0] )
        if len(letter) < word_len:
            original += letter
            x = ''
    print('Decoding Level %s Complete\n>~~~~~~~~~~~~~~~~~~~~~~~~~<\n'%len(bins[0]))
    return original
    


# High Level Functions - Level 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\


def word2bin(list_of_params):
    '''Format is to pass in a list with [message, depth, security, seed]'''
    message = list_of_params[0]
    depth = list_of_params[1]
    security = list_of_params[2]
    seed = list_of_params[3]
    
    np.random.seed(seed) # to generate same cypher
    vocab = vocabulary() # vocab tool
    cypher_ = word_cypher( depth, security, vocab)
    return encode( message, vocab, cypher_)


def bin2word(list_of_params):
    '''Format is to pass in a list with [binary, depth, security, seed]'''
    binary = list_of_params[0]
    depth = list_of_params[1]
    security = list_of_params[2]
    seed = list_of_params[3]
    
    np.random.seed(seed) # to generate same cypher
    vocab = vocabulary() # vocab tool
    cypher_ = word_cypher( depth, security, vocab)
    return decode( binary, vocab, cypher_)


# High Level Functions - Level 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\


def bincrypt( list_of_params ):
    '''List of params: [x, exponent, depth, security, seed]'''
    x = list_of_params[0]
    exponent = list_of_params[1]
    depth = list_of_params[2]
    security = list_of_params[3]
    seed = list_of_params[4]
    
    np.random.seed(seed)
    c = cypher(exponent, depth, security) # create cypher
    bins = binary_enumerator(exponent) # binary index tool
    x2 = byter(x, exponent) # slice message
    x3 = bin_encoder(x2, bins, c) # encode
    x3 = flip(x3)
    return x3


def bindec(list_of_params ):
    '''List of params: [x, exponent, depth, security, seed]'''
    x = list_of_params[0]
    exponent = list_of_params[1]
    depth = list_of_params[2]
    security = list_of_params[3]
    seed = list_of_params[4]
    
    np.random.seed(seed)
    c = cypher(exponent, depth, security) # create cypher
    bins = binary_enumerator(exponent) # binary index tool
    x = flip(x)
    x4 = bin_decoder(x, bins, c)
    return x4






#~~~~~ ENCODING LEVEL 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Level 1 ~~~~~~~~~~~~~\

'''
m = 'hello im Charles\nwelcome to my page which has 4/5 blogs'


#~~~/---Only need 1 set of Hyper Params for level 1---\
w_depth = 10
w_security = 5
w_seed = 45

x1 = word2bin( m, w_depth, w_security, w_seed) # encrypt
original = bin2word( x1, w_depth, w_security, w_seed) # decrypt

print('Encryption Validity Check:' original == m )


'''

print('\n~~~~~~~~~~~~~~~LEVEL 1 TEST COMPLETE~~~~~~~~~~~~~~~\n')


#~~~~~ ENCODING LEVEL 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Level 1 ~~~~~~~~~~~~~\

'''Encryption Guide:
~~~~~~~~~~~~~~~~~~~~~
EXP DEP SEC SEED
 5   4   1  45
 2   40  2  12
 15  6   3   4
 2   60  2  41
 6   10  5  10

A good strategy is to intermix long-bit encryptions and short-bit ones.
Depth should be large for short-bit encryptions, and small for large ones
as the probability of it hitting the same 15-bit number isn't too large.
The numpy seed must be restarted at each phase to generate the same cypher
'''

'''
w_depth = 10
w_security = 5
w_seed = 45

m = 'hello im Charles\nwelcome to my page which has 4/5 blogs'


start_time = time.time()


x1 = word2bin( [m, w_depth, w_security, w_seed] ) # encrypt the word message


e1 = bincrypt( [ x1, 5, 4, 1, 45] )
e2 = bincrypt( [ e1, 2, 40, 2, 12] )
e3 = bincrypt( [ e2, 12, 6, 3, 4] )
e4 = bincrypt( [ e3, 2, 60, 4, 41] )
e5 = bincrypt( [ e4, 7, 10, 5, 10] )

d5 = bindec( [e5, 7, 10, 5, 10])
d4 = bindec( [e4, 2, 60, 4, 41])
d3 = bindec( [d4, 12, 6, 3, 4])
d2 = bindec( [d3, 2, 40, 2, 12])
d1 = bindec( [d2, 5, 4, 1, 45])

original = bin2word( [d1, w_depth, w_security, w_seed] ) # decrypt
print( 'Encryption Validity Test:' , x1 == d1 )
print('Time Taken:',  time.time() - start_time)


'''

print('\n~~~~~~~~~~~~~~~LEVEL 2 TEST COMPLETE~~~~~~~~~~~~~~~\n')




m = 'hello im Charles\nwelcome to my page which has 4/5 blogs'

key = 'Pokemon'

def meta( key, message = None, code=None, encrypt = True ): #add prompt feature
    start_time = time.time()
    strength = 4 # 5 would take too much compute
    pre_key = list( word2bin([ key , strength, 10,45]) )
    pre_key = sum( int(i) for i in pre_key)
    key2 = word2bin([ key , strength, 12,pre_key]) # 4 is rasonable power for the params
    k2 = byter(key2, strength)[:-1]
    numbas = []
    for i in k2:
        numbas.append( decimal( i, strength))
    numbas = np.array(numbas)
    numbas[numbas<=2] = 2
    numbas[numbas>=8] = 8 # for testing / speed
    print('Numbas:\n',numbas)
    encryptions = numbas[0] + 4 # just in case :)
    if encrypt: 
        e0 = word2bin( [message, numbas[1],numbas[2],numbas[3]] )
        e1 = e0
        for i in range(encryptions):
            e1 = bincrypt([e1,numbas[4+i],numbas[5+i],numbas[6+i],numbas[7+i]])
        print( len(e1) )
        print('Time For Encryption:', time.time() - start_time)
        return e1 # change this to a save file next
    
    if not encrypt:
        try: 
            decryptions = numbas[0] + 4
            for i in range(encryptions):
                j = encryptions-1-i
                code=bindec([code,numbas[4+j],numbas[5+j],numbas[6+j],numbas[7+j]])
            original = bin2word( [code, numbas[1],numbas[2],numbas[3]] )
            print( original )
            print( 'Amount of Cypher Encryptions:', encryptions)
            print('Time For Decryption:', time.time() - start_time)
            return original
        except:
            print('Wrong Key Phrase!')





encoded = meta(key,m) 
decoded = meta(key,code = encoded, encrypt=False)


print( 'Validity Test:', decoded == m )
















