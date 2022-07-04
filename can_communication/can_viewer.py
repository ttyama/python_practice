# Thanks for the URL.
# https://qiita.com/StrayDog/items/203640d9dc7c801dad0f


import tkinter as tk
from tkinter import scrolledtext 
import threading
import can
import subprocess

class CAN_CONTROL():
    def __init__(self):
        pass

    def send_msg(self,msg1,msg2):
        with can.interface.Bus() as bus:
            try:
                bus.send(msg1)
                bus.send(msg2)
                print(f"Message sent on {bus.channel_info} \n")
            except can.CanError:
                print("Message NOT sent \n")

    def recv_msg(self):
        with can.interface.Bus() as bus:
            try:
                msg1 = bus.recv()
                msg2 = bus.recv()
                print(f"Message received on {bus.channel_info} \n")
                return msg1, msg2
            except can.CanError:
                print("Message NOT receive \n")

class GUI(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        
        self.master = master # substitute arg for  
        master.geometry("1200x800")
        master.title("Test")

        # setting
        self.count = 0 # labelに定義する値のバッファ

        # generate Frame test1
        self.test = tk.Frame(self.master, borderwidth=10, relief='solid')
        self.test.pack(expand = True, fill='both')

        # generate count text label
        self.label = tk.Label(self.test)
        self.label.pack(padx = 10, pady=5, side = tk.TOP)
        self.label["text"] = str(self.count)

        # generate scrorrled text for send message
        self.text_area_send = scrolledtext.ScrolledText(self.test)
        self.text_area_send.pack(side = tk.TOP, expand = True, fill = tk.X)

        # generate scrolled text fot received message
        self.text_area_receive = scrolledtext.ScrolledText(self.test)
        self.text_area_receive.pack(side = tk.TOP, expand = True, fill = tk.X)        

        # make instance of CAN_CONTROL class
        self.can_control = CAN_CONTROL()

        # start thread process
        self.timeEvent()

    # timer start
    def timeEvent(self):
        th = threading.Thread(target=self.update)
        th.start()
        self.after(500, self.timeEvent)

    # thread update process
    def update(self):
        if self.count == 255:
            self.count = 0
        else:
            self.count += 1
        self.label["text"] = str(self.count)

        # generate messages
        tx_msg1 = can.Message(arbitration_id=0xC0FFEE, data=[self.count, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True)
        tx_msg2 = can.Message(arbitration_id=0xC0FFEF, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True)

        # send data
        self.can_control.send_msg(tx_msg1,tx_msg2)

        # send data view
        self.text_area_send.insert(tk.END, str(tx_msg1) + "\n")
        self.text_area_send.insert(tk.END, str(tx_msg2) + "\n")
        self.text_area_send.see(tk.END)

        # receive data
        rx_msg1,rx_msg2 = self.can_control.recv_msg()
        
        # receive data view
        self.text_area_receive.insert(tk.END, str(rx_msg1) + "\n")
        self.text_area_receive.insert(tk.END, str(rx_msg2) + "\n")
        self.text_area_receive.see(tk.END)

if __name__ == "__main__":
    gui = tk.Tk()
    app = GUI(master = gui)
    app.mainloop()