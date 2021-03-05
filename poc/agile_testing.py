#!/usr/bin/env python2

from ctypes import cdll, c_double, byref

if __name__ == '__main__':
    libc = cdll.LoadLibrary("libc.so.6")

    dt = libc.time(None)
    pie = c_double()
    libc.sscanf(str(22.0/7), "%lf", byref(pie))
    answer = libc.printf(
        b"Terminal output through libc ... PI is close to %lf.\n",
        pie
    )
    print("libc system call (printf) returned %d." % answer)
    answer = libc.sleep(2)
    dt -= libc.time(None)
    print("libc call to sleep(2) returned %d, time elapsed is %ds." %\
          (answer, -dt)
    )
