from customtkinter import *
from socket import *
import threading
class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.title('Logitalk')

        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0,y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -5

        self.btn = CTkButton(self, text = '>', command = self.toggle_menu,
                             width = 30)
        self.btn.place(x=0, y=0)
        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x = 30, y = 0)
        self.message_enrty = CTkEntry(self, placeholder_text="Введіть повідомлення", height=40)
        self.message_enrty.place(x=30,y=200)
        self.send_button = CTkButton(self, text='>', width=50, height=40, command = self.send_message)
        self.send_button.place(x=0, y=0)
        self.adaptive_ui()
        self.username = "1488MEn"
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8080))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався"
            self.sock.send(hello.encode())
            threading.Thread(target = self.recv_message, daemon = True).start()
        except Exception as e:
            print(e)

    def add_message(self, message):
        message_frame = CTkFrame(self.chat_field, fg_color='blue')
        message_frame.pack(pady=5, anchor='w')
        CTkLabel(message_frame, text=message, text_color='white', justify='left').pack(
            padx=10, pady=5)

    def send_message(self):
        message = self.message_enrty.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_enrty.delete(0, END)
    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        else:
            self.add_message(line)
    def toggle_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='>')
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='<')
            self.show_menu()
            self.label = CTkLabel(self.menu_frame, text='Введіть text')
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack()
    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label and self.entry:
                self.label.destroy()
                self.entry.destroy()
    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width() - 20)
        self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
        self.message_enrty.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_enrty.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - 110)

        self.after(50, self.adaptive_ui)

window = MainWindow()
window.mainloop()
