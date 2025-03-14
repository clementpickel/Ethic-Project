import tkinter as tk
from UI.MenuGUI import MenuGUI

def main():
    root = tk.Tk()
    root.title("Gomoku Game")
    # gui = GomokuGUI(root, game)
    gui = MenuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
