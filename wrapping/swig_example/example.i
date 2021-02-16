%module example
%{
  /* Includes the header in the wrapper code */
  #include "example.h"
  %}

/* Parse the header file to generate wrappers */
%include "example.h"
