import GPU

GPU.platform_id = -1

import random
import numpy as np
import time


try:
    import Tkinter as tk
except:
    import tkinter as tk


try:
    import ImageTk
    import Image
except:
    from PIL import ImageTk
    from PIL import Image



single = ['cos', 'sin'] #Operations on a single number
binary = ['*', '+', '-'] #Operations for 2 numbers
numlist = ['x', 'y', 't', 'Constant']


def randFunction(length, singleweight, numberweight):
    hasx = False
    hasy = False
    hast = False
    while not(hasx and hasy and hast):
        #Types: b for binary, s for single, f for first, n for number
        function = ''
        lasttype = 'f'
        thistype = 0
        hasx = False
        hasy = False
        hast = False
        chanceend = 0
        length = 1 #Number of operations done so far
        while True:
            chanceend = (1.0 - (1.0 / length)) ** (float(functionLength)/7)
            if lasttype == 'n':
                number = random.random()
                if number < chanceend:
                    break
                function = '(' + function + ')' + random.choice(binary)
                lasttype = 'b'
            elif lasttype == 's' or lasttype == 'b' or lasttype == 'f':
                function += '('
                thistype = random.random()
                if thistype < singleweight / (singleweight + numberweight):
                    function += random.choice(single)
                    lasttype = 's'
                else:
                    what = random.choice(numlist)
                    if what == 'Constant':
                        function += str(random.gauss(150, 50))
                    else:
                        function += what
                        if what == 'x':
                            hasx = True
                        elif what == 'y':
                            hasy = True
                        elif what == 't':
                            hast = True
                    lasttype = 'n'
                    function += ')'
            length += 1
    if function.count('(') > function.count(')'):
        function += ')' * (function.count('(') - function.count(')'))
    return function

    
gpu = GPU.GPU()

root = tk.Tk()
root.geometry('720x480')
root.title('AutoVideosLive')

def replace(s, substr, newsubstr):
    #Replaces the first instance of substr in s with newsubstr
    return s[:s.index(substr)] + newsubstr + s[s.index(substr)+len(substr):]

t = 0

def startVideo():
    global width, height, rfunction, gfunction, bfunction
    global imageLabel, globalSize, clProgramTemplate, t

    root.update()
    resolution = root.winfo_width(), root.winfo_height()

    root.resizable(False, False)

    startButton.destroy()
    infoLabel.destroy()

    imageLabel = tk.Label(root)
    imageLabel.pack()
    
    width, height = resolution

    globalSize = (width*height,)
    
    

    rfunction = randFunction(80., 1., 1.)
    gfunction = randFunction(80., 1., 1.)
    bfunction = randFunction(80., 1., 1.)
    
    clProgramTemplate = open('AutoVideosLive.cl').read()
    clProgramTemplate = replace(clProgramTemplate, '<WIDTH>', str(width))
    clProgramTemplate = replace(clProgramTemplate, '<RFUNCTION>', rfunction)
    clProgramTemplate = replace(clProgramTemplate, '<GFUNCTION>', gfunction)
    clProgramTemplate = replace(clProgramTemplate, '<BFUNCTION>', bfunction)
    
    


    t = 0
    playFrame()

def onSpacePress():
    global rfunction, gfunction, bfunction
    global clProgramTemplate, t

    

    rfunction = randFunction(80., 1., 1.)
    gfunction = randFunction(80., 1., 1.)
    bfunction = randFunction(80., 1., 1.)
    
    clProgramTemplate = open('AutoVideosLive.cl').read()
    clProgramTemplate = replace(clProgramTemplate, '<WIDTH>', str(width))
    clProgramTemplate = replace(clProgramTemplate, '<RFUNCTION>', rfunction)
    clProgramTemplate = replace(clProgramTemplate, '<GFUNCTION>', gfunction)
    clProgramTemplate = replace(clProgramTemplate, '<BFUNCTION>', bfunction) 


    t = 0

def playFrame():
    global t
    
    
    clProgram = replace(clProgramTemplate, '<FRAMENUMBER>', str(float(t)))

    start = time.time()
    
    gpu.readFromString(clProgram)

    output = np.zeros(globalSize, dtype=np.float32)

    gpu.setup([], output)

    output = gpu.run('AutoFrame', globalSize) % 255

    
    
    output.resize(height, width, refcheck=False)

    output = output.astype(np.uint8)
    
    output = np.repeat(output, 3)

    output.resize(height, width, 3)    
    
    img = Image.fromarray(output, 'RGB')

    photo = ImageTk.PhotoImage(img.convert('RGBA'))
    imageLabel.config(image=photo)
    imageLabel.image = photo

    t += 1
    end = time.time()
    print end-start

    root.after(1, playFrame)

def spacePress(e):
    if e.char == ' ':
        onSpacePress()

startButton = tk.Button(text='Start video at this resolution',
                        command=startVideo)

startButton.pack()

infoLabel = tk.Label(text='Press space to change video.')
infoLabel.pack()

root.bind('<Key>', spacePress)
root.mainloop()
