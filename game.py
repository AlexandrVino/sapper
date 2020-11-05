from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import random


PATH = 'E:/Python/Chess/'
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 700)
Config.set('graphics', 'height', 770)


# инструкция к установке python kivy
# https://kivy.org/doc/stable/installation/installation-windows.html
# зарание прошу прощения за переменную "i" в списочных выражениях, это для PEP8


class EmptyButton(Button):
    def __init__(self, coord, name, **kwargs):
        super().__init__(**kwargs)
        self.coord = coord
        self.name = name
        self.touch = False

    def open(self):
        self.touch = True
        coord1 = list(self.coord).copy()
        coord2 = list(self.coord).copy()
        coord3 = list(self.coord).copy()
        coord4 = list(self.coord).copy()
        coord1[0] -= 1
        coord2[0] += 1
        coord3[1] -= 1
        coord4[1] += 1
        list_of_coord = [coord1, coord2, coord3, coord4]
        list_of_coord = [i for i in list_of_coord if 0 <= i[0] <= 19 and 0 <= i[1] <= 19]

        x, y = self.coord[0], self.coord[1]
        BOARD.list_of_buttons[x][y].background_color = [.10, .58, .95, 1]
        for coord in list_of_coord:
            if not BOARD.list_of_buttons[coord[0]][coord[1]].touch:
                BOARD.list_of_buttons[coord[0]][coord[1]].open()

        return 2


class IntegerButton(EmptyButton):
    def __init__(self, coord, name, **kwargs):
        super().__init__(coord, name, **kwargs)
        self.dict_of_colors = {
            1: [.96, .53, .25, 1],
            2: [.99, .87, .53, 1],
            3: [.94, 0, .58, 1],
            4: [.11, .59, .96, 1],
            5: [.2, .8, 1, 1],
            6: [1, .5, .7, 1],
            7: [.8, 0, 1, 1],
            8: [1, .4, 0, 1]
        }
        
    def open(self):
        self.touch = True
        self.text = str(self.number)
        x, y = self.coord[0], self.coord[1]
        BOARD.list_of_buttons[x][y].background_color = self.dict_of_colors[int(self.text)]

        return 1


class BombButton(EmptyButton):
    def open(self):
        self.touch = True
        self.text = '*'
        BOARD.list_of_buttons[self.coord[0]][self.coord[1]].background_color = [1, 0, 1, .4]
        return 0


class PlayGroundApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self): 
        global label
        self.bl = Widget()
        self.layout = GridLayout(cols=20, rows=20, size=(700, 700))
        self.lbl = Label(pos=(0, 700), text='GAME', 
                         font_size=30, size=(600, 70), color=[1, 1, 1, 1])
        label = self.lbl
        for i in range(20):
            for j in range(20):
                new_botton = BOARD.list_of_buttons[i][j]
                self.layout.add_widget(new_botton)

        self.bl.add_widget(label)
        self.bl.add_widget(Button(pos=(600, 700), text='restart', 
                                  size=(100, 70), on_press=self.restart))
        self.bl.add_widget(self.layout)
        return self.bl

    def touch(instance):
        global BOARD
        global IS_GAME
        global label
        y = 19 - int(instance.y // 35)
        x = int(instance.x // 35)

        if type(BOARD.list_of_buttons[y][x]) is BombButton:
            IS_GAME = False
        if not IS_GAME:
            label.text = "GAMEOVER!!!"
        
        if label.text == "GAMEOVER!!!" and type(BOARD.list_of_buttons[y][x]) is BombButton:
            for i in range(20):
                for j in range(20):
                    if type(BOARD.list_of_buttons[i][j]) is BombButton:
                        BOARD.list_of_buttons[i][j].text = '*'
                        BOARD.list_of_buttons[i][j].background_color = [1, 0, 0, 1]
        if label.text != "GAMEOVER!!!":
            BOARD.open((19 - int(instance.y // 35), int(instance.x // 35)))            

        count = 0
        for i in range(20):
            for j in range(20):
                if type(BOARD.list_of_buttons[i][j]) is not BombButton:
                    if BOARD.list_of_buttons[i][j].touch:
                        count += 1  
        if count == 325:
            label.text = "YOU WIN!!!"
            for i in range(20):
                for j in range(20):
                    if type(BOARD.list_of_buttons[i][j]) is BombButton:
                        BOARD.list_of_buttons[i][j].background_color = [.16, .65, .38, 1]
                        BOARD.list_of_buttons[i][j].text='*',


    def restart(self, instance):
        global BOARD
        global IS_GAME
        global label

        self.bl.remove_widget(label)
        self.bl.remove_widget(self.layout)

        self.layout = GridLayout(cols=20, rows=20, size=(700, 700))
        self.lbl = Label(pos=(0, 700), text='GAME', font_size=30, 
                         size=(600, 70), color=[1, 1, 1, 1])
        label = self.lbl
        BOARD = Board()
        for i in range(20):
            for j in range(20):
                new_botton = BOARD.list_of_buttons[i][j]
                self.layout.add_widget(new_botton)

        self.bl.add_widget(label)
        self.bl.add_widget(Button(pos=(600, 700), text='restart', 
                                  size=(100, 70), on_press=self.restart))
        self.bl.add_widget(self.layout)
        
        label.text = "GAME"
        IS_GAME = True

        for i in range(20):
            for j in range(20):
                BOARD.list_of_buttons[i][j].text = ''
                BOARD.list_of_buttons[i][j].background_color = [1, 1, 1, .8]
                BOARD.list_of_buttons[i][j].touch = False
        

class Board:
    def __init__(self):
        self.list_of_buttons = self.gineration()
    
    def open(self, coord):
        if type(self.list_of_buttons[coord[0]][coord[1]]) is BombButton:
            PlayGroundApp.is_game = False
        else:
            self.list_of_buttons[coord[0]][coord[1]].open()

    def gineration(self):      
        board = [[0 for j in range(20)] for i in range(20)]
        for i in range(80):
            index_row = random.randint(0, 19)
            index_col = random.randint(0, 19)
            while board[index_row][index_col] != 0:
                index_row = random.randint(0, 19)
                index_col = random.randint(0, 19)
            
            coord1 = [index_row, index_col]
            coord2 = [index_row, index_col]
            coord3 = [index_row, index_col]
            coord4 = [index_row, index_col]
            coord1[0] -= 1
            coord2[0] += 1
            coord3[1] -= 1
            coord4[1] += 1
            list_of_coord = [coord1, coord2, coord3, coord4]
            list_of_coord = [i for i in list_of_coord if 0 <= i[0] <= 19 and 0 <= i[1] <= 19]
            list_of_coord = [board[coord[0]][coord[1]] for coord in list_of_coord]
            
            while len([1 for elem in list_of_coord if type(elem) is BombButton]) > 0:
                index_row = random.randint(0, 19)
                index_col = random.randint(0, 19)
                
                coord1 = [index_row, index_col]
                coord2 = [index_row, index_col]
                coord3 = [index_row, index_col]
                coord4 = [index_row, index_col]
                coord1[0] -= 1
                coord2[0] += 1
                coord3[1] -= 1
                coord4[1] += 1
                list_of_coord = [coord1, coord2, coord3, coord4]
                list_of_coord = [i for i in list_of_coord if 0 <= i[0] <= 19 and 0 <= i[1] <= 19]
                list_of_coord = [board[coord[0]][coord[1]] for coord in list_of_coord]

            board[index_row][index_col] = BombButton((index_row, index_col), 'bomb',
                                                     on_press=PlayGroundApp.touch, 
                                                     font_size=25,
                                                     background_color=[1, 1, 1, .8])

        for i in range(20):
            for j in range(20):
                if board[i][j] == 0:
                    coord1 = [i, j]
                    coord2 = [i, j]
                    coord3 = [i, j]
                    coord4 = [i, j]
                    coord5 = [i, j]
                    coord6 = [i, j]
                    coord7 = [i, j]
                    coord8 = [i, j]
                    coord1[0] -= 1
                    coord2[0] += 1
                    coord3[1] -= 1
                    coord4[1] += 1

                    coord5[0] -= 1
                    coord5[1] -= 1

                    coord6[0] -= 1
                    coord6[1] += 1

                    coord7[0] += 1
                    coord7[1] -= 1

                    coord8[0] += 1
                    coord8[1] += 1

                    list_of_coord = [coord1, coord2, coord3, coord4, coord5, coord6, coord7, coord8]
                    list_of_coord = [i for i in list_of_coord if 0 <= i[0] <= 19 and 0 <= i[1] <= 19]
                    list_of_coord = [board[coord[0]][coord[1]] for coord in list_of_coord]
                    number_of_bombs = sum([1 for elem in list_of_coord if type(elem) is BombButton])
                    if number_of_bombs:
                        board[i][j] = IntegerButton((i, j), 'integer', 
                                                    on_press=PlayGroundApp.touch, 
                                                    background_color=[1, 1, 1, .8])
                        board[i][j].number = number_of_bombs
                    else:
                        board[i][j] = EmptyButton((i, j), 'empty', 
                                                  on_press=PlayGroundApp.touch, 
                                                  background_color=[1, 1, 1, .8])
        return board


BOARD = Board()
IS_GAME = True
label = ''

if __name__ == '__main__':
    PlayGroundApp().run()