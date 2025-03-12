import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime, timedelta
import csv
import tkinter.font as tkfont
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os

LANGUAGES = {
    "English": {
        "title": "Emergency Resource Manager Pro",
        "login": "Login",
        "register": "Register",
        "username": "Username:",
        "password": "Password:",
        "name": "Resource Name:",
        "quantity": "Quantity:",
        "unit": "Unit:",
        "category": "Category:",
        "expiry": "Expiry (YYYY-MM-DD):",
        "add": "Add Resource",
        "delete": "Delete Resource",
        "export": "Export to CSV",
        "filter": "Filter by Category:",
        "adjust": "Adjust Quantity",
        "forecast": "Forecast Consumption",
        "location": "Storage Location:",
        "alert": "All resources are under control.",
        "updated": "Last Updated: N/A",
        "search": "Search Resources:",
        "graph": "Show Resource Graph",
        "settings": "Settings",
        "logout": "Logout",
        "log": "Activity Log",
        "error_fill": "Please fill in all required fields!",
        "error_format": "Quantity must be a number and expiry must be in YYYY-MM-DD format!",
        "error_select": "Please select a resource!",
        "success_export": "Resources exported to 'emergency_resources_export.csv'!",
        "login_error": "Invalid username or password!",
        "register_success": "User registered successfully!",
        "register_error": "Username already exists!",
    },
    "Persian": {
        "title": "مدیریت حرفه‌ای منابع اضطراری",
        "login": "ورود",
        "register": "ثبت‌نام",
        "username": "نام کاربری:",
        "password": "رمز عبور:",
        "name": "نام منبع:",
        "quantity": "مقدار:",
        "unit": "واحد:",
        "category": "دسته‌بندی:",
        "expiry": "تاریخ انقضا (YYYY-MM-DD):",
        "add": "اضافه کردن منبع",
        "delete": "حذف منبع",
        "export": "خروجی به CSV",
        "filter": "فیلتر بر اساس دسته‌بندی:",
        "adjust": "تنظیم مقدار",
        "forecast": "پیش‌بینی مصرف",
        "location": "محل ذخیره:",
        "alert": "همه منابع تحت کنترل هستند.",
        "updated": "آخرین به‌روزرسانی: نامشخص",
        "search": "جست‌وجوی منابع:",
        "graph": "نمایش نمودار منابع",
        "settings": "تنظیمات",
        "logout": "خروج",
        "log": "لاگ فعالیت‌ها",
        "error_fill": "لطفاً همه فیلدها را پر کنید!",
        "error_format": "مقدار باید عددی و تاریخ به فرمت YYYY-MM-DD باشد!",
        "error_select": "لطفاً یک منبع انتخاب کنید!",
        "success_export": "منابع به 'emergency_resources_export.csv' خروجی شدند!",
        "login_error": "نام کاربری یا رمز عبور اشتباه است!",
        "register_success": "کاربر با موفقیت ثبت شد!",
        "register_error": "نام کاربری قبلاً وجود دارد!",
    }
}

resources = {}
users = {}
current_user = None
current_language = "English"
current_theme = "Dark"
settings = {"accent_color": "#A93226", "font_size": 12}

def save_resources():
    with open(f"resources_{current_user}.json", "w") as file:
        json.dump(resources, file)

