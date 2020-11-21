import tkinter as tk
from functools import partial
import random
#Разрешение окна
WIDTH = 600
HEIGHT = 600
root = tk.Tk()

class Cell:
    """Класс клетки на поле"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #С этими полями работать через гетеры/сеттеры
        self._isbomb = None
        self.value = None
        self.isclicked = False

    #TODO
    def click(self):
        """Обработка нажатия на кнопку"""
        self.isclicked = True
        print("На меня нажали")
        print("Мои координаты: {}, {}".format(self.x, self.y))

    @property
    def isbomb(self):
        return self._isbomb

    @isbomb.setter
    def isbomb(self, value):
        """Выставление бомбы"""
        self._isbomb = value
        self.value = "*"

class Field:
    """Класс игрового поля"""

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix = None
        self.buttons_matrix = None
        self.generation()
        self.filler()
        self.buttonsmatrix_generation()
        self.synchronizer()

    def filler(self):
        """Заполнение матрицы данными"""
        
        matrix = self.matrix

        #Логика расстановки бомб на игровом поле
        bomb_counter = 0
        #TODO ПОМЕНЯТЬ
        while bomb_counter < (5):
            x_coord, y_coord = random.randint(0, self.n-1), random.randint(0, self.m-1)
            #Если выбранная клетка не бомба, то она станет бомбой
            if not matrix[x_coord][y_coord].isbomb:
                matrix[x_coord][y_coord].isbomb = True
                bomb_counter += 1

        #Логика выставления чисел
        for i in range(self.n):
            for j in range(self.m):
                # Если это не бомба - присваиваем ей значение
                if not matrix[i][j].isbomb:
                    buf_value = 0
                    for a in range(3):
                        for b in range(3):
                            if (0<=(i-1+a)<self.n) and (0<=(j-1+b)<self.m) and (matrix[i-1+a][j-1+b].isbomb):
                                buf_value+=1 #Если клетка внутри поля и это бомба, то считаем
                    matrix[i][j].value = buf_value
        
        self.matrix = matrix

    def button_clicker(self, coords):
        """Обработка нажатия на button на уровне tkinter"""
        x, y = coords
        self.matrix[x][y].click()

        #TODO Если значение ячейки 0, то раскрываем соседние ячейки до тех пор, пока не до дойдем до ячейки с числом
        if self.matrix[x][y].value == 0:
            self.recursion_clicker(x, y)

        self.synchronizer()

    def recursion_clicker(self, x, y):
        """Рекурсивное раскрытитие соседних ячеек"""
        try:
            self.matrix[x][y].click()
        except IndexError:
            return
        print(self.matrix[x][y].value)
        if self.matrix[x][y].value == 0:
            self.recursion_clicker(x-1, y)
            self.recursion_clicker(x-1, y+1)
            self.recursion_clicker(x-1, y-1)

            self.recursion_clicker(x+1, y)
            self.recursion_clicker(x+1, y+1)
            self.recursion_clicker(x+1, y-1)
        else:
            return


    def generation(self):
        """Генерация основной матрицы"""
        matrix = []
        for i in range(self.n):
            buf_matrix = []
            for j in range(self.m):
                buf_matrix.append(Cell(i, j))
            matrix.append(buf_matrix)
        self.matrix = matrix

    def buttonsmatrix_generation(self):
        """Генерация матрицы buttonов"""

        buttons_matrix = []
        for c in range(self.n):
            row = []
            for r in range(self.m):
                action = partial(self.button_clicker, (c,r))
                button = tk.Button(root, text=str(self.matrix[c][r].value), command=action)
                button.grid(row=r, column=c)
                row.append(button)
            buttons_matrix.append(row)
        self.buttons_matrix = buttons_matrix
    
    #TODO
    def synchronizer(self):
        """Синхронизация значений в self.matrix с buttons_matrix"""
        #TODO Проверить, чтоб все цвета существовали в tkinter
        number2color_dict = {
            "0" : "white",
            "1" : "blue2",
            "2" : "green2",
            "3" : "red2",
            "4" : "cyan",
            "5" : "red4",
            "6" : "purple1",
            "7" : "yellow",
            "8" : "magenta2",
            "*" : "black",
        }
        for c in range(self.n):
            for r in range(self.m):
                #Если нет нажатия на button - значение неизвестно
                if not self.matrix[c][r].isclicked:           
                    self.buttons_matrix[c][r].config(text="    ")
                else:
                    value = self.matrix[c][r].value
                    self.buttons_matrix[c][r].config(text=" {} ".format(str(value).replace("0", "  ")), disabledforeground=number2color_dict[str(value)], state=tk.DISABLED, bg="#b8b8b8", relief="flat")

    def __str__(self):
        """Вывод матрицы на экран"""
        matrix = self.matrix
        for i in range(self.n):
            for j in range(self.m):
                print(matrix[i][j].value, end=' ')
            print('')
        return ""
    
def main():
    
    #Инициализация канваса
    c = tk.Canvas(root, width=WIDTH, heigh=HEIGHT)
    root.title("Сапёр")

    #Экземпляр игрового поля
    field_obj = Field(10,10)
    print(field_obj)
    
    root.mainloop()
    

if __name__ == "__main__":
    main()