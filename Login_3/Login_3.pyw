from customtkinter import *
from PIL import Image
from CTkMessagebox import CTkMessagebox
import time, threading
import os
import sys
import subprocess
# الاسم المستخدم والرقم السري في السطر 80 في حال اردنا التغير 

 
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x620+200+40")
        self.root.configure(fg_color="#808080")
        self.root.resizable(False, False)
        #self.root.set_default_color_theme("dark-blue")
        Height = 12
        Width = 300
        icon_size = 35
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        # اضافة صورة لخلفية الواجهة 
        spotify_image = CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(75, 75))
        email_image = CTkImage(Image.open(os.path.join(image_path, "mail.png")), size=(icon_size, icon_size))
        password_image = CTkImage(Image.open(os.path.join(image_path, "lock.png")), size=(icon_size, icon_size))

        self.loginframe = CTkFrame(self.root, fg_color="#111", corner_radius=15)

        CTkLabel(self.loginframe, text=" Login", image=spotify_image, compound=LEFT, font=("monospace", 40, "bold"), text_color="white").pack(pady=20, side=TOP, anchor="nw", padx=100)

        CTkLabel(self.loginframe, text="Login to create account", font=("monospace", 30, "bold"), text_color="white").pack(pady=13)

        self.username_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        CTkLabel(self.username_frame, text="", image=email_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.usernameInput = CTkEntry(self.username_frame, placeholder_text="Email or username", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="#f3f3f3", fg_color="transparent", border_width=0)
        self.usernameInput.pack(side=LEFT, ipady=15)
        self.username_frame.pack(pady=10, ipadx=10, ipady=2 , anchor="center")

        self.password_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="#333")
        CTkLabel(self.password_frame, text="", image=password_image, fg_color="transparent", corner_radius=0).pack(side=LEFT, padx=10)
        self.passwordInput = CTkEntry(self.password_frame, placeholder_text="Password", font=("monospace", 20, "bold"), 
                                         height=Height, width=Width, text_color="white", fg_color="transparent", border_width=0, show="*")
        self.passwordInput.pack(side=LEFT, ipady=10)
        self.password_frame.pack(pady=5, ipadx=10, ipady=2, anchor="center")

        self.show_password_btn = CTkCheckBox(self.loginframe, text=" Show Password", font=("Canbera", 21), command=self.show_password)
        self.show_password_btn.pack(pady=15, side=TOP, anchor="nw", padx=65)

        self.loginBtn = CTkButton(self.loginframe, text="LOG IN", text_color="black", font=("monospace", 20, "bold"), fg_color="white", corner_radius=10,
                                     hover_color="#dcdada", command=self.login)
        self.loginBtn.pack(side=TOP, fill=X, padx=55, pady=10, ipady=10)

        self.loginframe.pack(side=TOP, fill=BOTH, expand=True, pady=50, padx=260, ipady=10)

        progressbar_frame = CTkFrame(self.loginframe, height=0, width=0, fg_color="transparent")
        self.progressbar = CTkProgressBar(self.loginframe,  orientation="horizontal", mode="determinate", determinate_speed=1, 
                                             fg_color="white", height=5, progress_color="#1ED765", corner_radius=0, )
        self.progressbar.set(0)
        self.progressbar.pack(side=BOTTOM, fill=X)
        progressbar_frame.pack(side=BOTTOM, fill=X)

        self.thread = threading.Thread(target=self.loading)

    def show_password(self):
        self.passwordInput.configure(show="")
        self.show_password_btn.configure(command=self.hide_password)

    def hide_password(self):
        self.passwordInput.configure(show="#")
        self.show_password_btn.configure(command=self.show_password)

    def login(self):
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        if len(username) == 0 or len(password) == 0:
            CTkMessagebox(title="Error", message=" Username or Password can't be empty ", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)
        elif username == "mohammad" and password == "admin":
            global user_name 
            user_name = username
            self.progressbar.start()
            self.thread.start()
        else:
            CTkMessagebox(title="Error", message="Invalid username or password", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)

    def loading(self):
        time.sleep(1.1)
        self.progressbar.stop()
        self.progressbar.set(100)

        try:
            # Get the absolute path to main_project.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_project_path = os.path.join(os.path.dirname(current_dir), "main_project.py")
            
            # Get Python path
            python_path = os.path.join(os.path.dirname(sys.executable), "python.exe")
            
            # Close the login window
            self.root.quit()
            
            # Run the main project with the correct Python path
            subprocess.Popen([python_path, main_project_path])
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to start main application: {str(e)}", icon="cancel", font=("monospace", 15, "bold"), text_color="white", wraplength=600)

root = CTk(fg_color="black")
root.title("Login Page")
root.iconbitmap("Login_3/images/logo.ico")

LoginPage(root)

root.mainloop()