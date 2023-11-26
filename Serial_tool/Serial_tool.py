import serial
import tkinter as tk
from tkinter import END, Scrollbar
import threading

readSer = serial.Serial("COM3", 115200)

class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=800, height=600, borderwidth=4, relief="groove")
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # 終了ボタン作成
        quit_btn = tk.Button(self, text="close", command=self.root.destroy)
        quit_btn.pack(side="bottom")
        
        # テキストボックスの作成
        self.text_box = tk.Text(self, width=7000, height=500)
        self.text_box.pack()

        # スクロールバーの追加
        scrollbar = Scrollbar(self, command=self.text_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=scrollbar.set)
        
        # Serial通信
        self.start_serial_thread()  # start_serial_threadを呼び出す

    def read_serial(self):
        while 1:
            string = readSer.readline().decode("utf-8") # １行ずつ出力
            self.text_box.insert(END, string)           # テキストボックスに文字出力
            self.text_box.see(END)                      # テキストボックスを最後までスクロール
            self.master.update_idletasks()              # イベント処理の実行

    def start_serial_thread(self):
        #Serial通信を行うスレッドを開始
        serial_thread = threading.Thread(target=self.read_serial)
        serial_thread.start()
        
    def close_application(self):
        #ウィンドウが閉じられた時に呼ばれる関数
        readSer.close()
        self.root.destroy()
        
    def on_closing(self):
        # ウィンドウが閉じられるときの処理
        # スレッドを終了させてからウィンドウを閉じる
        if hasattr(self, 'serial_thread') and self.serial_thread.is_alive():
            self.serial_thread.join()
        self.root.destroy()

root = tk.Tk()
root.title("Test")
root.geometry("800x600")

app = Application(root=root)
app.mainloop()

