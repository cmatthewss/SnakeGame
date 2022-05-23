from msilib.schema import Font
import time
import tkinter as tk
from tkinter import Tk, ttk, StringVar, Toplevel
from tkinter import *
import random
from typing import List

high_scores = []

class Apple:

    def __init__(self):
        self.__x = random.randint(1, App.BOARD_WIDTH - 3)
        self.__y = random.randint(1, App.BOARD_HEIGHT - 3)

    def create_new_apple(self) -> None:
        self.__x = random.randint(1, App.BOARD_WIDTH - 3)
        self.__y = random.randint(1, App.BOARD_HEIGHT - 3)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y
        

class Snake:

    KEYS = ["w", "a", "s", "d"]
    MAP_KEY_OPP = {"w": "s", "a": "d", "s": "w", "d": "a"}
    number_of_clicks = 0

    def __init__(self, apple):
        # the apple now is a list of Apple instance
        self.__apple = apple
        self.__x = [20, 20, 20]
        self.__y = [20, 21, 22]
        self.__length = 3
        self.__key_current = "w"
        self.__key_last = self.__key_current
        self.__points = 0

    def move(self) -> None:  # move and change direction with wasd

        self.__key_last = self.__key_current

        for i in range(self.length - 1, 0, -1):
            self.__x[i] = self.__x[i - 1]
            self.__y[i] = self.__y[i - 1]

        if self.__key_current == "w":
            self.__y[0] = self.__y[0] - 1
            self.number_of_clicks += 1

        elif self.__key_current == "s":
            self.__y[0] = self.__y[0] + 1
            self.number_of_clicks += 1

        elif self.__key_current == "a":
            self.__x[0] = self.__x[0] - 1
            self.number_of_clicks += 1

        elif self.__key_current == "d":
            self.__x[0] = self.__x[0] + 1
            self.number_of_clicks += 1

        self.eat_apple()

    def eat_apple(self) -> None:
        # iteration over Apple instance to see which apple the snake eats
        for __apple in self.__apple:
            if self.__x[0] == __apple.x and self.__y[0] == __apple.y:

                self.__length = self.__length + 1

                x = self.__x[len(self.__x) - 1]  # snake grows
                y = self.__y[len(self.__y) - 1]
                self.__x.append(x + 1)
                self.__y.append(y)

                self.__points = self.__points + 1
                __apple.create_new_apple()

    @property
    def gameover(self) -> bool:

        for i in range(1, self.length, 1):

            if self.__y[0] == self.__y[i] and self.__x[0] == self.__x[i]:
                return True  # snake ate itself

        if self.__x[0] < 1 or self.__x[0] >= App.BOARD_WIDTH - 1 or self.__y[0] < 1 or self.__y[0] >= App.BOARD_HEIGHT - 1:
            return True  # snake out of bounds

        return False

    def set_key_event(self, event: Event) -> None:

        if event.char in Snake.KEYS and event.char != Snake.MAP_KEY_OPP[self.__key_last]:
            self.__key_current = event.char

    @property
    def x(self) -> List[int]:
        return self.__x.copy()

    @property
    def y(self) -> List[int]:
        return self.__y.copy()

    @property
    def length(self) -> int:
        return self.__length

    @property
    def points(self) -> int:
        return self.__points

