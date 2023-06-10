import csv
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = []

        self.title("CAADI")
        self.geometry("650x500")

        self.main_panel = ttk.PanedWindow(orient="vertical")
        self.horiz_panel = ttk.PanedWindow(orient="horizontal")

        self.header_frame = tk.Frame(self.main_panel,bg="#1A1713",borderwidth=0)
        self.image1_path = "escudo_ug.png"  
        self.image1 = Image.open(self.image1_path)
        self.image1 = self.image1.resize((70, 80))  
        self.photo1 = ImageTk.PhotoImage(self.image1)
        self.main_panel.add(self.header_frame)
        self.image1_label = tk.Label(self.header_frame, image=self.photo1)
        self.image1_label.pack(side="top",padx=10)

        self.side_frame = tk.Frame(self.horiz_panel,bg="#DBD0C5")
        self.bUpload = tk.Button(self.side_frame, text="Subir archivo", fg="white",bg="#C39A7A",border="0",padx="41",pady="10",command=self.open_file)
        self.bUpload.pack(side="top")
        self.lFilter = tk.Label(self.side_frame,text="Filtro: ", bg="#DBD0C5", pady=10,)
        self.lFilter.pack()
        self.filterText = tk.StringVar()
        self.eFilter = tk.Entry(self.side_frame, textvariable=self.filterText)
        self.eFilter.pack()
        self.space = tk.Label(self.side_frame, bg="#DBD0C5",pady="5")
        self.space.pack()
        self.bFilter = tk.Button(self.side_frame,text="Aplicar filtro",fg="white",bg="#B8926A",border="0",padx="43",pady="10",command=self.apply_filter)
        self.bFilter.pack()
        self.bLimpiar = tk.Button(self.side_frame,text="Limpiar filtro",fg="white",bg="#854621",border="0",padx="41",pady="10",command=self.wipe_filter)
        self.bLimpiar.pack()
        self.bExit = tk.Button(self.side_frame, text="SALIR", fg="white", bg="#423025",border="0",padx="60",pady="10",command=exit)
        self.bExit.pack(side="bottom")
        self.horiz_panel.add(self.side_frame)

        self.main_frame = tk.Frame(self.horiz_panel)
        self.main_canvas = tk.Canvas(self.main_frame)
        self.table = tk.Frame(self.main_canvas, bg="#F2F3EC")
        self.scrollbar = tk.Scrollbar(self.main_canvas,orient="vertical",command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_canvas.pack(fill="both", expand=True)
        self.scrollbar.pack(side="right",fill="y")

        self.bind("<Return>", self.apply_filter)

        self.horiz_panel.add(self.main_frame)
        self.main_panel.add(self.horiz_panel)

        self.main_panel.pack(fill="both",expand=True)

    def apply_filter(self, event=None):
        filter = self.filterText.get()
        filter_data = [self.title] + [row for row in self.rows if filter.lower() in str(row).lower()]
        for widget in self.table.winfo_children():
            widget.destroy()
        for row, data_row in enumerate(filter_data):
            for col, dat in enumerate(data_row):
                tk.Label(self.table, text=dat, relief=tk.GROOVE, width=20).grid(row=row, column=col)

    def wipe_filter(self, event=None):
        self.eFilter.delete(0,"end")
        self.apply_filter()

    def show_table(self, event=None):
        self.title = self.data[0]
        for col,name in enumerate(self.title):
            tk.Label(self.table, text=name, relief=tk.GROOVE, width=20).grid(row=0, column=col)
        self.rows = self.data[1:]
        for row,data_row in enumerate(self.rows): 
            for col, dat in enumerate(data_row):
                tk.Label(self.table, text=dat, relief=tk.GROOVE, width=20).grid(row=row+1, column=col)

        self.table.pack(expand=True)
        self.main_canvas.create_window((0,0), window=self.table, anchor="n", tags="table")
        self.table.bind("<Configure>", lambda event, canvas=self.main_canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def open_file(self, event=None):
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            datos = [fila for fila in lector_csv]
            self.data = datos
        self.show_table()
    
    def exit(self, event=None):
            self.destroy()     

if __name__ == "__main__":
    window = Window()
    window.mainloop()