def load_resources():
    try:
        with open(f"resources_{current_user}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"items": [], "last_updated": str(datetime.now().date())}

def save_users():
    with open("users.json", "w") as file:
        json.dump(users, file)

def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_settings():
    with open(f"settings_{current_user}.json", "w") as file:
        json.dump(settings, file)

def load_settings():
    try:
        with open(f"settings_{current_user}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"accent_color": "#A93226", "font_size": 12}

def log_activity(activity):
    with open(f"activity_log_{current_user}.txt", "a") as file:
        file.write(f"{datetime.now()}: {activity}\n")

def show_login_screen():
    global login_frame
    login_frame = tk.Frame(root, bg="#2E2E2E")
    login_frame.pack(fill="both", expand=True)

    tk.Label(login_frame, text="Emergency Resource Manager Pro", font=("Helvetica", 20, "bold"), bg="#2E2E2E", fg="white").pack(pady=20)
    tk.Label(login_frame, text=LANGUAGES[current_language]["username"], bg="#2E2E2E", fg="white").pack(pady=5)
    entry_username = tk.Entry(login_frame, width=20, font=("Helvetica", 12))
    entry_username.pack(pady=5)
    tk.Label(login_frame, text=LANGUAGES[current_language]["password"], bg="#2E2E2E", fg="white").pack(pady=5)
    entry_password = tk.Entry(login_frame, width=20, show="*", font=("Helvetica", 12))
    entry_password.pack(pady=5)

    def login():
        global current_user
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        if username in users and users[username] == password:
            current_user = username
            resources.clear()
            resources.update(load_resources())
            settings.update(load_settings())
            login_frame.destroy()
            show_main_screen()
        else:
            messagebox.showerror("Error", LANGUAGES[current_language]["login_error"])

    def register():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Error", LANGUAGES[current_language]["error_fill"])
            return
        if username in users:
            messagebox.showerror("Error", LANGUAGES[current_language]["register_error"])
        else:
            users[username] = password
            save_users()
            messagebox.showinfo("Success", LANGUAGES[current_language]["register_success"])

    tk.Button(login_frame, text=LANGUAGES[current_language]["login"], command=login, bg="#A93226", fg="white", font=("Helvetica", 12)).pack(pady=10)
    tk.Button(login_frame, text=LANGUAGES[current_language]["register"], command=register, bg="#A93226", fg="white", font=("Helvetica", 12)).pack(pady=5)

def change_language(event):
    global current_language
    current_language = combo_language.get()
    update_ui_texts()

def toggle_theme():
    global current_theme
    current_theme = "Light" if current_theme == "Dark" else "Dark"
    update_theme()

def update_ui_texts():
    lang = LANGUAGES[current_language]
    root.title(f"{lang['title']} - {current_user}")
    lbl_name.config(text=lang["name"])
    lbl_quantity.config(text=lang["quantity"])
    lbl_unit.config(text=lang["unit"])
    lbl_category.config(text=lang["category"])
    lbl_expiry.config(text=lang["expiry"])
    btn_add.config(text=f"➕ {lang['add']}")
    btn_delete.config(text=f"🗑️ {lang['delete']}")
    btn_export.config(text=f"📤 {lang['export']}")
    btn_adjust.config(text=f"⚙️ {lang['adjust']}")
    btn_forecast.config(text=f"📅 {lang['forecast']}")
    btn_graph.config(text=f"📊 {lang['graph']}")
    btn_settings.config(text=f"⚙️ {lang['settings']}")
    btn_logout.config(text=f"🚪 {lang['logout']}")
    btn_log.config(text=f"📜 {lang['log']}")
    lbl_filter.config(text=lang["filter"])
    lbl_location.config(text=lang["location"])
    lbl_search.config(text=lang["search"])
    lbl_alert.config(text=lang["alert"])
    lbl_last_updated.config(text=lang["updated"])
    update_resource_list()

def update_theme():
    bg_color = "#2E2E2E" if current_theme == "Dark" else "#F5F5F5"
    fg_color = "white" if current_theme == "Dark" else "black"
    accent_color = settings["accent_color"]
    entry_bg = "#3C3C3C" if current_theme == "Dark" else "#E0E0E0"

    root.config(bg=bg_color)
    header_frame.config(bg=accent_color)
    input_frame.config(bg=bg_color)
    filter_frame.config(bg=bg_color)
    tree_frame.config(bg=bg_color)
    bottom_frame.config(bg=bg_color)

    for widget in [lbl_name, lbl_quantity, lbl_unit, lbl_category, lbl_expiry, lbl_filter, lbl_location, lbl_search, lbl_alert, lbl_last_updated]:
        widget.config(bg=bg_color, fg=fg_color)

    for entry in [entry_name, entry_quantity, entry_expiry, entry_location, entry_search]:
        entry.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)

    for btn in [btn_add, btn_delete, btn_export, btn_adjust, btn_forecast, btn_graph, btn_settings, btn_logout, btn_log]:
        btn.config(bg=accent_color, fg="white")

    style.configure("Treeview", background=entry_bg, foreground=fg_color, fieldbackground=entry_bg)
    style.configure("Treeview.Heading", background=accent_color, foreground="white")
    style.configure("TCombobox", fieldbackground=entry_bg, background=accent_color, foreground=fg_color)

def add_resource():
    name = entry_name.get().strip()
    quantity = entry_quantity.get().strip()
    unit = combo_unit.get()
    category = combo_category.get()
    expiry = entry_expiry.get().strip()
    location = entry_location.get().strip() or "Unknown"

    if not all([name, quantity, expiry]):
        messagebox.showwarning("Error", LANGUAGES[current_language]["error_fill"])
        return

    try:
        quantity = float(quantity)
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        resource = {
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "category": category,
            "expiry": expiry,
            "location": location,
            "added_date": str(datetime.now().date())
        }
        resources["items"].append(resource)
        resources["last_updated"] = str(datetime.now().date())
        update_resource_list()
        save_resources()
        log_activity(f"Added resource: {name}")
        clear_inputs()
    except ValueError:
        messagebox.showerror("Error", LANGUAGES[current_language]["error_format"])

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    combo_unit.set("Units")
    combo_category.set("General")
    entry_expiry.delete(0, tk.END)
    entry_location.delete(0, tk.END)

def update_resource_list(filter_category="All", search_query=""):
    for item in tree.get_children():
        tree.delete(item)
    for res in resources["items"]:
        if (filter_category == "All" or res["category"] == filter_category) and (search_query.lower() in res["name"].lower() or not search_query):
            expiry_date = datetime.strptime(res["expiry"], "%Y-%m-%d").date()
            days_left = (expiry_date - datetime.now().date()).days
            status = "Critical" if days_left <= 7 else "Available"
            location = res.get("location", "Unknown")
            tree.insert("", tk.END, values=(res["name"], res["category"], f"{res['quantity']} {res['unit']}", res["expiry"], days_left, location, status))
    check_alerts()
    lbl_last_updated.config(text=f"{LANGUAGES[current_language]['updated'].split(':')[0]}: {resources['last_updated']}")

def search_resources(event):
    query = entry_search.get().strip()
    update_resource_list(combo_filter.get(), query)

def check_alerts():
    alerts = []
    for res in resources["items"]:
        expiry_date = datetime.strptime(res["expiry"], "%Y-%m-%d").date()
        days_left = (expiry_date - datetime.now().date()).days
        if days_left <= 7:
            alerts.append(f"Alert: {res['name']} expires in {days_left} days!")
        if res["quantity"] < 5:
            alerts.append(f"Alert: {res['name']} quantity below 5 {res['unit']}!")
    lbl_alert.config(text="\n".join(alerts) if alerts else LANGUAGES[current_language]["alert"])
    if alerts:
        threading.Thread(target=show_reminder, args=(alerts,), daemon=True).start()

def show_reminder(alerts):
    time.sleep(5)  
    messagebox.showwarning("Reminder", "\n".join(alerts))

def delete_resource():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", LANGUAGES[current_language]["error_select"])
        return
    res_index = tree.index(selected[0])
    resource_name = resources["items"][res_index]["name"]
    del resources["items"][res_index]
    update_resource_list(combo_filter.get(), entry_search.get().strip())
    save_resources()
    log_activity(f"Deleted resource: {resource_name}")

def adjust_quantity():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", LANGUAGES[current_language]["error_select"])
        return
    res_index = tree.index(selected[0])
    adjust_window = tk.Toplevel(root)
    adjust_window.title("Adjust Quantity")
    adjust_window.geometry("300x150")
    adjust_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    tk.Label(adjust_window, text="Enter change (±):", bg=adjust_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=10)
    entry_adjust = tk.Entry(adjust_window, width=10)
    entry_adjust.pack(pady=5)

    def apply_adjustment():
        try:
            change = float(entry_adjust.get())
            resources["items"][res_index]["quantity"] += change
            if resources["items"][res_index]["quantity"] < 0:
                resources["items"][res_index]["quantity"] = 0
            update_resource_list(combo_filter.get(), entry_search.get().strip())
            save_resources()
            log_activity(f"Adjusted quantity of {resources['items'][res_index]['name']} by {change}")
            adjust_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    tk.Button(adjust_window, text="Apply", command=apply_adjustment, bg=settings["accent_color"], fg="white").pack(pady=10)

def forecast_consumption():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", LANGUAGES[current_language]["error_select"])
        return
    res_index = tree.index(selected[0])
    forecast_window = tk.Toplevel(root)
    forecast_window.title("Consumption Forecast")
    forecast_window.geometry("400x200")
    forecast_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    tk.Label(forecast_window, text="Daily Consumption Rate:", bg=forecast_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=10)
    entry_rate = tk.Entry(forecast_window, width=10)
    entry_rate.pack(pady=5)

    def calculate_forecast():
        try:
            rate = float(entry_rate.get())
            quantity = resources["items"][res_index]["quantity"]
            days_left = int(quantity / rate)
            messagebox.showinfo("Forecast", f"{resources['items'][res_index]['name']} will last approximately {days_left} days.")
            forecast_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    tk.Button(forecast_window, text="Calculate", command=calculate_forecast, bg=settings["accent_color"], fg="white").pack(pady=10)

def show_resource_graph():
    graph_window = tk.Toplevel(root)
    graph_window.title("Resource Quantity Graph")
    graph_window.geometry("600x400")
    graph_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    names = [res["name"] for res in resources["items"]]
    quantities = [res["quantity"] for res in resources["items"]]

    fig, ax = plt.subplots()
    ax.bar(names, quantities, color=settings["accent_color"])
    ax.set_title("Resource Quantities", color="white" if current_theme == "Dark" else "black")
    ax.set_ylabel("Quantity", color="white" if current_theme == "Dark" else "black")
    ax.tick_params(axis="x", rotation=45, colors="white" if current_theme == "Dark" else "black")
    ax.tick_params(axis="y", colors="white" if current_theme == "Dark" else "black")
    ax.set_facecolor("#3C3C3C" if current_theme == "Dark" else "#E0E0E0")
    fig.set_facecolor("#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    tk.Label(settings_window, text="Accent Color:", bg=settings_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=10)
    entry_color = tk.Entry(settings_window, width=10)
    entry_color.insert(0, settings["accent_color"])
    entry_color.pack(pady=5)

    tk.Label(settings_window, text="Font Size:", bg=settings_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=10)
    entry_font_size = tk.Entry(settings_window, width=10)
    entry_font_size.insert(0, settings["font_size"])
    entry_font_size.pack(pady=5)

    def apply_settings():
        settings["accent_color"] = entry_color.get().strip()
        try:
            settings["font_size"] = int(entry_font_size.get())
            header_font.configure(size=settings["font_size"] + 2)
            text_font.configure(size=settings["font_size"])
            update_theme()
            save_settings()
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Font size must be a number!")

    tk.Button(settings_window, text="Apply", command=apply_settings, bg=settings["accent_color"], fg="white").pack(pady=10)

def show_activity_log():
    log_window = tk.Toplevel(root)
    log_window.title("Activity Log")
    log_window.geometry("500x400")
    log_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    log_text = scrolledtext.ScrolledText(log_window, width=60, height=20, bg="#3C3C3C" if current_theme == "Dark" else "#E0E0E0", fg="white" if current_theme == "Dark" else "black")
    log_text.pack(pady=10, padx=10)

    try:
        with open(f"activity_log_{current_user}.txt", "r") as file:
            log_text.insert(tk.END, file.read())
    except FileNotFoundError:
        log_text.insert(tk.END, "No activities logged yet.")

def logout():
    global current_user
    save_resources()
    save_settings()
    current_user = None
    for widget in root.winfo_children():
        widget.destroy()
    show_login_screen()

def export_to_csv():
    with open(f"emergency_resources_export_{current_user}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Category", "Quantity", "Unit", "Expiry", "Location", "Days Left", "Status"])
        for res in resources["items"]:
            expiry_date = datetime.strptime(res["expiry"], "%Y-%m-%d").date()
            days_left = (expiry_date - datetime.now().date()).days
            status = "Critical" if days_left <= 7 else "Available"
            location = res.get("location", "Unknown")
            writer.writerow([res["name"], res["category"], res["quantity"], res["unit"], res["expiry"], location, days_left, status])
    messagebox.showinfo("Success", LANGUAGES[current_language]["success_export"])

def show_calendar():
    cal_window = tk.Toplevel(root)
    cal_window.title("Select Expiry Date")
    cal_window.geometry("300x300")
    cal_window.config(bg="#2E2E2E" if current_theme == "Dark" else "#F5F5F5")

    def set_date(day):
        selected_date = f"{year_var.get()}-{month_var.get():02d}-{day:02d}"
        entry_expiry.delete(0, tk.END)
        entry_expiry.insert(0, selected_date)
        cal_window.destroy()

    year_var = tk.IntVar(value=datetime.now().year)
    month_var = tk.IntVar(value=datetime.now().month)

    tk.Label(cal_window, text="Year:", bg=cal_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=5)
    tk.Entry(cal_window, textvariable=year_var, width=6).pack(pady=5)
    tk.Label(cal_window, text="Month:", bg=cal_window["bg"], fg="white" if current_theme == "Dark" else "black").pack(pady=5)
    tk.Entry(cal_window, textvariable=month_var, width=6).pack(pady=5)

    def draw_calendar():
        for widget in cal_frame.winfo_children():
            widget.destroy()
        year = year_var.get()
        month = month_var.get()
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
        first_day = datetime(year, month, 1).weekday()
        for i in range(42):
            if i < first_day or i >= first_day + days_in_month:
                tk.Button(cal_frame, text="", width=2, bg=cal_frame["bg"]).grid(row=i // 7, column=i % 7)
            else:
                day = i - first_day + 1
                tk.Button(cal_frame, text=day, width=2, command=lambda d=day: set_date(d), bg=settings["accent_color"], fg="white").grid(row=i // 7, column=i % 7)

    cal_frame = tk.Frame(cal_window, bg=cal_window["bg"])
    cal_frame.pack(pady=10)
    tk.Button(cal_window, text="Show Calendar", command=draw_calendar, bg=settings["accent_color"], fg="white").pack(pady=5)
    draw_calendar()

def show_main_screen():
    global header_frame, input_frame, filter_frame, tree_frame, bottom_frame
    global lbl_name, lbl_quantity, lbl_unit, lbl_category, lbl_expiry, lbl_filter, lbl_location, lbl_search, lbl_alert, lbl_last_updated
    global entry_name, entry_quantity, entry_expiry, entry_location, entry_search
    global combo_unit, combo_category, combo_filter, combo_language
    global btn_add, btn_delete, btn_export, btn_adjust, btn_forecast, btn_graph, btn_settings, btn_logout, btn_log
    global tree, style, header_font, text_font

    header_font = tkfont.Font(family="Helvetica", size=settings["font_size"] + 2, weight="bold")
    text_font = tkfont.Font(family="Helvetica", size=settings["font_size"])

    style = ttk.Style()
    style.theme_use("clam")

    header_frame = tk.Frame(root, bg=settings["accent_color"])
    header_frame.pack(fill="x")
    tk.Label(header_frame, text=LANGUAGES[current_language]["title"], font=header_font, bg=settings["accent_color"], fg="white").pack(side=tk.LEFT, padx=10, pady=5)
    btn_logout = tk.Button(header_frame, text=f"🚪 {LANGUAGES[current_language]['logout']}", command=logout, font=text_font, relief="raised")
    btn_logout.pack(side=tk.RIGHT, padx=10, pady=5)
    btn_settings = tk.Button(header_frame, text=f"⚙️ {LANGUAGES[current_language]['settings']}", command=show_settings, font=text_font, relief="raised")
    btn_settings.pack(side=tk.RIGHT, padx=10, pady=5)

    input_frame = tk.Frame(root, bg="#2E2E2E", bd=2, relief="groove")
    input_frame.pack(pady=20, padx=20, fill="x")

    lbl_name = tk.Label(input_frame, text="Resource Name:", font=text_font)
    lbl_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_name = tk.Entry(input_frame, width=25, font=text_font)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    lbl_quantity = tk.Label(input_frame, text="Quantity:", font=text_font)
    lbl_quantity.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    entry_quantity = tk.Entry(input_frame, width=10, font=text_font)
    entry_quantity.grid(row=0, column=3, padx=10, pady=5)

    lbl_unit = tk.Label(input_frame, text="Unit:", font=text_font)
    lbl_unit.grid(row=0, column=4, padx=10, pady=5, sticky="e")
    combo_unit = ttk.Combobox(input_frame, values=["Units", "Liters", "Kilograms"], width=12, state="readonly", font=text_font)
    combo_unit.set("Units")
    combo_unit.grid(row=0, column=5, padx=10, pady=5)

    lbl_category = tk.Label(input_frame, text="Category:", font=text_font)
    lbl_category.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_category = ttk.Combobox(input_frame, values=["General", "Food", "Water", "Medical"], width=15, state="readonly", font=text_font)
    combo_category.set("General")
    combo_category.grid(row=1, column=1, padx=10, pady=5)

    lbl_expiry = tk.Label(input_frame, text="Expiry (YYYY-MM-DD):", font=text_font)
    lbl_expiry.grid(row=1, column=2, padx=10, pady=5, sticky="e")
    entry_expiry = tk.Entry(input_frame, width=15, font=text_font)
    entry_expiry.grid(row=1, column=3, padx=10, pady=5)
    tk.Button(input_frame, text="📅", command=show_calendar, bg=settings["accent_color"], fg="white").grid(row=1, column=4, padx=5, pady=5)

    lbl_location = tk.Label(input_frame, text="Storage Location:", font=text_font)
    lbl_location.grid(row=1, column=4, padx=10, pady=5, sticky="e")
    entry_location = tk.Entry(input_frame, width=15, font=text_font)
    entry_location.grid(row=1, column=5, padx=10, pady=5)

    btn_add = tk.Button(input_frame, text="➕ Add Resource", command=add_resource, font=header_font, relief="raised")
    btn_add.grid(row=2, column=2, columnspan=2, pady=10)

    filter_frame = tk.Frame(root, bg="#2E2E2E")
    filter_frame.pack(pady=10, padx=20, fill="x")

    lbl_filter = tk.Label(filter_frame, text="Filter by Category:", font=text_font)
    lbl_filter.pack(side=tk.LEFT, padx=5)
    combo_filter = ttk.Combobox(filter_frame, values=["All", "General", "Food", "Water", "Medical"], width=15, state="readonly", font=text_font)
    combo_filter.set("All")
    combo_filter.pack(side=tk.LEFT, padx=5)
    combo_filter.bind("<<ComboboxSelected>>", lambda e: update_resource_list(combo_filter.get(), entry_search.get().strip()))

    lbl_search = tk.Label(filter_frame, text="Search Resources:", font=text_font)
    lbl_search.pack(side=tk.LEFT, padx=20)
    entry_search = tk.Entry(filter_frame, width=20, font=text_font)
    entry_search.pack(side=tk.LEFT, padx=5)
    entry_search.bind("<KeyRelease>", search_resources)

    tk.Label(filter_frame, text="Language:", bg="#2E2E2E", fg="white", font=text_font).pack(side=tk.LEFT, padx=20)
    combo_language = ttk.Combobox(filter_frame, values=["English", "Persian"], width=10, state="readonly", font=text_font)
    combo_language.set("English")
    combo_language.pack(side=tk.LEFT, padx=5)
    combo_language.bind("<<ComboboxSelected>>", change_language)

    tk.Button(filter_frame, text="🌙 Toggle Theme", command=toggle_theme, bg=settings["accent_color"], fg="white", font=text_font).pack(side=tk.RIGHT, padx=10)

    tree_frame = tk.Frame(root, bg="#2E2E2E")
    tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

    columns = ("name", "category", "quantity", "expiry", "days_left", "location", "status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    tree.heading("name", text="Resource Name")
    tree.heading("category", text="Category")
    tree.heading("quantity", text="Quantity")
    tree.heading("expiry", text="Expiry Date")
    tree.heading("days_left", text="Days Left")
    tree.heading("location", text="Location")
    tree.heading("status", text="Status")
    tree.column("name", width=200)
    tree.column("category", width=120)
    tree.column("quantity", width=100)
    tree.column("expiry", width=120)
    tree.column("days_left", width=100)
    tree.column("location", width=150)
    tree.column("status", width=100)
    tree.pack(side=tk.LEFT, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    bottom_frame = tk.Frame(root, bg="#2E2E2E")
    bottom_frame.pack(pady=20, padx=20, fill="x")

    btn_delete = tk.Button(bottom_frame, text="🗑️ Delete Resource", command=delete_resource, font=header_font, relief="raised")
    btn_delete.pack(side=tk.LEFT, padx=10)

    btn_export = tk.Button(bottom_frame, text="📤 Export to CSV", command=export_to_csv, font=header_font, relief="raised")
    btn_export.pack(side=tk.LEFT, padx=10)

    btn_adjust = tk.Button(bottom_frame, text="⚙️ Adjust Quantity", command=adjust_quantity, font=header_font, relief="raised")
    btn_adjust.pack(side=tk.LEFT, padx=10)

    btn_forecast = tk.Button(bottom_frame, text="📅 Forecast Consumption", command=forecast_consumption, font=header_font, relief="raised")
    btn_forecast.pack(side=tk.LEFT, padx=10)

    btn_graph = tk.Button(bottom_frame, text="📊 Show Resource Graph", command=show_resource_graph, font=header_font, relief="raised")
    btn_graph.pack(side=tk.LEFT, padx=10)

    btn_log = tk.Button(bottom_frame, text="📜 Activity Log", command=show_activity_log, font=header_font, relief="raised")
    btn_log.pack(side=tk.LEFT, padx=10)

    lbl_alert = tk.Label(bottom_frame, text="All resources are under control.", font=text_font, fg="#E74C3C", justify="left", wraplength=600)
    lbl_alert.pack(side=tk.LEFT, padx=10)

    lbl_last_updated = tk.Label(bottom_frame, text="Last Updated: N/A", font=("Helvetica", 10, "italic"))
    lbl_last_updated.pack(side=tk.RIGHT, padx=10)

    update_theme()
    update_resource_list()

root = tk.Tk()
root.geometry("1200x900")
users = load_users()
show_login_screen()
root.mainloop()