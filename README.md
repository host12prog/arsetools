# arsetools
Tools for making music for the A5625 sound chip
# how to use
arseinter is the interpreter that converts .arse register dumps to .raw audio files
arsemusint is the tool that interprets a .txt file to convert into .arse format
build the arseinter tool first:
```
gcc -o arseinter arseinter.c a5625.c
```
then to use it, use:
```
./arseinter [infile]
```
the output will always be in a file called "arse.out", which is an 8-bit PCM 32kHz sample rate raw audio file

to use arsemusint, use python:
```
python3 arsemusintv38.py [infile]
```
this will output a file called "musix.arse", which you can use with arseinter.
a txt file has been included for testing.

# .arse format
```
The playback rate of an ARSE file should be 50hz, or at a 32kHz sampling rate, 640 samples per frame.
Offset | Description
0x00   | 4-byte "ARSE" header
0x04   | Channel 1 period
0x05   | Channel 1 control
       | 0xnv (where n - 0 for tone, 1 for noise, and v - 4-bit volume)
0x06   | Channel 2 period
0x07   | Channel 2 control
... repeat these 4 bytes until EOF
```
