import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import time

# ==============================
# Cấu hình màu sắc & chủ đề
# ==============================
PASTEL_PINK = "#F0B2C7"     # màu chủ đạo
PINK_DARK = "#C77CA8"       # nhấn
PINK_LIGHT = "#F8D9E4"      # nền phụ
WHITE = "#FFFFFF"
GRAY_TEXT = "#6B6B6B"
SUCCESS_GREEN = "#3CB371"
ERROR_RED = "#D9534F"

FONT_PRIMARY = ("Nunito", 12)
FONT_TITLE = ("Nunito", 18, "bold")
FONT_SUBTITLE = ("Nunito", 11)
FONT_BUTTON = ("Nunito", 12, "bold")
FONT_CODE = ("Consolas", 11)

# ==============================
# Bộ nhớ giả lập người dùng
# ==============================
class UserStore:
    def __init__(self):
        # username -> {email, password, reset_code}
        self.users = {}
        self.current_user = None

    def register(self, username, email, password):
        if not username or not email or not password:
            return False, "Vui lòng điền đầy đủ thông tin."
        if username in self.users:
            return False, "Tên người dùng đã tồn tại."
        if len(password) < 6:
            return False, "Mật khẩu cần ít nhất 6 ký tự."
        self.users[username] = {
            "email": email,
            "password": password,
            "reset_code": None,
        }
        return True, "Đăng ký thành công! Bạn có thể đăng nhập."

    def login(self, username, password):
        if username not in self.users:
            return False, "Không tìm thấy người dùng."
        if self.users[username]["password"] != password:
            return False, "Mật khẩu không chính xác."
        self.current_user = username
        return True, f"Xin chào {username}!"

    def logout(self):
        self.current_user = None

    def request_reset(self, username_or_email):
        # Tìm theo username hoặc email
        target = None
        if username_or_email in self.users:
            target = username_or_email
        else:
            for u, info in self.users.items():
                if info["email"] == username_or_email:
                    target = u
                    break
        if not target:
            return False, "Không tìm thấy tài khoản với thông tin cung cấp."
        # Tạo mã reset 6 ký tự
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.users[target]["reset_code"] = code
        # Demo: Hiển thị mã ngay. Thực tế: gửi email/sms.
        return True, f"Mã đặt lại mật khẩu của bạn là: {code}"

    def reset_password(self, username, code, new_password):
        if username not in self.users:
            return False, "Không tìm thấy người dùng."
        info = self.users[username]
        if not code or code != info.get("reset_code"):
            return False, "Mã xác nhận không hợp lệ."
        if len(new_password) < 6:
            return False, "Mật khẩu cần ít nhất 6 ký tự."
        info["password"] = new_password
        info["reset_code"] = None
        return True, "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập."