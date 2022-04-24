#name: alanis zhao
#andrew id: aazhao

from cmu_112_graphics import *
import random
import copy
from copy import deepcopy

def appStarted(app):
    #used to resize images https://www.befunky.com/create/resize-image/
    #backgrounds
    app.bedroom=app.loadImage('bedroom.png')
    app.bathroom=app.loadImage('bathroom.png')
    app.kitchen=app.loadImage('kitchen.png')
    #above from https://www.spriters-resource.com/lcd_handhelds/tamagotchion/sheet/119803/
    app.night=app.loadImage('night.png')
    #from https://www.vectorstock.com/royalty-free-vector/cute-seamless-night-sky-pattern-with-cartoon-vector-31098550
    #minions
    app.minion1=app.loadImage('minion1.png')
    #from https://pngimg.com/images/heroes/minions
    app.minion2=app.loadImage('minion2.png')
    #from https://www.pngkey.com/maxpic/u2q8q8e6e6t4o0y3/
    app.minion3=app.loadImage('minion3.png')
    #from https://www.pngmart.com/image/179718
    #icons
    app.hungericon=app.loadImage('food.png')
    #from https://en.wikipedia.org/wiki/File:Bananas.svg
    app.happyicon=app.loadImage('happy.png')
    #from https://www.pngmart.com/image/7823
    app.cleanicon=app.loadImage('clean.png')
    #from https://pngimg.com/image/27878
    app.kitchenicon=app.loadImage('fridge.png')
    #from https://www.pngfind.com/mpng/wRiwxo_fridge-sprite-002-fridge-food-cartoon-png-transparent/
    app.bedicon=app.loadImage('bed.png')
    #from https://robloxislands.fandom.com/wiki/Large_Red_Bed
    app.gameicon=app.loadImage('game.png')
    #from https://www.flaticon.com/free-icon/game-controller_1451303
    app.bathicon=app.loadImage('bath.png')
    #from https://www.pinterest.com/pin/584482857867781853/
    app.lampicon=app.loadImage('lamp.png')
    #from https://clipartpng.com/?2101,lamp-png-clip-art
    app.graveicon=app.loadImage('grave.png')
    #from https://pngimg.com/image/42466
    app.cakeicon=app.loadImage('cake.png')
    #from https://www.pngkey.com/maxpic/u2w7y3e6r5w7e6r5/
    app.tiredicon=app.loadImage('wantsleep.png')
    #from https://pngset.com/download-free-png-rfypa
    app.bubbleicon=app.loadImage('bubble.png')
    #from https://pngtree.com/freepng/smoke-bubble-border_3288281.html
    #initial stats
    app.happy=100
    app.hunger=100
    app.cleanliness=100
    app.margin=50
    #lists
    app.currIcons=[app.gameicon,app.kitchenicon,app.bathicon]
    app.iconLocations=[app.height/2-325,app.height/2-225,app.height/2-125]
    app.stats=[app.happy,app.hunger,app.cleanliness]
    app.minions=[app.minion1,app.minion2,app.minion3]
    app.copyMinions=[app.minion1,app.minion2,app.minion3]
    app.messages=['LOL!!!','You suck!','Too easy!','Hahaha!','So fun!']
    #ctrl variables
    app.currI=random.randint(0,len(app.minions)-1)
    app.currMinion=app.copyMinions[app.currI]
    app.state='bedroom'
    app.needSleep=False
    app.age=0
    app.alive=True
    app.soapY=app.height-75
    app.soapX=app.width/2-350
    app.soap=False
    app.foodY=app.height-75
    app.foodX=app.width/2-350
    app.food=False
    app.drawHeart=False
    app.showWarning=[False,None]
    app.warningShown=False
    app.bday=False
    app.rotate=False
    app.angle=0
    app.dir=1
    app.squareSize=(min(app.width,app.height)-2*app.margin)//8
    app.game=None
    app.drawGameWarning=False
    app.isCalc=False
    app.myLost=False
    app.gameLost=False
    app.gameAnimation=False
    app.minionName=app.getUserInput('Name your Minion!')
    if app.minionName==None:
        app.minionName='Your minion'
    app.minionAnimation=False
    app.timeMinionAnimation=0
    app.minionX=app.width//40
    app.minionY=app.height//2
    app.currMessage=None
    #time variables
    app.sleepTime=random.randrange(30000,60000,5000)
    app.timePassed=0
    app.timerDelay=50
    app.timeNight=0
    app.timeHeart=0
    app.lastSleep=0
    app.timeWarning=0
    app.timeBday=0
    app.timeRotate=0
    app.timeGame=0
    app.timeLastWarning=0

def timerFired(app):
    #checkers game
    if(app.state=='game' and app.game!=None and app.game.myTurn==False and 
        app.minionAnimation==False):
        #if it is the game's turn
        app.isCalc=True
        value,board=minimax(app.game.board,4,app.game) #find the best move
        #the int above can be changed to a higher value for a better ai but 4 
        # is the highest my computer can run
        app.game.board=board
        app.isCalc=False
        app.game.myTurn=True
        #check for losses to end game
        if (app.game.board.myPieces<=0 and app.game.board.myKings<=0):
            app.myLost=True
        if (app.game.board.gamePieces<=0 and app.game.board.gamePieces<=0):
            app.gameLost=True
        if (app.myLost or app.gameLost):
            app.gameAnimation=True
            app.game=None
            app.stats[0]=100
        if (app.game!=None and app.game.board.hasChanged()):#play minion animation
            app.minionAnimation=True
            app.currMessage=app.messages[random.randint(0,4)]
    app.copyMinions=copy.copy(app.minions) #prevents distortion
    #movement tracking for icons
    if(abs(app.soapY-2*app.height/3)<=150 and app.stats[2]<100 and 
        abs(app.soapX-app.width/2)<=150): #currently washing minion
        app.stats[2]+=1
    if(abs(app.foodY-2*app.height/3)<=50 and app.stats[1]<100 and 
        abs(app.foodX-app.width/2)<=50): #done feeding minion
        if(app.stats[1]+10>100):
            app.stats[1]=100
        else:
            app.stats[1]+=10
        app.food=False
    if(app.food==False): #reset food icon
        app.foodY=app.height-75
        app.foodX=app.width/2-350
    #end animation tracking
    if(app.timeBday>=2000): #end birthday animation after 2 second
        app.bday=False
        app.timeBday=0
        app.state='bedroom'
    if(app.timeGame>=2000): #end game animation after 2 second
        app.gameAnimation=False
        app.timeGame=0
        app.state='bedroom'
    if(app.timeHeart>=1000): #end heart animation after 1 second
        app.drawHeart=False
        app.timeHeart=0
    if(app.timeWarning>=2000): #end warning animation after 2 second
        app.showWarning[0]=False
        app.timeWarning=0
        app.timeLastWarning=0
        app.warningShown=False
    if(app.timeNight==10000): #minion finishes sleeping
        app.state='bedroom'
        app.timeNight=0
        app.lastSleep=0
        app.sleepTime=random.randrange(30000,60000,5000)
        app.needSleep=False
    if(app.minionX>=app.width-app.width//40):#minion animation finishes
        app.minionAnimation=False
        app.timeMinionAnimation=0
        app.minionX=app.width//40
    #checking for conditions
    if(app.rotate):
        app.angle+=30*app.dir
        app.timeRotate+=app.timerDelay
    for currStat in app.stats: #minion dies if stat falls below 0
        if currStat<=0:
            app.alive=False
    if(app.lastSleep%app.sleepTime==0 and app.timePassed!=0 #minion needs sleep
        and app.lastSleep!=0):
        app.needSleep=True
    if(app.timePassed!=0):
        if(app.timePassed%10000==0):
            i=random.randint(0,len(app.stats)-1)
            app.stats[i]-=2 #random stat falls by 2 every 10 seconds
    for i in range(len(app.stats)):
        if (app.stats[i]<=20 and app.warningShown!=True and 
            app.timeLastWarning>=30000):
                app.showWarning=[True,i] #warns if stat is below 20
                app.warningShown=True
    if(app.lastSleep-app.sleepTime>=600000):
        app.alive=False
    #time tracking
    if(app.timeRotate%600==0 and app.timeRotate!=0):
        app.rotate=False
        app.timeRotate=0
        app.dir*=-1
    if(app.drawHeart): #track heart animation time
        app.timeHeart+=app.timerDelay
    if(app.showWarning[0]): #if showing warning
        app.timeWarning+=app.timerDelay
    if(app.bday): #if showing birthday
        app.timeBday+=app.timerDelay
    if(app.gameAnimation): 
        app.timeGame+=app.timerDelay
    if(app.timePassed%1800000==0 and app.timePassed!=0):
        app.age+=1
        app.bday=True
        #minion ages every 1 min, play bday animation
    if (app.minionAnimation):
        app.timeMinionAnimation+=app.timerDelay
        app.minionX+=app.width//30
    if(app.state=='night'):
        app.timeNight+=app.timerDelay #count time of night animation
    app.timePassed+=app.timerDelay #track game time
    app.lastSleep+=app.timerDelay #time since last sleep
    app.timeLastWarning+=app.timerDelay

def keyPressed(app,event):
    if(event.key=='r' and app.alive==False): #restart for dead minion
        appStarted(app)
    if(event.key=='c'): #makes minion cartwheel
        app.rotate=True
        decrease=random.randint(1,2)
        app.stats[decrease]-=2
    if(event.key=='y' and app.drawGameWarning): #ends game
        app.state='bedroom'
        app.game=Game(app.squareSize)
        app.drawGameWarning=False
    if(event.key=='n' and app.drawGameWarning): #continue game
        app.drawGameWarning=False
    if(event.key=='e' and app.state=='question'): #exit help screen
        app.state=app.lastState

def mouseDragged(app,event):
    if (app.state=='bathroom' and app.soap and app.stats[2]<100):
        app.soapY=event.y
        app.soapX=event.x
        #change location of soap icon
    elif(app.state=='bathroom'):
        app.soapY=app.height-75
        app.soapX=app.width/2-350
        #reset soap icon
    elif (app.state=='kitchen' and app.food and app.stats[1]<100):
        app.foodY=event.y
        app.foodX=event.x
        #change location of food icon
    elif(app.state=='kitchen'):
        app.soapY=app.height-75
        app.soapX=app.width/2-350
        #reset food icon
    elif(app.state=='bedroom'):
        if((abs(event.y-2*app.height/3)<=100 and 
            abs(event.x-app.width/2)<=100)): #draw heart when minion is pet
            app.drawHeart=True

def mousePressed(app,event):
    if(app.state=='game' and app.game.myTurn and app.minionAnimation==False): 
        #allow player to select a piece
        (row,col)=((event.y-10)//app.squareSize,(event.x-10)//app.squareSize)
        if(row>=0 and row<8 and col>=0 and col<8):
            if(app.game.board.getPiece(row,col)!=0 and 
                app.game.board.getPiece(row,col).color=='my'):
                app.game.select(row,col)
    if(app.state=='game' and app.game.myTurn and app.game.selected!=None and app.minionAnimation==False): #allow player to move to a square
        if(row>=0 and row<8 and col>=0 and col<8):
            (row,col)=((event.y-10)//app.squareSize,(event.x-10)//app.squareSize)
            piece=app.game.board.getPiece(row,col)
            if piece==0:
                app.game.move(row,col)
    if(app.state=='game' and event.x<=app.margin and event.y<=app.margin):
        #if you click the x
        app.drawGameWarning=True
    if(event.x<=100 and app.state=='bedroom'): #night when lamp pressed
        if(app.height/2-event.y<=50):
            app.state='night'
    elif(event.x<=100 and app.state=='bathroom'): #pick up soap
        if(app.height/2-event.y<=50):
            app.soap=True
    elif(event.x<=100 and app.state=='kitchen'): #pick up food
        if(app.height/2-event.y<=50):
            app.food=True
    if(app.state!='night' and app.state!='game'): #change rooms
        if(abs(event.x-(app.width/2+325))<=50):
            for i in range(len(app.iconLocations)):
                if(abs(event.y-app.iconLocations[i])<=50):
                    #random minion w room change
                    app.currI=random.randint(0,len(app.minions)-1)
                    app.currMinion=app.minions[app.currI]
                    if(app.currIcons[i]==app.kitchenicon):
                        app.state='kitchen'
                        app.currIcons=[app.gameicon,app.bathicon,app.bedicon]
                    elif(app.currIcons[i]==app.bedicon):
                        app.state='bedroom'
                        app.currIcons=[app.gameicon,app.bathicon,
                                        app.kitchenicon]
                    elif(app.currIcons[i]==app.bathicon):
                        app.state='bathroom'
                        app.currIcons=[app.gameicon,app.bedicon,app.kitchenicon]
                    else:
                        app.state='game'
                        app.game=Game(app.squareSize)
    if(app.state!='night' and app.state!='game'): #question mark pressed
        if(event.x>=app.width/2+275 and event.y>= app.height-125):
            app.lastState=app.state
            app.state='question'    

def drawRoom(app,canvas): #draws current background
    if(app.state=='bedroom'):
        canvas.create_image(app.width/2, app.height/2, 
                            image=ImageTk.PhotoImage(app.bedroom))
    elif(app.state=='bathroom'):
        canvas.create_image(app.width/2,app.height/2,
                            image=ImageTk.PhotoImage(app.bathroom))
    elif(app.state=='kitchen'):
        canvas.create_image(app.width/2,app.height/2,
                            image=ImageTk.PhotoImage(app.kitchen))
    elif(app.state=='night'):
        canvas.create_image(app.width/2,app.height/2,
                            image=ImageTk.PhotoImage(app.night))
        canvas.create_text(app.width/2-10,app.height/2-10,
                            text=f'{app.minionName} is sleeping...',
                            fill='white', font='Times 30 bold')
        
def drawSleep(app,canvas): #draws minion being tired
    canvas.create_image(app.width/2+100,app.height/2-50,
                        image=ImageTk.PhotoImage(app.tiredicon))

def drawHeart(app,canvas): #draws heart for pet minion
    canvas.create_image(app.width/2+100,app.height/2-50,
                        image=ImageTk.PhotoImage(app.happyicon))

def drawAge(app,canvas): #draws current age
    canvas.create_oval(app.width/2-50,app.height-110,app.width/2+50,
                        app.height-10,fill='white',width=0)
    canvas.create_text(app.width/2,app.height-60,
                        text=f'Age: {app.age}',fill='black',
                        font='Times 26 bold')

def drawMinion(app,canvas): #draws minion
    rotated=app.currMinion.rotate(app.angle)
    if(app.state!='night'):
        canvas.create_image(app.width/2,2*app.height/3,
                            image=ImageTk.PhotoImage(rotated))

def drawIcons(app,canvas): #draws current icons
    if(app.state!='night'):
        for i in range(len(app.currIcons)):
            canvas.create_image(app.width/2+325,app.iconLocations[i],
                                image=ImageTk.PhotoImage(app.currIcons[i]))
        if app.state=='bedroom':
            canvas.create_image(app.width/2-350,app.height-75,
                                image=ImageTk.PhotoImage(app.lampicon))
        elif app.state=='bathroom':
            canvas.create_image(app.soapX,app.soapY,
                                image=ImageTk.PhotoImage(app.cleanicon))
        elif app.state=='kitchen':
            canvas.create_image(app.foodX,app.foodY,
                                image=ImageTk.PhotoImage(app.hungericon))
        if(app.state!='game'):
            canvas.create_oval(app.width/2+275,app.height-125,app.width/2+375, 
            app.height-25, fill='white', width='0')
            canvas.create_text(app.width/2+325, app.height-75, text='?', 
            fill='black', font=f'Times {app.margin} bold')

def drawStats(app,canvas): #draws minion stats
    if(app.state!='night'):
        canvas.create_image(app.width/2-325,app.height/2-325,
                            image=ImageTk.PhotoImage(app.hungericon))
        canvas.create_text(app.width/2-320,app.height/2-310,
                            text=f'{app.stats[1]}',fill='white',
                            font='Times 26 bold')
        canvas.create_image(app.width/2-325,app.height/2-210,
                            image=ImageTk.PhotoImage(app.happyicon))
        canvas.create_text(app.width/2-325,app.height/2-210,
                            text=f'{app.stats[0]}',fill='white',
                            font='Times 26 bold')
        canvas.create_image(app.width/2-325,app.height/2-105,
                            image=ImageTk.PhotoImage(app.cleanicon))
        canvas.create_text(app.width/2-325,app.height/2-110,
                            text=f'{app.stats[2]}',fill='white',
                            font='Times 26 bold')

def drawDeath(app,canvas): #draws death animation
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    canvas.create_image(app.width/2,app.height/2,
                        image=ImageTk.PhotoImage(app.graveicon))
    canvas.create_text(app.width/2,app.height/2,
                        text=f'{app.minionName} has died...\nPress R to restart',
                        fill='black',font='Times 40 bold')

def drawWarning(app,canvas): #draws low stat warning
    canvas.create_rectangle(100,app.height/2-100,app.width-100,app.height/2+100,
                            fill='red',width='5')
    if(app.showWarning[1]==0):
        canvas.create_text(app.width/2,app.height/2,
                            text=f'{app.minionName} has low happiness',
                            fill='black',font='Times 40 bold')
    elif(app.showWarning[1]==1):
        canvas.create_text(app.width/2,app.height/2,
                            text=f'{app.minionName} has low hunger',fill='black',
                            font='Times 40 bold')
    else:
        canvas.create_text(app.width/2,app.height/2,
                            text=f'{app.minionName} has low cleanliness',
                            fill='black',font='Times 40 bold')

def drawGameWarning(app,canvas): #draws game exit warning
    canvas.create_rectangle(100,app.height/2-100,app.width-100,app.height/2+100,
                            fill='red',width='5')
    canvas.create_text(app.width/2,app.height/2,
                            text=f'Are you sure?\r You will not receive\r'+
                                ' happiness points for this game!\rPress Y to '
                                +'continue\rPress N to keep playing',
                            fill='black',font=f'Times {app.margin//2} bold')

def drawBirthday(app,canvas): #draws birthday animation
    canvas.create_rectangle(0,0,app.width,app.height,fill='pink',width='0')
    canvas.create_text(app.width/2,app.height/2-100,
                        text=f'{app.minionName} is now age {app.age}!',
                        fill='white',font='Times 40 bold')
    canvas.create_image(app.width/2,app.height/2+100,
                        image=ImageTk.PhotoImage(app.cakeicon))

def drawHelp(app,canvas): #text for help page
    line1='Welcome to Minion Tamagotchi!'
    line2='1. If your minion is tired, press the lamp to sleep.'
    line3='2. If your minion is hungry, feed it bananas in the kitchen'
    line4='3. If your minion is dirty, wash it with soap in the bathroom'
    line5='4. Play games with your minion for happiness!'
    line6='5. If health, happiness, or cleanliness is less than 0, your minion will die!'
    line7='6. Your minion grows 1 year older every 30 minutes.'
    line8=''
    line9='Fun Things:'
    line10='Try pressing C...'
    line11='Which room can you pet the minion?'
    line12=''
    line13='Press E to continue the game!'
    lines=[line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,
            line12,line13]
    for i in range(len(lines)):
        canvas.create_text(app.width/2,app.margin+i*app.margin,text=lines[i],
                            fill='black',font=f'Times {app.margin//3} bold')

def drawBoard(app,canvas,game): #draws game board
    if game!=None: #fills in colors of squares
        for row in range(8):
            for col in range(8):
                if(row%2==0):
                    if(col%2==0): color='pink'
                    else: color='red'
                else:
                    if(col%2==0): color='red'
                    else: color='pink'
                x=app.margin+col*game.size
                y=app.margin+row*game.size
                canvas.create_rectangle(x,y,x+game.size,y+game.size, 
                                        fill=color, width=0)
        if game.selected!=None: #if a piece is selected, draw valid moves
            possMoves=game.board.getValidMoves(game.selected)
            for move in possMoves:
                x=app.margin+move[1]*game.size
                y=app.margin+move[0]*game.size
                canvas.create_rectangle(x,y,x+game.size,y+game.size, 
                                        fill='green', width=0)
        canvas.create_text(app.margin/2,app.margin/2, text='X',fill='black',
                                font=f'Times {app.margin} bold')
        canvas.create_text(2*app.margin,app.height-app.margin/2, 
                            text=f'My pieces: {12-game.board.gamePieces}',
                            fill='black',font=f'Times {app.margin//2} bold')
        canvas.create_text(app.width-2*app.margin,app.height-app.margin/2, 
                            text=f'Game pieces: {12-game.board.myPieces}',
                            fill='black',font=f'Times {app.margin//2} bold')

def drawPieces(app,canvas,board): #draw all game pieces
    for row in range(8):
        for col in range(8):
            currPiece=board.getPiece(row,col)
            x=app.margin+col*app.squareSize
            y=app.margin+row*app.squareSize
            if currPiece!=0: #draw piece if there is a piece on that square
                if currPiece.king: #king pieces
                    canvas.create_oval(x,y,x+app.squareSize,y+app.squareSize,
                                        fill='yellow',width=0)
                else:
                    canvas.create_oval(x,y,x+app.squareSize,y+app.squareSize,
                                        fill='black',width=0)
                if currPiece.color=='my' and currPiece.king==False: #text for player pieces
                    canvas.create_text(x+app.squareSize//2,y+app.squareSize//2, 
                                        text='X', font=f'Times 40 bold', 
                                        fill='white',width='0')
                if currPiece.color=='my' and currPiece.king:
                    canvas.create_text(x+app.squareSize//2,y+app.squareSize//2, 
                                        text='X', font=f'Times 40 bold', 
                                        fill='black',width='0')

def drawGameAnimation(app,canvas): #draws game end animation
    canvas.create_rectangle(0,0,app.width,app.height,fill='pink',width='0')
    canvas.create_image(app.width//2,app.height//2-100,
                        image=ImageTk.PhotoImage(app.gameicon))
    if(app.myLost):
        canvas.create_text(app.width/2,app.height/2,
                            text=f'You lost!',fill='white',
                            font='Times 40 bold')
    else:
        canvas.create_text(app.width/2,app.height/2,
                            text=f'You won!',fill='white',
                            font='Times 40 bold')

def drawMinionAnimation(app,canvas): #draws minion during game
    canvas.create_image(app.minionX,app.minionY,
                        image=ImageTk.PhotoImage(app.currMinion))
    canvas.create_image(app.minionX+150,app.minionY-150,
                        image=ImageTk.PhotoImage(app.bubbleicon))
    canvas.create_text(app.minionX+150,app.minionY-150,
                            text=app.currMessage,fill='Black',
                            font='Times 40 bold')    

def redrawAll(app, canvas):
    if(app.alive==False): #draw death if minion is dead
        drawDeath(app,canvas)
    elif(app.state=='game'): #draw board and pieces if in game
        if(app.isCalc==False and app.game!=None):
            drawBoard(app,canvas,app.game)
            drawPieces(app,canvas,app.game.board)
        if(app.drawGameWarning):
            drawGameWarning(app,canvas)
        if(app.gameAnimation):
            drawGameAnimation(app,canvas)
        if app.minionAnimation and app.drawGameWarning==False:
            drawMinionAnimation(app,canvas)
    elif(app.state=='question'):
        drawHelp(app,canvas)
    else:
        if(app.state!='game'): #if not in a game
            drawRoom(app,canvas)
            drawMinion(app,canvas)
            drawStats(app,canvas)
            drawIcons(app,canvas)
            if(app.state!='night'):
                drawAge(app,canvas)
            if(app.needSleep==True and app.state!='night'): #if minion is tired
                drawSleep(app,canvas)
            if(app.drawHeart==True and app.state=='bedroom'): #if being pet
                drawHeart(app,canvas)
            if(app.showWarning[0]): #if low stat
                drawWarning(app,canvas)
            if(app.bday): #if birthday
                drawBirthday(app,canvas)

#for my code below, i followed the youtube tutorials in this series
#https://www.youtube.com/watch?v=vnd3RfeG3NM&list=PLzMcBGfZo4-lkJr3sqpikNyVzbNZLRiT3&t=0s
#i used it to learn the minimax algorithm but i had to alter it to fit into my
#tamagotchi code and i also had to change some drawing and functions because the
#tutorial used pygame. the tutorial uses the minimax algorithm but my code implements
#the "max" part because the player is playing against the ai

class Board: #defines board class for game
    def __init__(self,squareSize):
        self.board=[]
        self.myPieces=12
        self.gamePieces=12
        self.myKings=0
        self.gameKings=0
        self.lastSize=12
        self.size=squareSize
        self.change=False
        for row in range(8): #create empty board
            self.board.append([])
            for col in range(8):
                self.board[row].append(0)
        for row in range(3): #adds game pieces
            if row%2==0:
                for col in range(8):
                    if col%2==1:
                        self.board[row][col]=(Piece(row,col,'game',self.size))
            else:
                for col in range(8):
                    if col%2==0:
                        self.board[row][col]=(Piece(row,col,'game',self.size))
        for row in range(5,8): #adds player pieces
            if row%2==1:
                for col in range(8):
                    if col%2==0:
                        self.board[row][col]=(Piece(row,col,'my',self.size))
            else:
                for col in range(8):
                    if col%2==1:
                        self.board[row][col]=(Piece(row,col,'my',self.size))
    
    def move(self,piece,row,col): #moves a piece and makes it king
        justMovedPiece=self.board[piece.row][piece.col]
        self.board[piece.row][piece.col]=self.board[row][col]
        self.board[row][col]=justMovedPiece
        piece.move(row,col)
        if (piece.color=='my' and row==0):
            piece.makeKing()
        if (piece.color=='game' and row==7):
            piece.makeKing()
    
    def getPiece(self,row,col): #returns the piece at given location
        piece=self.board[row][col]
        return piece
    
    def evaluate(self): #evaluate the minimax score of code
        kingWeight=0.5
        pieceSum=self.gamePieces-self.myPieces
        kingSum=kingWeight*self.myKings-kingWeight*self.gameKings
        return pieceSum+kingSum
            
    def remove(self,pieces): #removes pieces from a board
        for piece in pieces:
            self.board[piece.row][piece.col]=0
            if (piece!=0):
                if piece.color == 'my':
                    self.myPieces-=1
                else:
                    self.gamePieces-=1
    
    def hasChanged(self): #checks if player pieces have decreased
        if self.lastSize!=self.myPieces:
            self.lastSize=self.myPieces
            return True
        return False
    
    def winner(self): #returns winner of game
        if(self.myPieces<=0):
            return 'GAME'
        elif self.gamePieces<=0:
            return 'ME'
        return None
    
    def getValidMoves(self,piece): #returns valid moves of a piece
        moves=dict()
        left=piece.col-1
        right=piece.col+1
        row=piece.row
        if (piece.color=='my' or piece.king):
            #adds player moves to the left or right and king moves
            if(row-3>-1):
                stop=row-3
            else: stop=-1
            result=self.moveLeft(row-1,stop,-1,piece.color,left)
            for curr in result:
                moves[curr]=result[curr]
            result=self.moveRight(row-1,stop,-1,piece.color,right)
            for curr in result:
                moves[curr]=result[curr]
        if (piece.color=='game' or piece.king):
        #adds game moves to the left or right or king moves
            if (row+3<8):
                stop=row+3
            else: stop=8
            result=self.moveLeft(row+1,stop,1,piece.color,left)
            for curr in result:
                moves[curr]=result[curr]
            result=self.moveRight(row+1,stop,1,piece.color,right)
            for curr in result:
                moves[curr]=result[curr]
        return moves
    
    def moveLeft(self,start,stop,step,color,left,skipped=[]):
        moves=dict()
        last=[]
        for r in range(start,stop,step):
            if left<0: #end if out of bounds
                break
            current=self.board[r][left]
            if (isinstance(current,Piece)==False): #if current square is empty
                if (len(skipped)!=0 and len(last)==0): #if we can't skip anymore then end it
                    break
                elif len(skipped)!=0: #if we can skip add skipped move and keep going
                    moves[(r,left)]=last+skipped
                else: #otherwise just add the move if no skipping at all
                    moves[(r,left)]=last
                if len(last)!=0: #check to see if we can keep going(after potentially skipping piece)
                    if step==-1:
                        if(r-3>0):
                            row=r-3
                        else: row=0
                    else:
                        if(r+3<8):
                            row=r+3
                        else: row=8
                    result=self.moveLeft(r+step,row,step,color,left-1,skipped=last) #check left
                    for curr in result:
                        moves[curr]=result[curr]
                    result=self.moveRight(r+step,row,step,color,left+1,skipped=last) #check right
                    for curr in result:
                        moves[curr]=result[curr]
                break
            elif current.color==color: #if the square is taken by our color, break
                break
            else: #if square is other color, keep checking to see if we can take
                last=[current]
            left-=1 #move left
        return moves
    
    def getAllPieces(self,color): #returns all pieces of a given color
        pieces=set()
        for row in range(8):
            for col in range(8):
                if self.board[row][col]!=0 and self.board[row][col].color==color:
                    pieces.add(self.board[row][col])
        return pieces

    def moveRight(self,start,stop,step,color,right,skipped=[]):
        moves=dict()
        last=[]
        for r in range(start, stop, step):
            if right>=8: #end if out of bounds
                break
            current=self.board[r][right]
            if isinstance(current,Piece)==False: #if current square is empty
                if len(skipped)!=0 and len(last)==0: #if we can't skip anymore then end it
                    break
                elif len(skipped)!=0: #if we can skip add skipped move and keep going
                    moves[(r,right)] = last + skipped
                else: #otherwise just add the move if no skipping at all
                    moves[(r, right)] = last
                if len(last)!=0: #check to see if we can keep going(after potentially skipping piece)
                    if step==-1:
                        if(r-3>0):
                            row=r-3
                        else: row=0
                    else:
                        if (r+3<8):
                            row=r-3
                        else: row=8
                    result=self.moveLeft(r+step, row, step, color, right-1,skipped=last) #check left
                    for curr in result:
                        moves[curr]=result[curr]
                    result=self.moveRight(r+step, row, step, color, right+1,skipped=last) #check right
                    for curr in result:
                        moves[curr]=result[curr]
                break
            elif (current.color==color): #if the square is taken by our color
                break
            else: #if the square is other color, continue loop
                last=[current]
            right+=1
        return moves

class Piece: #defines pieces
    def __init__(self,row,col,color,squareSize):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.size=squareSize

    def __repr__(self): #returns string of color
        return self.color

    def makeKing(self): #for drawing and movement
        self.king = True

    def move(self,row,col): #move a piece to a given row
        self.row=row
        self.col=col

class Game: #defines a checkers game
    def __init__(self, squareSize):
        self.size=squareSize
        self.selected=None
        self.board=Board(self.size)
        self.myTurn=True
        self.validMoves=dict()

    def winner(self): #returns if a game is won
        return self.board.winner()

    def select(self,row,col): #select a piece
        if self.selected!=None: #check if trying to move
            moveSuccessful=self.move(row, col)
            if moveSuccessful: #if the move was valid
                self.selected=None
                self.select(row, col) #reselect the moved piece to continue possible moves
        piece=self.board.getPiece(row, col)
        if piece!=0 and self.myTurn and piece.color=='my': #initially select piece and it's my turn
            self.selected=piece
            self.validMoves=self.board.getValidMoves(piece) #find valid moves
            return True   
        return False

    def move(self,row,col): #move a piece to row and column
        piece = self.board.getPiece(row,col)
        if self.selected!=0 and piece==0 and (row,col) in self.validMoves:
            #check move conditions
            self.board.move(self.selected,row,col)
            skipped=self.validMoves[(row,col)]
            if len(skipped)!=0: #if you jumped over pieces
                self.board.remove(skipped)
            self.changeTurn()
            self.selected=None #unselect after move
            return True #
        else:
            return False #if move was not valid

    def changeTurn(self): #change turn
        self.validMoves = dict() #reset moves
        if self.myTurn:
            self.myTurn=False
        else:
            self.myTurn=True

def minimax(position,depth,game): #recursive ai checkers fxn
    if depth==0 or position.winner()!= None: #if at move depth or someone wins
        return position.evaluate(),position  #return score and current board
    else:
        maxScore=0
        bestMove=None
        for move in getAllMoves(position, 'game'): #for all possible moves
            score = minimax(move, depth-1, game)[0] #find their score
            if maxScore<=score: #keep track of best move so far
                maxScore=score
                bestMove=move
        return maxScore, bestMove

def simulateMove(piece, move, board, skipped): #find board of hypothetical move
    board.move(piece, move[0], move[1])
    if len(skipped)!=0:
        board.remove(skipped)
    return board

def getAllMoves(board,color): #return all poss moves of a board and color
    moves=set()
    for piece in board.getAllPieces(color):
        validMoves = board.getValidMoves(piece)
        for currMove in validMoves:
            move=currMove
            skip=validMoves[currMove]
            possBoard = copy.deepcopy(board)
            possPiece = possBoard.getPiece(piece.row, piece.col)
            newBoard = simulateMove(possPiece, move, possBoard, skip)
            moves.add(newBoard)
    return moves

runApp(width=800,height=800)