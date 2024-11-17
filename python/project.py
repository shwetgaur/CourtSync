import tkinter as tk
from tkinter import messagebox
import pymysql

class CourtCaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CourtSync")
        self.root.geometry("600x400")
        
        # Database connection
        self.db_connection = None
        self.db_cursor = None
        self.connect_to_database()
        
        self.selected_table = None
        self.selected_action = None
        self.setup_main_menu()

    def connect_to_database(self):
        try:
            self.db_connection = pymysql.connect(
                host="localhost",
                user="root",
                password="Shadow@25",
                database="court_case_scheduling_system"
            )
            self.db_cursor = self.db_connection.cursor()
            print("Database connection successful!")
        except pymysql.MySQLError as e:
            print(f"Failed to connect to the database: {e}")
            messagebox.showerror("Database Error", "Failed to connect to the database.")
            self.db_connection = None
            self.db_cursor = None

    def setup_main_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text="Select a Table to Perform Actions", font=("Arial", 14))
        label.pack(pady=20)

        tables = ["Clients", "Lawyers", "Judges", "Courtrooms", "Cases", "Schedules"]
        for table in tables:
            button = tk.Button(self.root, text=table, font=("Arial", 12),
                               command=lambda t=table: self.select_table(t))
            button.pack(pady=5)

        exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit)
        exit_button.pack(pady=20)

    def select_table(self, table):
        self.selected_table = table
        self.show_crud_menu()

    def show_crud_menu(self):
        self.clear_window()
        label = tk.Label(self.root, text=f"Select an Operation for {self.selected_table}", font=("Arial", 14))
        label.pack(pady=20)

        actions = [("Add", self.show_add_form), ("Update", self.show_update_form),
                   ("Delete", self.show_delete_form), ("View", self.show_view_table)]
        for action_text, action_cmd in actions:
            button = tk.Button(self.root, text=action_text, font=("Arial", 12), command=action_cmd)
            button.pack(pady=5)

        home_button = tk.Button(self.root, text="Back to Home", font=("Arial", 12), command=self.setup_main_menu)
        home_button.pack(pady=20)

    def show_add_form(self):
        self.clear_window()
        label = tk.Label(self.root, text=f"Add Entry to {self.selected_table}", font=("Arial", 14))
        label.pack(pady=20)

        # Dynamic input fields based on the selected table's structure
        entries = []
        columns = self.get_table_columns()
        for column in columns:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            label = tk.Label(frame, text=column, width=15, anchor="w")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            entries.append((column, entry))

        def add_entry():
            values = [entry.get() for _, entry in entries]
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {self.selected_table} ({', '.join(columns)}) VALUES ({placeholders})"
            self.execute_query(query, values)
            messagebox.showinfo("Success", f"Entry added to {self.selected_table}")
            self.show_crud_menu()

        submit_button = tk.Button(self.root, text="Submit", font=("Arial", 12), command=add_entry)
        submit_button.pack(pady=10)

    def show_update_form(self):
        self.clear_window()
        label = tk.Label(self.root, text=f"Update Entry in {self.selected_table}", font=("Arial", 14))
        label.pack(pady=20)

        # Primary key field for selecting the record to update
        pk_column = self.get_primary_key_column()
        pk_frame = tk.Frame(self.root)
        pk_frame.pack(pady=5)
        pk_label = tk.Label(pk_frame, text=f"{pk_column} (Primary Key)", width=20, anchor="w")
        pk_label.pack(side=tk.LEFT)
        pk_entry = tk.Entry(pk_frame)
        pk_entry.pack(side=tk.LEFT)

        # Fields for update values
        entries = []
        columns = self.get_table_columns(exclude_pk=True)
        for column in columns:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            label = tk.Label(frame, text=column, width=15, anchor="w")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            entries.append((column, entry))

        def update_entry():
            pk_value = pk_entry.get()
            values = [entry.get() for _, entry in entries]
            set_clause = ', '.join([f"{col} = %s" for col, _ in entries])
            query = f"UPDATE {self.selected_table} SET {set_clause} WHERE {pk_column} = %s"
            self.execute_query(query, values + [pk_value])
            messagebox.showinfo("Success", f"Entry updated in {self.selected_table}")
            self.show_crud_menu()

        submit_button = tk.Button(self.root, text="Submit", font=("Arial", 12), command=update_entry)
        submit_button.pack(pady=10)

    def show_delete_form(self):
        self.clear_window()
        label = tk.Label(self.root, text=f"Delete Entry from {self.selected_table}", font=("Arial", 14))
        label.pack(pady=20)

        pk_column = self.get_primary_key_column()
        pk_frame = tk.Frame(self.root)
        pk_frame.pack(pady=5)
        pk_label = tk.Label(pk_frame, text=f"{pk_column} (Primary Key)", width=20, anchor="w")
        pk_label.pack(side=tk.LEFT)
        pk_entry = tk.Entry(pk_frame)
        pk_entry.pack(side=tk.LEFT)

        def delete_entry():
            pk_value = pk_entry.get()
            query = f"DELETE FROM {self.selected_table} WHERE {pk_column} = %s"
            self.execute_query(query, [pk_value])
            messagebox.showinfo("Success", f"Entry deleted from {self.selected_table}")
            self.show_crud_menu()

        delete_button = tk.Button(self.root, text="Delete", font=("Arial", 12), command=delete_entry)
        delete_button.pack(pady=10)

    def show_view_table(self):
        self.clear_window()
        label = tk.Label(self.root, text=f"Viewing All Entries in {self.selected_table}", font=("Arial", 14))
        label.pack(pady=10)
    
        # Frame for scrollable view
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
    
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        # Pack canvas and scrollbar into the frame
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        try:
            # Fetch column names
            self.db_cursor.execute(f"DESCRIBE {self.selected_table}")
            columns = self.db_cursor.fetchall()
            
            # Display column headers
            header_row = tk.Frame(scrollable_frame)
            header_row.pack(fill=tk.X)
            for col in columns:
                header_label = tk.Label(header_row, text=col[0], font=("Arial", 10, "bold"), width=15, anchor="w")
                header_label.pack(side=tk.LEFT, padx=5, pady=5)
    
            # Retrieve and display table rows
            self.db_cursor.execute(f"SELECT * FROM {self.selected_table}")
            rows = self.db_cursor.fetchall()
    
            for row in rows:
                row_frame = tk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X)
                for cell in row:
                    row_label = tk.Label(row_frame, text=cell, anchor="w", width=15)
                    row_label.pack(side=tk.LEFT, padx=5, pady=5)
        except pymysql.MySQLError as e:
            messagebox.showerror("Query Error", f"Failed to retrieve data: {e}")
        
        back_button = tk.Button(self.root, text="Back to CRUD Menu", font=("Arial", 12), command=self.show_crud_menu)
        back_button.pack(pady=10)



    def get_table_columns(self, exclude_pk=False):
        columns_dict = {
            "Clients": ["ClientID", "Name", "ContactInfo"],
            "Lawyers": ["LawyerID", "Name", "Specialty", "ContactInfo"],
            "Judges": ["JudgeID", "Name", "ExperienceYears", "ContactInfo"],
            "Courtrooms": ["CourtroomID", "Location", "Capacity", "Availability"],
            "Cases": ["CaseID", "ClientID", "LawyerID", "CaseType", "CaseStatus", "StartDate", "EndDate"],
            "Schedules": ["ScheduleID", "CaseID", "CourtroomID", "JudgeID", "Date", "Time"]
        }
        columns = columns_dict[self.selected_table]
        return columns[1:] if exclude_pk else columns

    def get_primary_key_column(self):
        pk_columns = {
            "Clients": "ClientID",
            "Lawyers": "LawyerID",
            "Judges": "JudgeID",
            "Courtrooms": "CourtroomID",
            "Cases": "CaseID",
            "Schedules": "ScheduleID"
        }
        return pk_columns[self.selected_table]

    def execute_query(self, query, values):
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Query Error", f"Failed to execute query: {e}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = CourtCaseApp(root)
root.mainloop()
