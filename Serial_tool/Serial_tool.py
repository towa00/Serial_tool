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
        # �I���{�^���쐬
        quit_btn = tk.Button(self, text="close", command=self.root.destroy)
        quit_btn.pack(side="bottom")
        
        # �e�L�X�g�{�b�N�X�̍쐬
        self.text_box = tk.Text(self, width=7000, height=500)
        self.text_box.pack()

        # �X�N���[���o�[�̒ǉ�
        scrollbar = Scrollbar(self, command=self.text_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=scrollbar.set)
        
        # Serial�ʐM
        self.start_serial_thread()  # start_serial_thread���Ăяo��

    def read_serial(self):
        while 1:
            string = readSer.readline().decode("utf-8") # �P�s���o��
            self.text_box.insert(END, string)           # �e�L�X�g�{�b�N�X�ɕ����o��
            self.text_box.see(END)                      # �e�L�X�g�{�b�N�X���Ō�܂ŃX�N���[��
            self.master.update_idletasks()              # �C�x���g�����̎��s

    def start_serial_thread(self):
        #Serial�ʐM���s���X���b�h���J�n
        serial_thread = threading.Thread(target=self.read_serial)
        serial_thread.start()
        
    def close_application(self):
        #�E�B���h�E������ꂽ���ɌĂ΂��֐�
        readSer.close()
        self.root.destroy()
        
    def on_closing(self):
        # �E�B���h�E��������Ƃ��̏���
        # �X���b�h���I�������Ă���E�B���h�E�����
        if hasattr(self, 'serial_thread') and self.serial_thread.is_alive():
            self.serial_thread.join()
        self.root.destroy()

root = tk.Tk()
root.title("Test")
root.geometry("800x600")

app = Application(root=root)
app.mainloop()

