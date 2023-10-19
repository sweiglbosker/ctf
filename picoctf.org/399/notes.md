picoctf local-target
====================

note: didn't look at the source code to get some reversing practice

checksec
--------

only nx bit

running
-------

prints 64 after you enter a number, ub when input is too large indicating stack overflow

reversing
---------

pattern scan -> padding is 24

that was easy