# a class to gererate input widgets and collect input
class Table(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # input results
        self.bunch = {}

    # create one input entry
    def add_input(self,label,val):
        val = StringVar(value=val)
        entry = tk.Entry(self, textvariable=val)
        self.bunch[label] = entry
        return entry
    
    # creat a label and a input entry
    def create_widgets(self, labelDict):
        widgets = []
        for key,val in labelDict.items():
            label = ttk.Label(self, text=key, foreground='green')
            widgets.append([label]+[self.add_input(key,str(val))])
        return widgets
    
    # the widgets layout
    def layout(self, widgets):
        for row, row_widgets in enumerate(widgets):
            for column, widget in enumerate(row_widgets):
                widget.grid(row=row, column=column)
    
    # return the results in dict
    def todict(self):
        return {key:value.get() for key, value in self.bunch.items()}

# creat a new input window
class inputWindow(Toplevel):
    def __init__(self, master=None, cnf={}, label={}, **kw):
        super().__init__(master, cnf, **kw)
        # initation
        self.table = Table(self)
        self.ok_button = ttk.Button(self, text='OK', command=self.run)
        self.label = label
        self.layout()
        self.output = {}

    # create the layout using Table
    def layout(self):
        widgets = self.table.create_widgets(self.label)
        self.table.grid(row=0, column=0, sticky='we')
        self.table.layout(widgets)
        self.ok_button.grid(row=1, column=0, sticky='we')

    # return input result the App instance
    def run(self):
        self.output.update(self.table.todict())
        self.destroy()



class App(Tk):
    BOARD_WIDTH = 30
    BOARD_HEIGHT = 30
    TILE_SIZE = 10

    enter_name_shown = False
    add_to_leaderboard_shown = False
    entering_name = False
    id_number = 0
    name = "None"
    total_game_time = 0
    first_run_of_game = True


    COLOR_BACKGROUND = "white"
    COLOR_SNAKE_HEAD = "green"
    COLOR_SNAKE_BODY = "blue"
    COLOR_APPLE = "red"
    COLOR_FONT = "darkblue"
    FONT = "Times 14 bold"
    FONT_DISTANCE = 25

    TEXT_TITLE = "Snake"
    TEXT_GAMEOVER = "Game Over!"
    TEXT_NAME = "Name: "
    TEXT_POINTS = "Points: "
    TEXT_TIME_ELAPSED = "Time elapsed: "
    TEXT_SNAKE_LENGTH = "Snake length: "

    TICK_RATE = 200  # in ms

    # the number of apple
    number_apple = 1
    
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        Tk.__init__(self, screenName, baseName, className, useTk, sync, use)
        
        self.__apple = [Apple() for ii in range(App.number_apple)]
        self.__snake = Snake(self.__apple)

        self.__canvas = Canvas(self, width=App.BOARD_WIDTH * App.TILE_SIZE, height=App.BOARD_HEIGHT * App.TILE_SIZE)
        self.__canvas.pack()
        self.__canvas.configure(background=App.COLOR_BACKGROUND)
    
        self.title(App.TEXT_TITLE)
        self.bind('<KeyPress>', self.__snake.set_key_event)

        # activate shortcut
        self.bind_all('<KeyPress>', self.shortcut)

        # wheter pause the game
        self.__pause = False
        # wheter end pause and countdown
        self.__starting = False
        # the countdown time
        self.__count_time = 3

        self.start_button = Button(self, text="Start / Pause", command=self.setPause)
        self.start_button.pack(side='bottom')

    def mainloop(self, n=0):
        # menu
        self.__menu()

        self.__gameloop()
        Tk.mainloop(self, n)
    
    def __menu(self):
        mebubar = Menu(self)
        # menu 1: HOME
        menu1 = Menu(self, tearoff=0)
        menu1.add_command(label="Restart", command=self.setRestart)


        #
        mebubar.add_cascade(label="HOME", menu=menu1)
        #
        # menu 2: SETTING
        menu2 = Menu(self, tearoff=0)
        menu2.add_command(label="Windows Size", command=self.setWindowSize)
        menu2.add_separator()
        menu2.add_command(label="Number of Apples", command=self.setAppleNumber)
        #
        mebubar.add_cascade(label="SETTING", menu=menu2)
        
        # menu5 close the game
        mebubar.add_command(label="CLOSE", command=self.quit)
        self.config(menu=mebubar)

    def __gameloop(self):
        self.after(App.TICK_RATE, self.__gameloop)
        self.__canvas.delete(ALL)
        self.__pause = self.pause

        x, y = self.get_screen_center()
        self.__canvas.create_text(50, 10, fill=App.COLOR_FONT, font=App.FONT,
                                  text=self.name)

        if not self.__snake.gameover:
            # show the 'PAUSE' if stopping the game
            if self.__pause and not self.__starting:
                x, y = self.get_screen_center()
                self.__canvas.create_text(x, y, fill=App.COLOR_FONT, font=App.FONT, text='PAUSE')

            if not self.enter_name_shown:
                if self.first_run_of_game:
                    self.setPause()
                    self.first_run_of_game = False
                self.start_time = time.time()
                self.first_run_of_game = False
                self.enter_name_shown = True
                self.enter_high_score(self.set_current_user, self.setPause)

            # countdown when restarting the game
            if self.__starting:
                # accelerating for countdown
                App.TICK_RATE = 500
                self.countdown()
            else:
                # return to normal game speed
                App.TICK_RATE = 200
            
            # if the game is not stopped, the snack moves
            if not self.__pause:
                self.__snake.move()

            x = self.__snake.x
            y = self.__snake.y

            self.__canvas.create_rectangle(
                x[0] * App.TILE_SIZE,
                y[0] * App.TILE_SIZE,
                x[0] * App.TILE_SIZE + App.TILE_SIZE,
                y[0] * App.TILE_SIZE + App.TILE_SIZE,
                fill=App.COLOR_SNAKE_HEAD
            )  # Head

            for i in range(1, self.__snake.length, 1):
                self.__canvas.create_rectangle(
                    x[i] * App.TILE_SIZE,
                    y[i] * App.TILE_SIZE,
                    x[i] * App.TILE_SIZE + App.TILE_SIZE,
                    y[i] * App.TILE_SIZE + App.TILE_SIZE,
                    fill=App.COLOR_SNAKE_BODY
                )  # Body

            # iteration for all Apple instance
            for ii in range(len(self.__apple)):
                self.__canvas.create_rectangle(
                    self.__apple[ii].x * App.TILE_SIZE,
                    self.__apple[ii].y * App.TILE_SIZE,
                    self.__apple[ii].x * App.TILE_SIZE + App.TILE_SIZE,
                    self.__apple[ii].y * App.TILE_SIZE + App.TILE_SIZE,
                    fill=App.COLOR_APPLE
                )  # Apple
        else:  # GameOver Message
            if not self.add_to_leaderboard_shown:
                self.add_to_leaderboard_shown = True
                self.total_game_time = time.time() - self.start_time

                if self.name != "None":
                    high_scores.append([self.id_number, self.name, self.__snake.points, self.__snake.length,
                                        self.total_game_time])

            x, y = self.get_screen_center()
            self.__canvas.create_text(x, y - App.FONT_DISTANCE, fill=App.COLOR_FONT, font=App.FONT,
                                    text=App.TEXT_GAMEOVER)

            if self.name != "None":
                self.__canvas.create_text(x, y + App.FONT_DISTANCE*2, fill=App.COLOR_FONT, font=App.FONT,
                                          text=App.TEXT_NAME + str(self.name))

                self.__canvas.create_text(x, y + App.FONT_DISTANCE*3, fill=App.COLOR_FONT, font=App.FONT,
                                          text=App.TEXT_SNAKE_LENGTH + str(self.__snake.length))

                self.__canvas.create_text(x, y + App.FONT_DISTANCE * 4, fill=App.COLOR_FONT, font=App.FONT,
                                          text=App.TEXT_TIME_ELAPSED + str(abs(int(self.total_game_time))) + "s")

            self.__canvas.create_text(x, y + App.FONT_DISTANCE*5, fill=App.COLOR_FONT, font=App.FONT,
                                    text=App.TEXT_POINTS + str(self.__snake.points))

    # get the screen center for showing message
    def get_screen_center(self):
        x = App.BOARD_WIDTH * App.TILE_SIZE / 2  # x coordinate of screen center
        y = App.BOARD_HEIGHT * App.TILE_SIZE / 2  # y coordinate of screen center
        return x, y

    def enter_high_score(self, set_name_function, pause_function):
        self.entering_name = True
        enter_name_window = inputHighScoreWindow(self.master, set_name_function, pause_function)

    # get the state of pause
    @property
    def pause(self) -> bool:
        return self.__pause

    def set_current_user(self, id, name):
        self.id_number = id
        self.name = name
    
    # stop or restart the game
    def setPause(self):
        if self.__pause:
            self.__starting = True
        else:
            self.__pause = True
    
    # show countdown message
    def countdown(self):
        x, y = self.get_screen_center()
        self.__canvas.create_text(x, y, fill=App.COLOR_FONT, font=App.FONT, text=str(self.__count_time))
        self.__count_time -= 1
        if self.__count_time <= 0:
            self.__starting = False
            self.__count_time = 3
            self.__pause = False

    # restart the game
    def setRestart(self):
        # initiate the apple and snake
        self.__apple = [Apple() for ii in range(App.number_apple)]
        self.__snake = Snake(self.__apple)
        self.bind('<KeyPress>', self.__snake.set_key_event)
        
        # start the game
        self.__pause = True
        self.__starting = False
        self.enter_name_shown = False
        self.add_to_leaderboard_shown = False
        self.entering_name = False
        self.id_number = ""

    # set the window size
    def setWindowSize(self):
        # stop the game
        if not self.__pause:
            self.setPause()
        
        # create a new window for input
        window = inputWindow(self,label={'width':App.BOARD_WIDTH,\
                                            'height':App.BOARD_HEIGHT,
                                            'tile':App.TILE_SIZE})
        window.title('Please input the window size')
        window.transient(self)
        self.wait_window(window)

        # get input
        App.BOARD_WIDTH = int(window.output['width'])
        App.BOARD_HEIGHT = int(window.output['height'])
        App.TILE_SIZE = int(window.output['tile'])

        # create the canvas and start the game
        self.__canvas.config(width=App.BOARD_WIDTH * App.TILE_SIZE, height=App.BOARD_HEIGHT * App.TILE_SIZE)
        self.setPause()

     # set the apple number
    def setAppleNumber(self):
        # stop the game
        if not self.__pause:
            self.setPause()

        # previour number of apples
        before = App.number_apple
        
        # create a new window for inputing apples number
        window = inputWindow(self,label={'number of apples':App.number_apple})
        window.title('please input the number of apples')
        window.transient(self)
        self.wait_window(window)

        # get input
        App.number_apple = int(window.output['number of apples'])


        if App.number_apple > before:
            # create new Apple instance
            self.__apple += [Apple() for ii in range(App.number_apple-before)]
        else:
            # delete some Apple instances
            del self.__apple[App.number_apple:]
        self.__snake.__apple = self.__apple
        self.setPause()

    # shortcut event
    def shortcut(self, event):
            if (event.char == 'p') | (event.char == 'P'):
                self.setPause()
            if (event.char == 'o') | (event.char == 'O'):
                self.setWindowSize()
            if (event.char == 'n') | (event.char == 'N'):
                self.setAppleNumber()


def singleplayerwindow():
    App().mainloop()


def leaderboard():
    tk.Button.destroy(start_button)
    tk.Button.destroy(leaderboard_button)
    root.configure(background=App.COLOR_BACKGROUND)
    root.title("Leaderboard")
    label_leaderboard = tk.Label(root, text="Leaderboard", font=App.FONT, fg=App.COLOR_FONT)
    label_leaderboard.pack()
    label = tk.Label(root, text="Place:   Name   Apples", font=App.FONT, fg=App.COLOR_FONT)
    label.pack()
    sorted_list = list(reversed(sorted(high_scores, key=lambda entry: entry[2])))

    for i in range(min(len(sorted_list), 10)):
        entry = sorted_list[i]
        entry_text = f"{i+1}:\t {entry[1]}\t {entry[2]}"
        label = tk.Label(root, text=entry_text, font=App.FONT, fg=App.COLOR_FONT)
        label.pack()







root =Tk()
root.title("Snake Main Menu")
root.geometry('500x325')
#img=PhotoImage(file='C:/Users/alexr/OneDrive - Loughborough University/Year 2/WSB301 - Software/Snake/background1.gif')
#Label(root,image=img).pack()



leaderboard_button = tk.Button(root, bg = 'forestgreen', text='Leaderboard', command=leaderboard, width=25, font= ('Arial', 48))
leaderboard_button.pack(side='bottom')
start_button = tk.Button(root, bg = 'yellowgreen', text='Single Player', width=25, command=singleplayerwindow, font=('Arial', 48))
start_button.pack(side='bottom')

class inputHighScoreWindow(object):
    def __init__(self, master, set_current_user, pause_function):
        top = self.top = Toplevel(master)
        top.geometry("350x150+320+280")
        top.title("Enter name to start")
        self.label = Label(top, text="Enter name for high score:")
        self.button = Button(top, text="Enter", command=self.enter_name)
        self.enter_window = Entry(top)
        self.set_current_user = set_current_user
        self.pause_function = pause_function

        self.label.pack()
        self.enter_window.pack()
        self.button.pack()

    def enter_name(self):
        id = int(time.time())
        name = self.enter_window.get()
        self.set_current_user(id, name)
        self.pause_function()
        self.top.destroy()




root.mainloop()