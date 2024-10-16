from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Edwar0x\Pictures\47\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_gui(window):
    window.geometry("996x74")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=74,
        width=996,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        409.90345352075946,
        37.11239555126697,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#505050",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=25.946341148345084,
        y=15.381969451904297,
        width=767.9142247448287,
        height=41.46085219872535
    )

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=814.4543002316962,
        y=12.64764404296875,
        width=168.0873309866363,
        height=48.194292687160996
    )

# Nếu file này được chạy độc lập, khởi tạo GUI trong cửa sổ chính
if __name__ == '__main__':
    window = Tk()
    create_gui(window)
    window.resizable(False, False)
    window.mainloop()

# Nếu file này được gọi từ một module khác, khởi tạo GUI trong cửa sổ đã được truyền vào
if 'window' in globals():
    create_gui(window)
