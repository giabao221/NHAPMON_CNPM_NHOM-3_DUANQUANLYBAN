import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random, string, json, os
from datetime import datetime, timedelta, time as dtime

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

STATUS_COLORS = {
    "free": "#4CAF50",
    "running": "#FFC107",
    "locked": "#9E9E9E",
    "reserved": "#2196F3",
    "maintenance": "#F44336",
}

# ==============================
# Bộ nhớ giả lập người dùng
# ==============================
class UserStore:
    def __init__(self, filepath="users.json"):
        # username -> {email, password, reset_code, points}
        self.filepath = filepath
        self.users = {}
        self.current_user = None
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except:
                self.users = {}
    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

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
            "points": 0,
        }
        self._save()
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
        self._save()
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
        self._save()
        return True, "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập."
