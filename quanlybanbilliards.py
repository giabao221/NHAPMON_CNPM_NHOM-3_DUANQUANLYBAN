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
# ==============================
# Base frame với thẩm mỹ & layout
# ==============================
class PastelCard(ttk.Frame):
    def __init__(self, parent, title=""):
        super().__init__(parent, padding=16)
        # nền card
        self.card = tk.Frame(self, bg=WHITE, highlightthickness=0)
        self.card.pack(fill="both", expand=True)
        # header
        self.header = tk.Frame(self.card, bg=WHITE)
        self.header.pack(fill="x", pady=(8, 0))
        self.title_label = tk.Label(self.header, text=title, font=FONT_TITLE, fg=PINK_DARK, bg=WHITE)
        self.title_label.pack(anchor="w")

        # body
        self.body = tk.Frame(self.card, bg=WHITE)
        self.body.pack(fill="both", expand=True, pady=8)

        # footer
        self.footer = tk.Frame(self.card, bg=WHITE)
        self.footer.pack(fill="x", pady=(8, 12))

    def add_description(self, text):
        tk.Label(self.body, text=text, font=FONT_SUBTITLE, fg=GRAY_TEXT, bg=WHITE, wraplength=380, justify="left").pack(anchor="w", pady=(0, 8))

    def add_field(self, label, show=None):
        frame = tk.Frame(self.body, bg=WHITE)
        frame.pack(fill="x", pady=6)
        tk.Label(frame, text=label, font=FONT_PRIMARY, fg=GRAY_TEXT, bg=WHITE).pack(anchor="w")
        entry = ttk.Entry(frame, font=FONT_PRIMARY)
        if show:
            entry.configure(show=show)
        entry.pack(fill="x", pady=4)
        return entry

    def add_button(self, text, command, style="Pastel.TButton"):
        btn = ttk.Button(self.footer, text=text, command=command, style=style)
        btn.pack(side="right", padx=6)
        return btn

    def add_link(self, text, command):
        link = tk.Label(self.footer, text=text, font=FONT_SUBTITLE, fg=PINK_DARK, bg=WHITE, cursor="hand2")
        link.bind("<Button-1>", lambda e: command())
        link.pack(side="left", padx=6)
        return link

    def add_banner(self, text, kind="info"):
        color = {"info": PINK_LIGHT, "success": "#E8F6EF", "error": "#FDECEC"}.get(kind, PINK_LIGHT)
        fg = {"info": PINK_DARK, "success": SUCCESS_GREEN, "error": ERROR_RED}.get(kind, PINK_DARK)
        box = tk.Frame(self.body, bg=color)
        box.pack(fill="x", pady=(0, 8))
        tk.Label(box, text=text, font=FONT_SUBTITLE, fg=fg, bg=color, wraplength=380, justify="left").pack(anchor="w", padx=10, pady=8)
# ==============================
# Các trang
# ==============================
class LoginPage(ttk.Frame):
    def __init__(self, parent, app, store):
        super().__init__(parent)
        self.app = app
        self.store = store

        # backdrop
        self.backdrop = AnimatedBackdrop(self)
        self.backdrop.pack(side="left", fill="both", expand=True)

        # card
        self.card = PastelCard(self, title="Đăng nhập")
        self.card.pack(side="right", fill="both", expand=True)

        self.card.add_description("Chào mừng trở lại! Hãy đăng nhập để tiếp tục.")

        self.username = self.card.add_field("Tên người dùng")
        self.password = self.card.add_field("Mật khẩu", show="*")

        self.card.add_link("Quên mật khẩu?", self.goto_forgot)
        self.card.add_link("Chưa có tài khoản? Đăng ký", self.goto_register)
        self.card.add_button("Đăng nhập", self.do_login)

    def goto_forgot(self):
        self.app.show_page("forgot")

    def goto_register(self):
        self.app.show_page("register")

    def do_login(self):
        ok, msg = self.store.login(self.username.get().strip(), self.password.get().strip())
        if ok:
            messagebox.showinfo("Thành công", msg)
            self.app.show_page("tables")
        else:
            self.card.add_banner(msg, kind="error")

