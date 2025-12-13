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
# ==============================
# Họa tiết hoạt họa nền (Canvas)
# ==============================
class AnimatedBackdrop(ttk.Frame):
    def __init__(self, parent, width=420, height=520):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=PASTEL_PINK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.items = []
        self.width = width
        self.height = height
        self._create_shapes()
        self._animate()

    def _create_shapes(self):
        # Bong bóng (circles), hoa (petals), sao (stars)
        for _ in range(10):
            r = random.randint(16, 34)
            x = random.randint(r, self.width - r)
            y = random.randint(r, self.height - r)
            color = random.choice([WHITE, PINK_LIGHT, "#FFD1DC", "#E8AFCF"])
            item = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")
            self.items.append({"id": item, "dx": random.uniform(-0.5, 0.5), "dy": random.uniform(0.3, 0.8)})

        # Sao đơn giản (polygons)
        for _ in range(6):
            cx = random.randint(40, self.width - 40)
            cy = random.randint(40, self.height - 40)
            size = random.randint(10, 18)
            color = random.choice([WHITE, "#FFF0F6", "#FFE4EF"])
            points = self._star_points(cx, cy, size, 5)
            item = self.canvas.create_polygon(points, fill=color, outline="")
            self.items.append({"id": item, "dx": random.uniform(-0.4, 0.4), "dy": random.uniform(-0.3, 0.5)})

        # Petals (giọt nước)
        for _ in range(8):
            w = random.randint(14, 24)
            h = random.randint(24, 40)
            x = random.randint(w, self.width - w)
            y = random.randint(h, self.height - h)
            color = random.choice(["#FDE1E8", "#F9C6D5", "#FFD8E2"])
            item = self.canvas.create_oval(x-w//2, y-h//2, x+w//2, y+h//2, fill=color, outline="")
            self.items.append({"id": item, "dx": random.uniform(-0.2, 0.6), "dy": random.uniform(-0.5, 0.4)})

    def _star_points(self, cx, cy, r, n=5):
        # tạo điểm ngôi sao
        pts = []
        for i in range(2 * n):
            angle = i * (3.14159 / n)
            rr = r if i % 2 == 0 else r / 2.4
            x = cx + rr * math_cos(angle)
            y = cy + rr * math_sin(angle)
            pts.extend([x, y])
        return pts

    def _animate(self):
        # chuyển động nhẹ nhàng, chống vượt biên
        for it in self.items:
            self.canvas.move(it["id"], it["dx"], it["dy"])
            x1, y1, x2, y2 = self.canvas.bbox(it["id"])
            if x1 < 0 or x2 > self.width:
                it["dx"] = -it["dx"]
            if y1 < 0 or y2 > self.height:
                it["dy"] = -it["dy"]
        self.after(30, self._animate)

# helper trig to avoid importing math for small footprint
def math_sin(x):
    # Taylor series approx (sufficient for visuals); or import math for precision
    import math
    return math.sin(x)

def math_cos(x):
    import math
    return math.cos(x)