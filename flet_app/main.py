import sqlite3
import hashlib
import customtkinter as ctk

# ==========================================
# 1. DATABASE SETUP (SQLite)
# ==========================================
DB_NAME = "casheasy.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            from_curr TEXT,
            to_curr TEXT,
            rate REAL,
            converted_amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not username or not password:
        return False, "Username and password cannot be empty."
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        return True, "Account created successfully! Please log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def save_conversion(user_id, amount, from_curr, to_curr, rate, converted_amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversions (user_id, amount, from_curr, to_curr, rate, converted_amount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, amount, from_curr, to_curr, rate, converted_amount))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, from_curr, to_curr, rate, converted_amount, timestamp 
        FROM conversions WHERE user_id = ? ORDER BY id DESC LIMIT 10
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records


# ==========================================
# 2. DATA & EXCHANGE RATES (All 20 Currencies)
# ==========================================
CURRENCIES = [
    {"name": "United States Dollar", "code": "USD", "symbol": "$"},
    {"name": "Bangladeshi Taka", "code": "BDT", "symbol": "৳"},
    {"name": "Euro", "code": "EUR", "symbol": "€"},
    {"name": "British Pound", "code": "GBP", "symbol": "£"},
    {"name": "Japanese Yen", "code": "JPY", "symbol": "¥"},
    {"name": "Indian Rupee", "code": "INR", "symbol": "₹"},
    {"name": "Pakistani Rupee", "code": "PKR", "symbol": "₨"},
    {"name": "Chinese Yuan", "code": "CNY", "symbol": "元 / ¥"},
    {"name": "Russian Ruble", "code": "RUB", "symbol": "₽"},
    {"name": "Turkish Lira", "code": "TRY", "symbol": "₺"},
    {"name": "South Korean Won", "code": "KRW", "symbol": "₩"},
    {"name": "Thai Baht", "code": "THB", "symbol": "฿"},
    {"name": "Vietnamese Dong", "code": "VND", "symbol": "₫"},
    {"name": "Nigerian Naira", "code": "NGN", "symbol": "₦"},
    {"name": "Brazilian Real", "code": "BRL", "symbol": "R$"},
    {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF"},
    {"name": "Saudi Riyal", "code": "SAR", "symbol": "ر.س"},
    {"name": "United Arab Emirates Dirham", "code": "AED", "symbol": "د.إ"},
    {"name": "South African Rand", "code": "ZAR", "symbol": "R"},
    {"name": "Mexican Peso", "code": "MXN", "symbol": "MX$"}
]

DEFAULT_RATES = {
    ("USD", "USD"): 1.0, ("USD", "BDT"): 117.50, ("USD", "EUR"): 0.92, ("USD", "GBP"): 0.79,
    ("USD", "JPY"): 155.0, ("USD", "INR"): 83.20, ("USD", "PKR"): 278.0, ("USD", "CNY"): 7.25,
    ("USD", "RUB"): 92.0, ("USD", "TRY"): 32.50, ("USD", "KRW"): 1350.0, ("USD", "THB"): 36.70,
    ("USD", "VND"): 25400.0, ("USD", "NGN"): 1450.0, ("USD", "BRL"): 5.20, ("USD", "CHF"): 0.91,
    ("USD", "SAR"): 3.75, ("USD", "AED"): 3.67, ("USD", "ZAR"): 18.50, ("USD", "MXN"): 17.0
}

def get_default_rate(from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0
    rate_from_usd = DEFAULT_RATES.get(("USD", from_curr))
    rate_to_usd = DEFAULT_RATES.get(("USD", to_curr))
    if rate_from_usd and rate_to_usd:
        return rate_to_usd / rate_from_usd
    return 1.0


# ==========================================
# 3. CUSTOMTKINTER APPLICATION
# ==========================================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ExchangeEasyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        init_db()

        self.title("ExchangeEasy - Currency Assistant")
        self.geometry("440x720")
        self.resizable(False, False)

        self.current_user = {"id": None, "username": None}

        # Main container frame
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=15, pady=15)

        self.show_auth_frame()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------------- VIEW 1: AUTHENTICATION ----------------
    def show_auth_frame(self):
        self.clear_container()

        frame = ctk.CTkFrame(self.container, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(frame, text="EXCHANGEEASY", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(40, 5))

        subtitle_label = ctk.CTkLabel(frame, text="Your Smart Currency Assistant", text_color="gray", font=ctk.CTkFont(size=12))
        subtitle_label.pack(pady=(0, 25))

        self.auth_username_input = ctk.CTkEntry(frame, placeholder_text="Username", width=300, height=42)
        self.auth_username_input.pack(pady=10)

        self.auth_password_input = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300, height=42)
        self.auth_password_input.pack(pady=10)

        self.auth_msg_label = ctk.CTkLabel(frame, text="", text_color="red", font=ctk.CTkFont(size=12))
        self.auth_msg_label.pack(pady=5)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        login_btn = ctk.CTkButton(btn_frame, text="Login", width=135, height=38, command=self.handle_login)
        login_btn.pack(side="left", padx=8)

        signup_btn = ctk.CTkButton(btn_frame, text="Sign Up", width=135, height=38, fg_color="transparent", border_width=2, command=self.handle_signup)
        signup_btn.pack(side="left", padx=8)

    def handle_login(self):
        username = self.auth_username_input.get()
        password = self.auth_password_input.get()
        user = authenticate_user(username, password)
        if user:
            self.current_user["id"] = user[0]
            self.current_user["username"] = user[1]
            self.show_converter_frame()
        else:
            self.auth_msg_label.configure(text="Invalid username or password!", text_color="red")

    def handle_signup(self):
        username = self.auth_username_input.get()
        password = self.auth_password_input.get()
        success, msg = register_user(username, password)
        color = "green" if success else "red"
        self.auth_msg_label.configure(text=msg, text_color=color)

    # ---------------- VIEW 2: CONVERTER & HISTORY ----------------
    def show_converter_frame(self):
        self.clear_container()

        frame = ctk.CTkFrame(self.container, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Header Row
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        welcome_label = ctk.CTkLabel(header_frame, text=f"Welcome, {self.current_user['username']}!", font=ctk.CTkFont(size=15, weight="bold"))
        welcome_label.pack(side="left")

        signout_btn = ctk.CTkButton(header_frame, text="Sign Out", width=75, height=28, fg_color="gray", command=self.show_auth_frame)
        signout_btn.pack(side="right")

        # Amount Input
        self.amount_input = ctk.CTkEntry(frame, width=360, height=38, placeholder_text="Amount to Convert")
        self.amount_input.insert(0, "100.0")
        self.amount_input.pack(pady=8)

        # Dropdowns
        currency_strings = [f"{c['name']} ({c['code']}) [{c['symbol']}]" for c in CURRENCIES]
        
        self.from_dropdown = ctk.CTkComboBox(frame, values=currency_strings, width=360, height=38, command=self.update_rates_display)
        self.from_dropdown.set(currency_strings[0])  # USD
        self.from_dropdown.pack(pady=8)

        self.to_dropdown = ctk.CTkComboBox(frame, values=currency_strings, width=360, height=38, command=self.update_rates_display)
        self.to_dropdown.set(currency_strings[2])  # EUR
        self.to_dropdown.pack(pady=8)

        # Rate Mode Segmented Switch
        self.mode_segmented = ctk.CTkSegmentedButton(frame, values=["Default Rate", "Custom Rate"], command=self.on_mode_change, width=360)
        self.mode_segmented.set("Default Rate")
        self.mode_segmented.pack(pady=8)

        self.custom_rate_input = ctk.CTkEntry(frame, width=360, height=38, placeholder_text="Custom Exchange Rate")
        
        self.rate_info_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
        self.rate_info_label.pack(pady=2)

        # Convert Action Button
        convert_btn = ctk.CTkButton(frame, text="Convert & Save Record", width=360, height=40, command=self.calculate_conversion)
        convert_btn.pack(pady=10)

        # Result Display
        self.result_label = ctk.CTkLabel(frame, text="Result: --", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_label.pack(pady=2)

        # History Area
        ctk.CTkLabel(frame, text="Saved Conversion History:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(10, 2))
        
        self.history_scroll = ctk.CTkScrollableFrame(frame, width=350, height=120)
        self.history_scroll.pack(padx=10, pady=(0, 15))

        self.update_rates_display()
        self.refresh_history()

    def get_code_from_string(self, combo_string):
        return combo_string.split("(")[1].split(")")[0]

    def update_rates_display(self, *args):
        if self.mode_segmented.get() == "Default Rate":
            f_code = self.get_code_from_string(self.from_dropdown.get())
            t_code = self.get_code_from_string(self.to_dropdown.get())
            rate = get_default_rate(f_code, t_code)
            self.custom_rate_input.delete(0, "end")
            self.custom_rate_input.insert(0, f"{rate:.4f}")
            self.rate_info_label.configure(text=f"Default Rate applied: 1 {f_code} = {rate:.4f} {t_code}")

    def on_mode_change(self, value):
        if value == "Custom Rate":
            self.custom_rate_input.pack(before=self.rate_info_label, pady=4)
            self.rate_info_label.configure(text="Using user-defined custom exchange rate.")
        else:
            self.custom_rate_input.pack_forget()
            self.update_rates_display()

    def calculate_conversion(self):
        try:
            amount = float(self.amount_input.get())
            rate = float(self.custom_rate_input.get())
            f_code = self.get_code_from_string(self.from_dropdown.get())
            t_code = self.get_code_from_string(self.to_dropdown.get())
            target_symbol = next((c["symbol"] for c in CURRENCIES if c["code"] == t_code), "")

            converted_val = amount * rate
            self.result_label.configure(text=f"Result: {target_symbol} {converted_val:,.2f} {t_code}")

            if self.current_user["id"]:
                save_conversion(self.current_user["id"], amount, f_code, t_code, rate, converted_val)
                self.refresh_history()
        except ValueError:
            self.result_label.configure(text="Please enter valid numeric values!")

    def refresh_history(self):
        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        if self.current_user["id"]:
            records = get_user_history(self.current_user["id"])
            if not records:
                ctk.CTkLabel(self.history_scroll, text="No conversion history recorded yet.", font=ctk.CTkFont(size=11, slant="italic")).pack(anchor="w", padx=5, pady=2)
            for rec in records:
                amt, f_curr, t_curr, r, conv_amt, ts = rec
                item_text = f"{amt} {f_curr} → {conv_amt:,.2f} {t_curr} (Rate: {r:.4f})"
                lbl = ctk.CTkLabel(self.history_scroll, text=item_text, font=ctk.CTkFont(size=11), fg_color=("gray85", "gray20"), corner_radius=6, anchor="w")
                lbl.pack(fill="x", padx=2, pady=2)


if __name__ == "__main__":
    app = ExchangeEasyApp()
    app.mainloop()