class RegisterPage(ttk.Frame):
    def __init__(self, parent, app, store):
        super().__init__(parent)
        self.app = app
        self.store = store

        self.backdrop = AnimatedBackdrop(self)
        self.backdrop.pack(side="left", fill="both", expand=True)

        self.card = PastelCard(self, title="Đăng ký")
        self.card.pack(side="right", fill="both", expand=True)

        self.card.add_description("Tạo tài khoản mới với vài bước đơn giản.")

        self.username = self.card.add_field("Tên người dùng")
        self.email = self.card.add_field("Email")
        self.password = self.card.add_field("Mật khẩu", show="*")
        self.confirm = self.card.add_field("Xác nhận mật khẩu", show="*")

        self.card.add_link("Đã có tài khoản? Đăng nhập", self.goto_login)
        self.card.add_button("Tạo tài khoản", self.do_register)

    def goto_login(self):
        self.app.show_page("login")

    def do_register(self):
        u = self.username.get().strip()
        e = self.email.get().strip()
        p = self.password.get().strip()
        c = self.confirm.get().strip()
        if p != c:
            self.card.add_banner("Mật khẩu xác nhận không khớp.", kind="error")
            return
        ok, msg = self.store.register(u, e, p)
        if ok:
            self.card.add_banner(msg, kind="success")
        else:
            self.card.add_banner(msg, kind="error")

class ForgotPage(ttk.Frame):
    def __init__(self, parent, app, store):
        super().__init__(parent)
        self.app = app
        self.store = store

        self.backdrop = AnimatedBackdrop(self)
        self.backdrop.pack(side="left", fill="both", expand=True)

        self.card = PastelCard(self, title="Quên mật khẩu")
        self.card.pack(side="right", fill="both", expand=True)

        self.card.add_description("Nhập tên người dùng hoặc email. Bạn sẽ nhận được mã để đặt lại mật khẩu.")

        self.target = self.card.add_field("Tên người dùng / Email")

        self.card.add_link("Đã nhớ mật khẩu? Đăng nhập", self.goto_login)
        self.card.add_link("Có mã rồi? Đặt lại mật khẩu", self.goto_reset)
        self.card.add_button("Gửi mã đặt lại", self.do_request)

    def goto_login(self):
        self.app.show_page("login")

    def goto_reset(self):
        self.app.show_page("reset")

    def do_request(self):
        t = self.target.get().strip()
        ok, msg = self.store.request_reset(t)
        if ok:
            # Hiển thị mã để người dùng dùng ở trang đặt lại
            self.card.add_banner(msg, kind="info")
        else:
            self.card.add_banner(msg, kind="error")

class ResetPage(ttk.Frame):
    def __init__(self, parent, app, store):
        super().__init__(parent)
        self.app = app
        self.store = store

        self.backdrop = AnimatedBackdrop(self)
        self.backdrop.pack(side="left", fill="both", expand=True)

        self.card = PastelCard(self, title="Đặt lại mật khẩu")
        self.card.pack(side="right", fill="both", expand=True)

        self.card.add_description("Nhập tên người dùng, mã xác nhận và mật khẩu mới.")

        self.username = self.card.add_field("Tên người dùng")
        self.code = self.card.add_field("Mã xác nhận")
        self.new_password = self.card.add_field("Mật khẩu mới", show="*")
        self.confirm = self.card.add_field("Xác nhận mật khẩu", show="*")

        self.card.add_link("Quay về đăng nhập", self.goto_login)
        self.card.add_button("Đặt lại", self.do_reset)

    def goto_login(self):
        self.app.show_page("login")

    def do_reset(self):
        u = self.username.get().strip()
        code = self.code.get().strip()
        p1 = self.new_password.get().strip()
        p2 = self.confirm.get().strip()
        if p1 != p2:
            self.card.add_banner("Mật khẩu xác nhận không khớp.", kind="error")
            return
        ok, msg = self.store.reset_password(u, code, p1)
        if ok:
            self.card.add_banner(msg, kind="success")
        else:
            self.card.add_banner(msg, kind="error")

class HomePage(ttk.Frame):
    def __init__(self, parent, app, store):
        super().__init__(parent)
        self.app = app
        self.store = store

        self.backdrop = AnimatedBackdrop(self)
        self.backdrop.pack(side="left", fill="both", expand=True)

        self.card = PastelCard(self, title="Trang chính")
        self.card.pack(side="right", fill="both", expand=True)

        self.welcome_label = tk.Label(self.card.body, text="", font=FONT_PRIMARY, fg=PINK_DARK, bg=WHITE)
        self.welcome_label.pack(anchor="w", pady=(0, 10))
        self.card.add_description("Bạn đã đăng nhập thành công. Khám phá ứng dụng với phong cách pastel dịu mắt.")

        self.card.add_button("Đăng xuất", self.do_logout, style="Danger.TButton")

    def tkraise(self, aboveThis=None):
        # cập nhật lời chào động khi vào trang
        if self.store.current_user:
            self.welcome_label.config(text=f"Xin chào, {self.store.current_user} ✨")
        else:
            self.welcome_label.config(text="")
        super().tkraise(aboveThis)

    def do_logout(self):
        self.store.logout()
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất.")
        self.app.show_page("login")