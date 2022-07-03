# Thanks for the URL.
# https://qiita.com/StrayDog/items/203640d9dc7c801dad0f

import tkinter as tk
import threading
import keyboard

class GUI(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        self.master = master # substitute arg for  
        master.geometry("1200x500")
        master.title("Test")

        # setting
        self.count = 0 # labelに定義する値のバッファ
        self.off_color = "gainsboro"
        self.on_color = "coral"
        self.lever_move_pixel = 10
        self.lebal_width = "10"

        # generate Frame test1
        self.test1 = tk.Frame(self.master)#
        self.test1.pack(side = tk.LEFT)

        # generate count text label
        self.label1 = tk.Label(self.test1)
        self.label1.pack(padx = 10, pady=5)
        self.label1["text"] = str(self.count) # labelの値を初期化

        # generate Key state label
        self.label_zero = tk.Label(self.test1, width = self.lebal_width)
        self.label_zero.pack(padx = 10, pady=5)
        self.label_zero["text"] = "0"

        self.label_one = tk.Label(self.test1, width = self.lebal_width)
        self.label_one.pack(padx = 10, pady=5)
        self.label_one["text"] = "1"

        self.label_two = tk.Label(self.test1, width = self.lebal_width)
        self.label_two.pack(padx = 10, pady=5)
        self.label_two["text"] = "2"

        self.label_three = tk.Label(self.test1, width = self.lebal_width)
        self.label_three.pack(padx = 10, pady=5)
        self.label_three["text"] = "3"

        self.label_four = tk.Label(self.test1, width = self.lebal_width)
        self.label_four.pack(padx = 10, pady=5)
        self.label_four["text"] = "4"

        self.label_five = tk.Label(self.test1, width = self.lebal_width)
        self.label_five.pack(padx = 10, pady=5)
        self.label_five["text"] = "5"

        self.label_six = tk.Label(self.test1, width = self.lebal_width)
        self.label_six.pack(padx = 10, pady=5)
        self.label_six["text"] = "6"

        self.label_seven = tk.Label(self.test1, width = self.lebal_width)
        self.label_seven.pack(padx = 10, pady=5)
        self.label_seven["text"] = "7"

        self.label_eight = tk.Label(self.test1, width = self.lebal_width)
        self.label_eight.pack(padx = 10, pady=5)
        self.label_eight["text"] = "8"

        self.label_nine = tk.Label(self.test1, width = self.lebal_width)
        self.label_nine.pack(padx = 10, pady=5)
        self.label_nine["text"] = "9"
        
        # generate Frame test2
        self.test2 = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.test2, bg="white", height=400, width=400)
        self.test2.pack(side = tk.LEFT,expand = True)

        # draw grid
        for i in range(10):
            self.canvas.create_line(0+i*40, 0, 0+i*40, 400, fill= "gainsboro")
            self.canvas.create_line(0, 0+i*40, 400, 0+i*40, fill = "gainsboro")

        # draw lever pos graph
        self.id_oval = self.canvas.create_oval(190, 190, 210, 210, fill = "black")
        self.canvas.pack()

        # draw lever pos text
        self.id_text = self.canvas.create_text(300, 50, text = "X = 0 [%]\nY = 0 [%]", font = ("Times",15))
        #id = self.canvas.create_text(300, 100, text = "Y = 100 [%]")

        '''
        # generate Frame test3
        self.test3 = tk.Frame(self.master)
        self.canvas_right = tk.Canvas(self.test3, bg="white", height=400, width=400)
        self.test3.pack(side = tk.LEFT,expand = True)

        # draw grid
        for i in range(10):
            self.canvas_right.create_line(0+i*40, 0, 0+i*40, 400, fill= "gainsboro")
            self.canvas_right.create_line(0, 0+i*40, 400, 0+i*40, fill = "gainsboro")

        # draw lever pos
        self.id_oval_right = self.canvas_right.create_oval(190, 190, 210, 210, fill = "black")
        self.canvas_right.pack()

        # draw lever pos text
        self.id_text_right = self.canvas_right.create_text(300, 50, text = "X = 0 [%]\nY = 0 [%]", font = ("Times",15))
        '''

        # start thread process
        self.timeEvent()

    # timer start
    def timeEvent(self):
        th = threading.Thread(target=self.update)
        th.start()
        self.after(50, self.timeEvent)

    def update_key_bg(self, label, key):
        if keyboard.is_pressed(key):
            label["bg"] = self.on_color
        else:
            label["bg"] = self.off_color
    

    def update_lever_pos(self, canvas, canvas_id_oval, canvas_id_text, up_key, left_key, down_key, right_key, center_key):
        pos = canvas.coords(canvas_id_oval) # [x0,y0,x1,y1]
        pos_x_center = (pos[0] - 200) / 2
        pos_y_center = - (pos[1] - 200) / 2
        print(pos_x_center)
        print(pos_y_center)
        print("---")

        if keyboard.is_pressed(up_key):
            pos_y_center = min(pos_y_center + self.lever_move_pixel,100)
        elif keyboard.is_pressed(left_key):
            pos_x_center = max(pos_x_center - self.lever_move_pixel,-100)
        elif keyboard.is_pressed(down_key):
            pos_y_center = max(pos_y_center - self.lever_move_pixel,-100)
        elif keyboard.is_pressed(right_key):
            pos_x_center = min(pos_x_center + self.lever_move_pixel,100)
        elif keyboard.is_pressed(center_key):
            pos_x_center = 0
            pos_y_center = 0
        else:
            pass

        if keyboard.is_pressed(up_key) | keyboard.is_pressed(left_key) | keyboard.is_pressed(down_key) | keyboard.is_pressed(right_key) | keyboard.is_pressed(center_key):
            canvas.moveto(canvas_id_oval, pos_x_center * 2 + 200 - 1, - (pos_y_center) * 2 + 200 - 1)
            canvas.itemconfig(canvas_id_text, text = "X = "+str(pos_x_center)+" [%]\nY = "+str(pos_y_center)+" [%]")

    # thread update process
    def update(self):
        self.count += 1
        print(self.count) # デバッグメッセージ
        self.label1["text"] = str(self.count) # labelの値を更新

        self.update_key_bg(self.label_zero, "0")
        self.update_key_bg(self.label_one, "1")
        self.update_key_bg(self.label_two, "2")
        self.update_key_bg(self.label_three, "3")
        self.update_key_bg(self.label_four, "4")
        self.update_key_bg(self.label_five, "5")
        self.update_key_bg(self.label_six, "6")
        self.update_key_bg(self.label_seven, "7")
        self.update_key_bg(self.label_eight, "8")
        self.update_key_bg(self.label_nine, "9")
        self.update_lever_pos(self.canvas, self.id_oval, self.id_text,"w","a","x","d","s")
        # self.update_lever_pos(self.canvas_right, self.id_oval_right, self.id_text_right,"u","h","m","k","j")


if __name__ == "__main__":
    gui = tk.Tk()
    app = GUI(master = gui)
    app.mainloop()