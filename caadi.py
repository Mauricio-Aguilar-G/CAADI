import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize our data array
        self.data = []

        # Establish our window dimensions
        self.title("CAADI")
        self.geometry("650x500")

        # Create our main window panels
        self.main_panel = ttk.PanedWindow(orient="vertical")
        self.horiz_panel = ttk.PanedWindow(orient="horizontal")

        # Define what our main_panel is composed of
            #Frame that stores our components
        self.side_frame = tk.Frame(self.horiz_panel,bg="#DBD0C5")
            #Button
        self.bUpload = tk.Button(self.side_frame, text="Subir archivo", fg="white",bg="#C39A7A",border="0",height="2",command=self.open_file)
        self.bUpload.pack(side="top", fill="x")
            #Label
        self.lFilter = tk.Label(self.side_frame,text="Filtro: ", bg="#DBD0C5")
        self.lFilter.pack(fill="x", pady="15 0")
            #Entry
        self.filterText = tk.StringVar()
        self.eFilter = tk.Entry(self.side_frame, textvariable=self.filterText)
        self.eFilter.pack(fill="x", padx="5", pady="0 15")
            #Button
        self.bFilter = tk.Button(self.side_frame,text="Aplicar filtro",fg="white",bg="#B8926A",border="0",height="2",command=self.apply_filter)
        self.bFilter.pack(fill="x")
            #Button
        self.bLimpiar = tk.Button(self.side_frame,text="Limpiar filtro",fg="white",bg="#854621",border="0",height="2",command=self.wipe_filter)
        self.bLimpiar.pack(fill="x")
            #Button
        self.bExit = tk.Button(self.side_frame, text="SALIR", fg="white", bg="#423025",border="0",height="2",command=exit)
        self.bExit.pack(side="bottom", fill="x")
            #Add components to horiz_frame(LEFT SIDE)
        self.horiz_panel.add(self.side_frame)

        #Define whate our horiz_frame(RIGHT SIDE) is gonna contain
            #Frame
        self.main_frame = tk.Frame(self.horiz_panel)
            #Canvas for scrolling
        self.main_canvas = tk.Canvas(self.main_frame)
            #Table for our data
        self.table = tk.Frame(self.main_canvas, bg="#F2F3EC")
            #Configure scrollbar
        self.scrollbar = tk.Scrollbar(self.main_canvas,orient="vertical",command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right",fill="y")
        self.main_canvas.pack(fill="both", expand=True)
        
        #Bind "enter" with a function
        self.bind("<Return>", self.apply_filter)

        #Add our RIGHT_SIDE to the lower panel
        self.horiz_panel.add(self.main_frame)
        
        #Add lower panel to the maine panel
        self.main_panel.pack(fill="both",expand=True)
        self.main_panel.add(self.horiz_panel)

        
    #Methods
    def apply_filter(self, event=None):
        # Read the entry's text
        filter = self.filterText.get()
        # Filter our data to obtain the matches
        filter_data = [self.title] + [row for row in self.rows if filter.lower() in str(row).lower()]
        # Erase the table
        for widget in self.table.winfo_children():
            widget.destroy()
        # Show only the filtered data
        for row, data_row in enumerate(filter_data):
            for col, dat in enumerate(data_row):
                tk.Label(self.table, text=dat, relief=tk.GROOVE, width=20).grid(row=row, column=col)

    def wipe_filter(self, event=None):
        # Delete the entry's text and reload the table
        self.eFilter.delete(0,"end")
        self.apply_filter()

    def show_table(self, event=None):
        # Create and show the head of the table
        self.title = self.data[0]
        for col,name in enumerate(self.title):
            tk.Label(self.table, text=name, relief=tk.GROOVE, width=20).grid(row=0, column=col)
        # Create and show the table
        self.rows = self.data[1:]
        for row,data_row in enumerate(self.rows): 
            for col, dat in enumerate(data_row):
                tk.Label(self.table, text=dat, relief=tk.GROOVE, width=20).grid(row=row+1, column=col)

        self.table.pack(expand=True)
        self.main_canvas.create_window((0,0), window=self.table, anchor="n", tags="table")
        self.table.bind("<Configure>", lambda event, canvas=self.main_canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def open_file(self, event=None):
        # Load the data and store it in datos
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            datos = [fila for fila in lector_csv]
            self.data = datos
        self.show_table()
    
    def exit(self, event=None):
            # Close the window
            self.destroy()     

if __name__ == "__main__":
    # Create a window class object
    window = Window()
    # Execute the window
    window.mainloop()
