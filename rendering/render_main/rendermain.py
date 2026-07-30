import customtkinter as ctk
import os

from tkinter import messagebox


BG           = "#0F172A"
PANEL        = "#1E293B"
PANEL_ROW    = "#273549"
ACCENT       = "#3B82F6"
ACCENT_HOVER = "#2563EB"
TEXT         = "#F8FAFC"
TEXT_MUTED   = "#64748B"
FONT         = "Ubuntu"




class RenderMain:
    def __init__(self, app):
        self.app = app
        self.root = ctk.CTk()

    def unRender(self):
        for widget in self.root.winfo_children(): 
            widget.destroy()

    def render(self):
        self.unRender()
        self.root.title("MyMaze - Main")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(fg_color=BG)

        frameSize = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=12)
        frameSize.place(relwidth=0.16, relheight=0.85, x=10, y=10, anchor="nw")

        self.root.size = ctk.CTkEntry(
            frameSize,
            placeholder_text="Width",
            width=120, height=40,
            font=(FONT, 13),
            corner_radius=6,
        )
        self.root.size.pack(padx=12, pady=(15, 8))



        ctk.CTkButton(
            frameSize,
            text="Create",
            width=120,
            height=40,
            command=self.create_maze
        ).pack(padx=12, pady=(20, 10))

        
        frameMazeList = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=12)
        frameMazeList.place(
            relx=1.0, relwidth=0.45, relheight=0.9,
            x=-10, y=10, anchor="ne"
        )

        ctk.CTkLabel(
            frameMazeList,
            text="Saved mazes",
            font=(FONT, 13),
            text_color=TEXT_MUTED,
        ).pack(pady=(12, 4))

        self.fieldList(frameMazeList)

        ctk.CTkButton(
            self.root,
            text="Theme",
            width=60, height=40,
            font=(FONT, 13),
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=TEXT,
            command=self.toggleTheme,
        ).place(x=15, rely=1.0, anchor="sw", y=-10)

    def fieldList(self, frame):
        maze_dir = "./dataSorce/save_mazes"
        files = []
        if os.path.exists(maze_dir):
            files = sorted(
                f for f in os.listdir(maze_dir) if f.endswith(".txt")
            )

        if not files:
            ctk.CTkLabel(
                frame,
                text="No mazes found",
                font=(FONT, 12),
                text_color=TEXT_MUTED,
            ).pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(frame, fg_color=PANEL, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        for fname in files:
            row = ctk.CTkFrame(scroll, fg_color=PANEL_ROW, corner_radius=8)
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(
                row,
                text=fname.replace(".maze", ""),
                font=(FONT, 12),
                text_color=TEXT,
                anchor="w",
            ).pack(side="left", padx=12, pady=8)

            ctk.CTkButton(
                row,
                text="Open",
                width=65, height=30,
                font=(FONT, 12),
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                corner_radius=6,
                command=lambda f=fname: self.openMaze(f)
            ).pack(side="right", padx=8, pady=8)

    def openMaze(self, filename):
        self.app.loadMaze(
            filename,
        )
    def toggleTheme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "Dark" else "dark")

    def create_maze(self):
        v = self.root.size.get().strip()

        if not v:
            return self.show_error("Enter maze size")
        if not v.isdigit():
            return self.show_error("Only numbers allowed")

        size = int(v)

        if not (1 <= size <= 50):
            return self.show_error("Size must be 1–50")

        self.app.showMaze(size)


    def show_error(self, text):
        e = ctk.CTkToplevel(self.root)
        e.title("Error")
        e.geometry("360x170")
        e.resizable(False, False)
        e.configure(fg_color="#0B1220")

        e.transient(self.root)

        e.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 180
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 85
        e.geometry(f"+{x}+{y}")

        f = ctk.CTkFrame(
            e,
            fg_color=PANEL,
            corner_radius=12,
            border_width=1,
            border_color=ACCENT
        )
        f.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            f,
            text="⚠ Error",
            font=(FONT, 18, "bold"),
            text_color=ACCENT,
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            f,
            text=text,
            font=(FONT, 13),
            text_color=TEXT,
            wraplength=300,
            justify="center",
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            f,
            text="OK",
            width=120,
            height=35,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=TEXT,
            corner_radius=8,
            command=e.destroy,
        ).pack(pady=(0, 10))

        e.after(10, lambda: e.grab_set())