import tkinter
from tkinter import ttk
import sqlite3

class Sqlite_connection:
    SELECT_ALL_PARTS = "SELECT * FROM parts"
    SELECT_ONE_PART = "SELECT number_part, length FROM parts WHERE parts.number_part = ?;"
    INSERT_INTO_NEW_PART = "INSERT INTO parts(number_part, length) VALUES(?, ?);"
    UPDATE_LENGTH_PART = "UPDATE parts SET length = ? WHERE number_part = ?"
    CREATE_TABLE = """
    CREATE TABLE parts(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   number_part TEXT NOT NULL UNIQUE,
                   length INTEGER);
"""

    DB_NAME = "database.db"

    def __init__(self):
        try:
            self.query(self.CREATE_TABLE)

        except sqlite3.OperationalError as e:
            print(e)

    def query(self, query, parameters = ()):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        querySpan = cursor.fetchall()
        print(querySpan)
        conn.commit()
        conn.close()
        return querySpan

    def select_all(self):
        return self.query(self.SELECT_ALL_PARTS)

    def sqlite_close(self):
        self.conn.closed()

class Window_toplevel:
    def __init__(self, items):
        self.toplevel = self.create_toplevel()
        self.treeview = self.create_treeview()
        self.set_treeview(items)

    def create_toplevel(self):
        toplevel = tkinter.Toplevel()
        toplevel.title("todo")
        return toplevel

    def create_treeview(self):
        tree = ttk.Treeview(self.toplevel,height=10, columns=("lenght",))
        tree.pack()
        tree.heading("#0", text="nombre de parte", anchor=tkinter.CENTER)
        tree.heading("lenght", text="cantidad", anchor=tkinter.CENTER)

        return tree
    
    def set_treeview(self, items): 
        for row in items:
            self.treeview.insert('', 0, text=row[0], values=row[1])
    
        
class Widgets: 
    def __init__(self, window):
        self.stringvar = tkinter.StringVar()
        self.entry = self.create_entry(window)
        self.configure_style()

        ttk.Label(window, text="Historial de inserciones", style="Label").pack()
        self.treeView = self.create_tree()
        self.sql_conn = Sqlite_connection()
        self.button = tkinter.Button(window, text="Mostrar tood", command=self.on_create_tree).pack()

    def configure_style(self):
        style = ttk.Style()
        style.configure("Label", foreground="red")
        return style
    
    def create_entry(self, window):
        entry = ttk.Entry(window, textvariable=self.stringvar, font=("Arial", 15), width="100")
        entry.focus()
        entry.pack(pady=20)
        entry.bind("<Return>", self.on_return)
        return entry
    
    def on_return(self, event):
        entry_value = self.stringvar.get()
        self.stringvar.set('')
        query = self.sql_conn.query(self.sql_conn.SELECT_ONE_PART, (entry_value,))
        if(len(query) < 1):
            query = (entry_value, 1)
            self.sql_conn.query(self.sql_conn.INSERT_INTO_NEW_PART, query)
        else:
            query = query[0]
            query = (query[0], query[1] + 1)
            self.sql_conn.query(self.sql_conn.UPDATE_LENGTH_PART, (query[1] + 1, query[0]))
            
        self.treeView.insert('', 0, text=query[0], values=query[1])

    def create_tree(self):
        tree = ttk.Treeview(height=10, columns=("lenght",))
        tree.pack()
        tree.heading("#0", text="nombre de parte", anchor=tkinter.CENTER)
        tree.heading("lenght", text="cantidad", anchor=tkinter.CENTER)

        return tree
    
    def on_create_tree(self):
        
        Window_toplevel(self.sql_conn.query(self.sql_conn.SELECT_ALL_PARTS))

        
        


class Window:
    def __init__(self):
        self.window = self.create_window()
        self.widgets = Widgets(self.window)


    def create_window(self):
        window = tkinter.Tk()
        window.wm_attributes("-topmost", True)
        window.geometry("400x400")
        # window.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        # window.overrideredirect(True) quita el window manager
        
        return window

        
    def begin(self):
        self.window.mainloop()
        

if __name__ in "__main__":
    window = Window()
    window.begin()