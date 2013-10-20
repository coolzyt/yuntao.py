#coding=utf8
import struct
import base64
"""
struct fmt value
格式符    C语言类型    Python类型
x    pad byte    no value    
c    char    string of length 1    
b    signed char    integer    
B    unsigned char    integer    
?    _Bool    bool    (1)
h    short    integer    
H    unsigned short    integer    
i    int    integer    
I    unsigned int    integer or long    
l    long    integer    
L    unsigned long    long    
q    long long    long    (2)
Q    unsigned long long    long    (2)
f    float    float    
d    double    float    
s    char[]    string    
p    char[]    string    
P    void *    long
"""


def int2byte_BE(i):
    return struct.pack('>i',i)

def int2byte_LE(i):
    return struct.pack('<i',i)

def byte2int_BE(s):
    return struct.unpack('>i',s)[0]

def byte2int_LE(s):
    return struct.unpack('<i',s)[0]

def base16(inputbyte):
    return base64.b16encode(inputbyte).decode("ascii");

def base16decode(base16str):
    return base64.b16decode(base16str)

