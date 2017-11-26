# Cypher Generator Encryption

*generate your own encryption scheme with just one key-word*


### **NOTE!!!** THE PASS-KEY IS NOT STORED ANYWHERE EVER. THIS IS A DETERMINISTIC FUNCTION GENERATOR AND WILL CREATE THE SAME PSEUDO RANDOM ENCRYPTION SCHEMES BASED OFF YOUR PASS-KEY.

#### **NOTE** FOR ENTHUSIASTS: to see all the awesome behind-the-scenes math going on, I will include an original version with all the print function output intact, [here](https://github.com/ConsciousMachines/Cypher-Generator/blob/master/encryptor_enthusiasts.py).

###### Final note: this is the first part of a series of fun encryption projects. 

Now then...

If you want something done right, you gotta do it yourself.

So why not create our own encryption? This is especially true for modern encryption.
This meta-algorith generates a personalized encryption scheme based on
only one keyword that you will haveto remember.

![Alt text](https://github.com/ConsciousMachines/Cypher-Generator/blob/master/example.png )

You can try the fun out for yourself:

~~~python
m = 'hello im Charles\nwelcome to my page which has 4/5 blogs'

encoded = encrypt( m ) # this file you can save somewhere, feeling safe
decoded = encrypt( code = encoded, encrypt = False )

print('Validity Test:', decoded == m )
~~~

The algorithm works as follows: Your key generates a series of parameters,
including the number of encryption steps, the security within each step,
and more. First it converts your message into binary, then it cuts that binary
up and reads it as words of different bit length before re-encrpting it
in the upcoming steps.

The parameteres are: exponent, refering to the binary exponent which will read
your file as if it were composed of 2-bit, or 5-bit, or 25-bit numbers (that
all depends on the parameters generated from your key phrase).

Some of the behind-the-scenes-fun going on:

![Alt text](https://github.com/ConsciousMachines/Cypher-Generator/blob/master/cypher_math.png)

A good strategy is to intermix long-bit encryptions and short-bit ones.
Depth should be large for short-bit encryptions, and small for large ones
as the probability of it hitting the same 15-bit number isn't too large.
The numpy seed must be restarted at each phase to generate the same cypher


!!! NOTE: The pass phrase is case-sensitive, and please don't include '\' in
the key nor the document you wish to encrypt (except for '\n', that has been
added to the vocabulary)
