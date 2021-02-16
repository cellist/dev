#!/usr/bin/env python

"""
 NAME
     htonl,  htons,  ntohl,  ntohs - convert values between host and network
     byte order
"""
from ctypes import cdll

libc = cdll.LoadLibrary("libc.so.6")
ntohl = libc.ntohl

answer = ntohl(0x6C)
print(answer, hex(answer))
