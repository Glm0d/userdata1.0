import subprocess
import socket
import platform
import tkinter as tk
from pynput import keyboard

COMBINATION = {keyboard.Key.ctrl_l, keyboard.Key.alt_l}
current = set()

def on_press(key):
    global current
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            on_activate()

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def get_system_info():
    try:
        # سحب المطلوب من CMD
       username = subprocess.run("whoami", capture_output=True, text=True).stdout.strip()
       hostname = socket.gethostname()
       ip_address = socket.gethostbyname_ex(hostname)
       win_platform = platform.platform()
       serial_number = subprocess.check_output("wmic bios get serialnumber", shell=True, text=True).split('\n')[2].strip()
        
       info = f"ℹ️ Windows Platform: {win_platform}\n👤 User Name: {username}\n🏠 Hostname: {hostname}\n🌐 IP Address: {ip_address}\n🔢 Serial Number: {serial_number}"
       return info
    except Exception as e:
        return f"❌ Error getting system information: {str(e)}"

def on_activate():
    global root
    system_info = get_system_info()
    info_label.config(text=system_info)
    root.deiconify()
    root.focus()
    
def on_close():
    root.withdraw()

# إعداد نافذة التطبيق
root = tk.Tk()
root.title("معلومات العميل")
root.configure(bg="lightblue") 
root.withdraw()

info_label = tk.Label(root, text="Press Ctrl + Alt to get system info", font=("Arial", 16, "bold"), fg="navy", bg="lightblue")
info_label.pack(pady=20)

close_button = tk.Button(root, text="Close", command=on_close, bg="navy", fg="white", font=("Arial", 12, "bold"))
close_button.pack()

# ربط دالة on_root_closed مع حدث إغلاق النافذة
root.protocol("WM_DELETE_WINDOW", on_close)

# استماع للمفاتيح
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    root.mainloop()
