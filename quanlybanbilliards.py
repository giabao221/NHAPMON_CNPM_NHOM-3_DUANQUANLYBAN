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

# ==============================
# Ứng dụng chính
# ==============================
class PastelAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quan ly ban BILLIARDS")
        self.geometry("860x520")
        self.minsize(900, 600)
        self.configure(bg=PASTEL_PINK)
        self._center()

        self.store = UserStore()
        self._setup_style()

        container = ttk.Frame(self, style="Root.TFrame")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # tạo các trang
        self.pages = {
            "login": LoginPage(container, self, self.store),
            "register": RegisterPage(container, self, self.store),
            "forgot": ForgotPage(container, self, self.store),
            "reset": ResetPage(container, self, self.store),
            "home": HomePage(container, self, self.store),
        }

        # đặt layout stack
        for p in self.pages.values():
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("login")

        # thanh tiêu đề nhỏ (fake) pastel
        self._build_topbar()

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 3
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_style(self):
        style = ttk.Style(self)
        # sử dụng theme 'clam' cho linh hoạt màu
        style.theme_use("clam")

        style.configure("Root.TFrame", background=PASTEL_PINK)

        # Entry
        style.configure("TEntry", padding=8, fieldbackground=WHITE, bordercolor=PINK_LIGHT, lightcolor=PINK_LIGHT, darkcolor=PINK_LIGHT, foreground="#303030")
        style.map("TEntry", bordercolor=[("focus", PINK_DARK)], lightcolor=[("focus", PINK_DARK)], darkcolor=[("focus", PINK_DARK)])

        # Button chính
        style.configure("Pastel.TButton",
                        font=FONT_BUTTON,
                        foreground=WHITE,
                        background=PINK_DARK,
                        padding=8,
                        borderwidth=0)
        style.map("Pastel.TButton",
                  background=[("active", "#B36494")])

        # Button nguy cơ (logout)
        style.configure("Danger.TButton",
                        font=FONT_BUTTON,
                        foreground=WHITE,
                        background=ERROR_RED,
                        padding=8,
                        borderwidth=0)
        style.map("Danger.TButton",
                  background=[("active", "#C5423E")])

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=PINK_LIGHT, height=42)
        topbar.pack(fill="x", side="top")
        tk.Label(topbar, text="Quan ly ban BIllIARDS", font=FONT_TITLE, fg=PINK_DARK, bg=PINK_LIGHT).pack(side="left", padx=12)
        nav = tk.Frame(topbar, bg=PINK_LIGHT)
        nav.pack(side="right", padx=8)
        # các nút chuyển nhanh
        ttk.Button(nav, text="Đăng nhập", style="Pastel.TButton", command=lambda: self.show_page("login")).pack(side="left", padx=4)
        ttk.Button(nav, text="Đăng ký", style="Pastel.TButton", command=lambda: self.show_page("register")).pack(side="left", padx=4)
        ttk.Button(nav, text="Quên mật khẩu", style="Pastel.TButton", command=lambda: self.show_page("forgot")).pack(side="left", padx=4)

    def show_page(self, name):
        page = self.pages.get(name)
        if not page:
            return
        page.tkraise()
# ==============================
# Tiện ích serialize/deserialize thời gian
# ==============================
def dt_to_str(dt):
    return dt.isoformat() if dt else None

def str_to_dt(s):
    return datetime.fromisoformat(s) if s else None

def time_to_str(t: dtime):
    return f"{t.hour:02d}:{t.minute:02d}"

def str_to_time(s: str):
    h, m = map(int, s.split(":"))
    return dtime(h, m)

