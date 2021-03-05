#!/usr/bin/env python3

from ctypes import cdll

if __name__ == '__main__':
    libc = cdll.LoadLibrary("libc.so.6")

    t0 = libc.time(None)
    answer = libc.printf(b"Printing through libc...\n")
    print(f"libc system call (printf) returned {answer}.")
    answer = libc.sleep(3)
    t1 = libc.time(None)
    print(f"Libc call to sleep(3) returned {answer}, time elapsed is {t1-t0}s.")
