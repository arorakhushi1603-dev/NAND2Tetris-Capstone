
// NAND2Tetris Capstone - Part C
// Roll number K = 62
// Starting row = 62
// Height = 20 rows
// Width = 48 pixels = 3 memory words

(START)
    // Check whether a key is pressed
    @KBD
    D=M
    @WHITE
    D;JEQ

    // Key pressed: select black
    @BLACK
    0;JMP

(BLACK)
    @R15
    M=-1
    @DRAW
    0;JMP

(WHITE)
    // No key pressed: select white
    @R15
    M=0

(DRAW)
    // Starting address = SCREEN + 32*62 = 18368
    @18368
    D=A
    @R13
    M=D

    // Draw 20 rows
    @20
    D=A
    @R14
    M=D

(ROW)
    // Write first word
    @R15
    D=M
    @R13
    A=M
    M=D

    // Write second word
    @R13
    M=M+1
    @R13
    A=M
    M=D

    // Write third word
    @R13
    M=M+1
    @R13
    A=M
    M=D

    // Move to the next screen row (32 words)
    @R13
    M=M+1
    @29
    D=A
    @R13
    M=D+M

    // Decrease row counter
    @R14
    M=M-1
    D=M
    @ROW
    D;JGT

    // Repeat and check keyboard again
    @START
    0;JMP
