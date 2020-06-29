
def convert(Key): 
    KeyOffset = 52
    i = 28
    Chars = "BCDFGHJKMPQRTVWXY2346789"
    KeyOutput = ''
    while i>=0:
            Cur = 0
            x = 14
            while x>=0:
                Cur = Cur * 256
                Cur = x + KeyOffset + Cur
                #Key(x + KeyOffset) = (Cur \ 24) 
                Cur = Cur%24
                x = x -1
            i = i -1
            KeyOutput = Chars[Cur+1 + KeyOutput]
            if (((29 - i)%6) == 0) and (i != -1):
                    i = i -1
                    KeyOutput = "-" & KeyOutput
            

    return(KeyOutput)
convert('CDFGHJKMPQRTVJKM')