# ==============================
# Trang Order: thêm món, phục vụ, in phiếu/hóa đơn, thanh toán
# ==============================
class OrderPage(ttk.Frame):
    def __init__(self, parent, app, beer: BeerStore):
        super().__init__(parent); self.app = app; self.beer = beer; self.order_id = None

        header = tk.Frame(self, bg=WHITE); header.pack(fill="x", padx=10, pady=10)
        self.title = tk.Label(header, text="Order", font=FONT_TITLE, fg=PINK_DARK, bg=WHITE)
        self.title.pack(side="left")
        ttk.Button(header, text="Về bàn", style="Pastel.TButton", command=lambda: self.app.show_page("tables")).pack(side="right", padx=6)

        body = tk.Frame(self, bg=WHITE); body.pack(fill="both", expand=True, padx=10, pady=10)
        # items table
        self.tree = ttk.Treeview(body, columns=("product","qty","price","discount","served"), show="headings", height=10)
        for c, w in [("product",180),("qty",60),("price",100),("discount",100),("served",80)]:
            self.tree.heading(c, text=c.capitalize()); self.tree.column(c, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # add item controls
        ctrl = tk.Frame(body, bg=WHITE); ctrl.pack(fill="x", pady=8)
        self.product_var = tk.StringVar(); self.qty_var = tk.StringVar(value="1")
        prod_names = [f"{p['id']} - {p['name']} ({p['base_price']:.0f})" for p in self.beer.products.values()]
        ttk.Combobox(ctrl, textvariable=self.product_var, values=prod_names, state="readonly", width=40).pack(side="left", padx=6)
        ttk.Entry(ctrl, textvariable=self.qty_var, width=6).pack(side="left", padx=6)
        ttk.Button(ctrl, text="Thêm món", style="Pastel.TButton", command=self.add_item).pack(side="left", padx=6)
        ttk.Button(ctrl, text="Phục vụ (trừ kho)", style="Pastel.TButton", command=self.serve_selected).pack(side="left", padx=6)

        # totals
        self.totals = tk.Label(body, text="", font=FONT_SUBTITLE, fg=GRAY_TEXT, bg=WHITE)
        self.totals.pack(anchor="e")

        # actions
        actions = tk.Frame(body, bg=WHITE); actions.pack(fill="x", pady=6)
        ttk.Button(actions, text="In phiếu", style="Pastel.TButton", command=self.print_ticket).pack(side="left", padx=6)
        ttk.Button(actions, text="Xem hóa đơn", style="Pastel.TButton", command=self.print_invoice).pack(side="left", padx=6)
        self.pay_method = tk.StringVar(value="cash")
        ttk.Combobox(actions, textvariable=self.pay_method, values=["cash","card","momo"], state="readonly", width=10).pack(side="right", padx=6)
        ttk.Button(actions, text="Thanh toán", style="Danger.TButton", command=self.pay).pack(side="right", padx=6)

    def set_order(self, order_id):
        self.order_id = order_id
        self.refresh()

    def refresh(self):
        if not self.order_id: return
        order = self.beer.orders[self.order_id]
        tbl = self.beer.tables[order["table_id"]]
        self.title.config(text=f"Order #{order['id']} • Bàn {tbl['code']} • {order['status']}")
        # reload items
        for i in self.tree.get_children(): self.tree.delete(i)
        for it in [x for x in self.beer.order_items if x["order_id"] == self.order_id]:
            self.tree.insert("", "end", iid=str(it["id"]), values=(
                it["product_id"], it["qty"], f"{it['unit_price']:.0f}", f"{it['discount']:.0f}", "Yes" if it["served"] else "No"
            ))
        # totals
        self.beer.recalc_order(self.order_id)
        o = self.beer.orders[self.order_id]
        self.totals.config(text=f"Tạm tính: {o['subtotal']:.0f} | Tiền giờ: {o['time_charge']:.0f} | Giảm giá ({o['voucher_code'] or 'auto'}): {o['discount']:.0f} | Tổng: {o['total']:.0f}")

    def add_item(self):
        if not self.product_var.get(): return
        try:
            pid = int(self.product_var.get().split(" - ")[0]); qty = float(self.qty_var.get())
        except:
            messagebox.showerror("Lỗi", "Chọn sản phẩm và số lượng hợp lệ."); return
        ok, msg = self.beer.add_item(self.order_id, pid, qty)
        if not ok: messagebox.showerror("Lỗi", msg)
        self.refresh()

    def serve_selected(self):
        sel = self.tree.selection()
        if not sel: return
        item_id = int(sel[0])
        ok, msg = self.beer.serve_item(item_id)
        if not ok: messagebox.showerror("Lỗi", msg)
        self.refresh()

    def print_ticket(self):
        o = self.beer.orders[self.order_id]
        lines = [f"Phiếu Order #{o['id']} - Bàn {self.beer.tables[o['table_id']]['code']}"]
        for it in [x for x in self.beer.order_items if x["order_id"] == self.order_id]:
            lines.append(f"SP {it['product_id']} x {it['qty']} = {(it['unit_price']*it['qty']):.0f}")
        messagebox.showinfo("Phiếu", "\n".join(lines))

    def print_invoice(self):
        o = self.beer.orders[self.order_id]; self.beer.recalc_order(self.order_id)
        lines = [
            f"Hóa đơn #{o['id']} - Bàn {self.beer.tables[o['table_id']]['code']}",
            f"Tạm tính: {o['subtotal']:.0f}",
            f"Tiền giờ: {o['time_charge']:.0f}",
            f"Giảm giá ({o['voucher_code'] or 'auto'}): {o['discount']:.0f}",
            f"Tổng: {o['total']:.0f}",
            f"Thời điểm: {datetime.now()}",
        ]
        messagebox.showinfo("Hóa đơn", "\n".join(lines))

    def pay(self):
        ok, msg = self.beer.pay_order(self.order_id, self.pay_method.get())
        if ok:
            messagebox.showinfo("Thanh toán", msg)
            self.app.show_page("tables")
            self.app.pages["tables"].refresh()
        else:
            messagebox.showerror("Lỗi", msg)
# ==============================
# Trang hồ sơ bàn & nghiệp vụ
# ==============================
class TablesPage(ttk.Frame):
    def __init__(self, parent, app, beer: BeerStore):
        super().__init__(parent); self.app = app; self.beer = beer
        # top bar actions
        top = tk.Frame(self, bg=WHITE); top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Hồ sơ bàn", font=FONT_TITLE, fg=PINK_DARK, bg=WHITE).pack(side="left")
        ttk.Button(top, text="Đăng xuất", style="Danger.TButton", command=self.logout).pack(side="right", padx=6)
        ttk.Button(top, text="Đặt bàn trước", style="Pastel.TButton", command=self.reserve_dialog).pack(side="right", padx=6)
        ttk.Button(top, text="Chuyển order", style="Pastel.TButton", command=self.move_dialog).pack(side="right", padx=6)
        ttk.Button(top, text="Ghép order", style="Pastel.TButton", command=self.merge_dialog).pack(side="right", padx=6)
        ttk.Button(top, text="Khóa bàn", style="Pastel.TButton", command=self.lock_dialog).pack(side="right", padx=6)

        self.summary = tk.Label(self, text="", font=FONT_SUBTITLE, fg=GRAY_TEXT, bg=WHITE)
        self.summary.pack(anchor="w", padx=14)

        # grid
        self.grid_frame = tk.Frame(self, bg=WHITE)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    def logout(self):
        self.app.store.logout()
        messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất.")
        self.app.show_page("login")

    def refresh(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        running = self.beer.running_count()
        self.summary.config(text=f"Bàn đang chạy: {running} / Tổng: {len(self.beer.tables)}")
        # Render tables
        cols = 4
        i = 0
        for t in self.beer.tables.values():
            frame = tk.Frame(self.grid_frame, bg=self.beer.table_color(t["status"]), width=160, height=120)
            frame.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
            frame.grid_propagate(False)
            tk.Label(frame, text=t["code"], font=FONT_BUTTON, fg=WHITE, bg=self.beer.table_color(t["status"])).pack(pady=(10,0))
            tk.Label(frame, text=f"{t['area']} • {t['status']}", font=FONT_SUBTITLE, fg=WHITE, bg=self.beer.table_color(t["status"])).pack()
            btn_frame = tk.Frame(frame, bg=self.beer.table_color(t["status"]))
            btn_frame.pack(pady=6)
            if t["current_order_id"]:
                ttk.Button(btn_frame, text="Order", style="Pastel.TButton",
                           command=lambda oid=t["current_order_id"]: self.open_order(oid)).pack(side="left", padx=4)
            elif t["status"] in ("free", "reserved"):
                ttk.Button(btn_frame, text="Check-in", style="Pastel.TButton",
                           command=lambda tid=t["id"]: self.checkin(tid)).pack(side="left", padx=4)
            ttk.Button(btn_frame, text="Chi tiết", style="Pastel.TButton",
                       command=lambda tid=t["id"]: self.table_detail(tid)).pack(side="left", padx=4)
            i += 1

    def checkin(self, table_id):
        # kiểm tra ID bàn trước khi check-in
        if table_id not in self.beer.tables:
            messagebox.showerror("Lỗi", f"Bàn ID {table_id} không tồn tại.")
            return
        ok, res = self.beer.checkin_table(table_id)
        if ok:
            messagebox.showinfo("Check-in", f"Tạo order #{res}")
            self.refresh()
            self.open_order(res)
        else:
            messagebox.showerror("Lỗi", res)

    def table_detail(self, table_id):
        t = self.beer.tables.get(table_id)
        if not t:
            messagebox.showerror("Lỗi", f"Bàn ID {table_id} không tồn tại.")
            return
        msg = f"Bàn {t['code']}\nKhu: {t['area']}\nTrạng thái: {t['status']}\nOrder hiện tại: {t['current_order_id'] or '-'}"
        messagebox.showinfo("Chi tiết bàn", msg)

    def open_order(self, order_id):
        self.app.pages["order"].set_order(order_id)
        self.app.show_page("order")

    # dialogs
    def reserve_dialog(self):
        try:
            table_id = int(simpledialog.askstring("Đặt bàn", "ID bàn:"))
        except:
            return
        name = simpledialog.askstring("Đặt bàn", "Tên khách:")
        phone = simpledialog.askstring("Đặt bàn", "SĐT:")
        start = simpledialog.askstring("Đặt bàn", "Bắt đầu (YYYY-MM-DDTHH:MM):")
        end = simpledialog.askstring("Đặt bàn", "Kết thúc (YYYY-MM-DDTHH:MM):")
        if not (table_id and name and phone and start and end):
            return
        try:
            start_at = datetime.fromisoformat(start); end_at = datetime.fromisoformat(end)
        except:
            messagebox.showerror("Lỗi", "Định dạng thời gian sai."); return
        ok, msg = self.beer.create_reservation(table_id, name, phone, start_at, end_at)
        messagebox.showinfo("Đặt bàn", msg if ok else f"Lỗi: {msg}")
        self.refresh()

    def move_dialog(self):
        try:
            src = int(simpledialog.askstring("Chuyển order", "Bàn nguồn ID:"))
            dst = int(simpledialog.askstring("Chuyển order", "Bàn đích ID:"))
        except:
            return
        ok, msg = self.beer.move_order(src, dst)
        messagebox.showinfo("Chuyển order", msg if ok else f"Lỗi: {msg}")
        self.refresh()

    def merge_dialog(self):
        try:
            a = int(simpledialog.askstring("Ghép order", "Bàn A ID:"))
            b = int(simpledialog.askstring("Ghép order", "Bàn B ID:"))
        except:
            return
        ok, msg = self.beer.merge_order(a, b)
        messagebox.showinfo("Ghép order", msg if ok else f"Lỗi: {msg}")
        self.refresh()

    def lock_dialog(self):
        try:
            tid = int(simpledialog.askstring("Khóa bàn", "ID bàn:"))
        except:
            return
        ok, msg = self.beer.lock_table(tid)
        messagebox.showinfo("Khóa bàn", msg if ok else f"Lỗi: {msg}")
        self.refresh()
# ==============================
# Hệ thống nghiệp vụ quán bia (có lưu file)
# ==============================
class BeerStore:
    def __init__(self, user_store: UserStore, filepath="beerstore.json"):
        self.filepath = filepath
        self.users = user_store

        # Bàn: id -> dict
        self.tables = {}
        # Sản phẩm: id -> dict
        self.products = {}
        # Vouchers: code -> dict
        self.vouchers = {}
        # Price rules (khung giờ)
        self.price_rules = []
        # Orders: id -> dict
        self.orders = {}
        # OrderItems: list
        self.order_items = []
        # Reservations
        self.reservations = []
        # Số tăng id
        self._order_seq = 1

        self._load_or_seed()

    def _seed(self):
        # Tạo 12 bàn
        for i in range(1, 13):
            self.tables[i] = {
                "id": i,
                "code": f"T{i:02d}",
                "area": "Khu A" if i <= 6 else "Khu B",
                "status": "free",
                "current_order_id": None,
            }
        # Sản phẩm
        self.products[1] = {"id":1,"sku":"BEER1","name":"Bia Lager","base_price":20000,"unit":"chai","stock_qty":200}
        self.products[2] = {"id":2,"sku":"SNACK1","name":"Bim bim","base_price":15000,"unit":"bì","stock_qty":120}
        self.products[3] = {"id":3,"sku":"SNACK2","name":"Đậu phộng","base_price":15000,"unit":"dĩa","stock_qty":50}
        self.products[4] = {"id":4,"sku":"DRINK1","name":"Sting","base_price":25000,"unit":"chai","stock_qty":50}
        self.products[5] = {"id":5,"sku":"SNACK3","name":"Khô gà","base_price":35000,"unit":"dĩa","stock_qty":50}
        self.products[6] = {"id":6,"sku":"SNACK4","name":"Khô mực","base_price":150000,"unit":"dĩa","stock_qty":50}
        # Khung giờ: lưu dạng chuỗi HH:MM để serialize
        self.price_rules.append({"name":"Giờ vàng","start":time_to_str(dtime(18,0)),"end":time_to_str(dtime(22,0)),"multiplier":1.5,"fixed":0.0,"weekday":None})
        self.price_rules.append({"name":"Giờ thường","start":time_to_str(dtime(10,0)),"end":time_to_str(dtime(18,0)),"multiplier":1.0,"fixed":0.0,"weekday":None})
        # Voucher
        self.vouchers["HAPPY"] = {"code":"HAPPY","percent":10.0,"amount":0.0,"min_subtotal":50000.0,"active":True,"auto_apply":True}

    def _load_or_seed(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.tables = data.get("tables", {})
                # nếu thiếu hoặc rỗng, seed lại
                if not self.tables or len(self.tables) < 12:
                    self._seed()
                else:
                    self.products = data.get("products", {})
                    self.vouchers = data.get("vouchers", {})
                    self.price_rules = data.get("price_rules", [])
                # Orders: convert datetime back
                self.orders = {}
                for k, o in data.get("orders", {}).items():
                    o["started_at"] = str_to_dt(o.get("started_at"))
                    o["closed_at"] = str_to_dt(o.get("closed_at"))
                    self.orders[int(k)] = o
                self.order_items = data.get("order_items", [])
                # Reservations: convert datetime back
                self.reservations = []
                for r in data.get("reservations", []):
                    r["start_at"] = str_to_dt(r.get("start_at"))
                    r["end_at"] = str_to_dt(r.get("end_at"))
                    self.reservations.append(r)
                self._order_seq = data.get("_order_seq", 1)
            except:
                self._seed()
        else:
            self._seed()
        # đảm bảo có file ngay từ đầu
        self._save()

    def _save(self):
        # Convert datetimes to strings
        orders_dump = {}
        for oid, o in self.orders.items():
            orders_dump[str(oid)] = {
                **o,
                "started_at": dt_to_str(o.get("started_at")),
                "closed_at": dt_to_str(o.get("closed_at")),
            }
        reservations_dump = []
        for r in self.reservations:
            reservations_dump.append({
                **r,
                "start_at": dt_to_str(r.get("start_at")),
                "end_at": dt_to_str(r.get("end_at")),
            })
        data = {
            "tables": self.tables,
            "products": self.products,
            "vouchers": self.vouchers,
            "price_rules": self.price_rules,
            "orders": orders_dump,
            "order_items": self.order_items,
            "reservations": reservations_dump,
            "_order_seq": self._order_seq,
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---- Helpers ----
    def running_count(self):
        return sum(1 for t in self.tables.values() if t["status"] == "running")

    def table_color(self, status):
        return STATUS_COLORS.get(status, STATUS_COLORS["free"])

    def _compute_time_charge(self, started_at, now):
        total = 0.0
        if not started_at:
            return 0.0
        block = timedelta(minutes=15)
        t = started_at
        while t < now:
            t2 = min(t + block, now)
            weekday = t.weekday()
            applied = []
            for r in self.price_rules:
                if r["weekday"] is not None and r["weekday"] != weekday:
                    continue
                st = datetime.combine(t.date(), str_to_time(r["start"]))
                et = datetime.combine(t.date(), str_to_time(r["end"]))
                if st <= t < et:
                    applied.append(r)
            if applied:
                r = sorted(applied, key=lambda x: (x["fixed"] > 0, x["multiplier"]), reverse=True)[0]
                minutes = (t2 - t).total_seconds() / 60.0
                if r["fixed"] > 0:
                    total += r["fixed"] * (minutes / 60.0)
                else:
                    base_per_hour = 10000.0
                    total += base_per_hour * r["multiplier"] * (minutes / 60.0)
            t = t2
        return round(total, 0)

    def _auto_apply_voucher(self, order):
        subtotal = order["subtotal"]
        best_code, best_value = None, 0.0
        for v in self.vouchers.values():
            if not v["active"] or not v["auto_apply"]:
                continue
            if subtotal < v["min_subtotal"]:
                continue
            value = max(subtotal * (v["percent"] / 100.0), v["amount"])
            if value > best_value:
                best_value = value
                best_code = v["code"]
        order["voucher_code"] = best_code
        order["discount"] = round(best_value, 0)

    def recalc_order(self, order_id):
        order = self.orders.get(order_id)
        if not order:
            return
        items = [it for it in self.order_items if it["order_id"] == order_id]
        order["subtotal"] = sum((it["unit_price"] * it["qty"] - it["discount"]) for it in items)
        if order["status"] == "open":
            order["time_charge"] = self._compute_time_charge(order["started_at"], datetime.now())
        self._auto_apply_voucher(order)
        order["total"] = max(0.0, round(order["subtotal"] + order["time_charge"] - order["discount"], 0))

    # ---- Reservations & Check-in ----
    def create_reservation(self, table_id, name, phone, start_at, end_at):
        tbl = self.tables.get(table_id)
        if not tbl:
            return False, "Không tìm thấy bàn."
        if tbl["status"] not in ("free", "reserved"):
            return False, "Bàn không sẵn sàng cho đặt trước."
        self.reservations.append({
            "id": len(self.reservations)+1,
            "table_id": table_id,
            "customer_name": name,
            "customer_phone": phone,
            "start_at": start_at,
            "end_at": end_at,
            "status": "booked",
        })
        tbl["status"] = "reserved"
        self._save()
        return True, "Đặt bàn thành công."

    def checkin_table(self, table_id):
        if table_id not in self.tables:
            return False, f"Không tìm thấy bàn ID {table_id}."
        tbl = self.tables.get(table_id)
        if tbl["status"] not in ("free", "reserved"):
            return False, "Bàn không sẵn sàng để check-in."
        oid = self._order_seq
        self._order_seq += 1
        order = {
            "id": oid,
            "table_id": table_id,
            "status": "open",
            "started_at": datetime.now(),
            "closed_at": None,
            "subtotal": 0.0,
            "time_charge": 0.0,
            "discount": 0.0,
            "total": 0.0,
            "voucher_code": None,
            "customer_username": self.users.current_user, # để tích điểm
        }
        self.orders[oid] = order
        tbl["status"] = "running"
        tbl["current_order_id"] = oid
        self.recalc_order(oid)
        self._save()
        return True, oid
if __name__ == "__main__":
    PastelAuthApp().mainloop()
