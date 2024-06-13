import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter
from tkinter import ttk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Machine Learning Application")
        self.geometry(f"{1100}x{580}")

        # Dataset
        self.df = None
        self.target = ""
        self.selected_columns = []
        self.targetExist = False

        # # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        # # create sidebar frame with widgets
        # self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        # self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        # self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # # Sidebar buttons
        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Upload Data", command=self.show_upload_view)
        # self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_models_view)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
        #                                                             command=self.change_appearance_mode_event)
        # self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # # Create main content area
        # self.main_content_frame = customtkinter.CTkFrame(self, corner_radius=0)
        # self.main_content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        # # self.main_content_frame.pack(fill=tk.BOTH, expand=True)
        
        # # Configure main_content_frame to expand with the window
        # self.main_content_frame.grid_rowconfigure(0, weight=1)
        # self.main_content_frame.grid_columnconfigure(1, weight=1)

        # # Set default values
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        
        # Configure grid layout for the main window
        self.grid_columnconfigure(0, minsize=140)  # Sidebar width
        self.grid_columnconfigure(1, weight=0)      # Main content area
        self.grid_rowconfigure(0, weight=1)         # Only the first row expands by default

        # Create sidebar frame with widgets
        self.sidebar_frame = tk.Frame(self, bg="lightgray")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = tk.Label(self.sidebar_frame, text="CustomTkinter", font=("Arial", 20, "bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.sidebar_button_1 = tk.Button(self.sidebar_frame, text="Upload Data", command=self.show_upload_view)
        self.sidebar_button_1.pack(padx=20, pady=10, anchor="w")

        self.sidebar_button_2 = tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_models_view)
        self.sidebar_button_2.pack(padx=20, pady=10, anchor="w")

        self.appearance_mode_label = tk.Label(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(padx=20, pady=(10, 0), anchor="w")

        self.appearance_mode_optionmenu = tk.OptionMenu(self.sidebar_frame, tk.StringVar(), "Light", "Dark", "System")
        self.appearance_mode_optionmenu.pack(padx=20, pady=(0, 10), anchor="w")

        # Create main content area
        self.main_content_frame = tk.Frame(self, bg="white")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")

        label_main_content = tk.Label(self.main_content_frame, text="Main Content Area", font=("Arial", 14))
        label_main_content.grid(row=0, column=0, padx=20, pady=20)

        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        # Initialize the views
        self.upload_view = self.create_upload_view()
        self.columns_form_view = self.create_columns_form_view()
        self.features_view = self.create_features_view()
        self.models_view = self.create_models_view()
        
        # Show the default view
        self.show_upload_view()

    def open_new_window(self):
        new_window = customtkinter.CTkToplevel(self)
        new_window.title("New Window")
        new_window.geometry("300x200")

        label = customtkinter.CTkLabel(new_window, text="This is a new window", font=("Helvetica", 20, "bold"))
        label.pack(pady=20)

        close_button = customtkinter.CTkButton(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=20)

    def create_upload_view(self):
        frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew")  # Make the frame fill the available space

        # Configure grid to center content
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # Title
        title_label = customtkinter.CTkLabel(frame, text="Load Dataset", font=("Helvetica", 30, "bold"))
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Upload button
        upload_button = customtkinter.CTkButton(frame, text="Upload, Excel or CSV Format", font=("Helvetica", 20, "bold"), command=self.upload_dataset)
        upload_button.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        return frame

    def upload_dataset(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.show_target_view()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {e}")

    def create_target_view(self):
        target_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")

        # Title
        title_label = customtkinter.CTkLabel(target_frame, text="Radio Button List", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # Variable to store the selected option
        self.selected_option = tk.StringVar()

        # Check if dataset is loaded
        if self.df is not None:
            # Create radio buttons for each column in the dataset
            for column_name in self.df.columns:
                radio_button = customtkinter.CTkRadioButton(target_frame, text=column_name, variable=self.selected_option, value=column_name)
                radio_button.pack(anchor="w", padx=20, pady=5)
        # else:
        #     messagebox.showerror("Error", "No dataset loaded!")

        buttons_frame = customtkinter.CTkFrame(target_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        # Button to print selected option
        button = customtkinter.CTkButton(buttons_frame, text="Next", command=self.show_features_view)
        button.grid(row=0, column=2, padx=10)

        button_prev = customtkinter.CTkButton(buttons_frame, text="Skip", command=self.target_existe)
        button_prev.grid(row=0, column=1, padx=10)

        button_prev = customtkinter.CTkButton(buttons_frame, text="Previous", command=self.show_upload_view)
        button_prev.grid(row=0, column=0, padx=10)

        return target_frame

    def create_features_view(self):
        checkbox_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")

        # Title
        title_label = customtkinter.CTkLabel(checkbox_frame, text="Features", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # Variable to store the selected options
        self.selected_options = {}

        # Check if dataset is loaded
        if self.df is not None:
            # Create checkboxes for each column in the dataset
            for column_name in self.df.columns:
                if(self.target != column_name):
                    var = tk.BooleanVar()
                    checkbox = customtkinter.CTkCheckBox(checkbox_frame, text=column_name, variable=var)
                    checkbox.pack(anchor="w", padx=20, pady=5)
                    self.selected_options[column_name] = var
        # else:
        #     messagebox.showerror("Error", "No dataset loaded!")
        print(self.selected_options)
        # Button to print selected options
        buttons_frame = customtkinter.CTkFrame(checkbox_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        # Button to go to the previous view
        button_prev = customtkinter.CTkButton(buttons_frame, text="Previous", command=self.show_target_view)
        button_prev.grid(row=0, column=0, padx=10)

        # Button to go to the columns form view
        button_next = customtkinter.CTkButton(buttons_frame, text="Next", command=self.show_columns_form_view)
        button_next.grid(row=0, column=1, padx=10)
        


        return checkbox_frame

    def create_columns_form_view(self):
        form_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")

            # Title
        title_label = customtkinter.CTkLabel(form_frame, text="Input Form", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

            # Dictionary to store the entry widgets for each column
        self.entry_widgets = {}

            # Create form fields for each selected column
        if self.selected_columns:
            for i, column_name in enumerate(self.selected_columns):
                    row = (i // 2) + 1  # Determine the row for grid placement
                    column = i % 2      # Determine the column for grid placement
                    
                    # Create label and entry widgets
                    label = customtkinter.CTkLabel(form_frame, text=column_name)
                    label.grid(row=row, column=column*2, padx=10, pady=5, sticky="e")
                    entry = customtkinter.CTkEntry(form_frame, placeholder_text=column_name)
                    entry.grid(row=row, column=column*2+1, padx=10, pady=5, sticky="w")
                    
                    # Store the entry widget
                    self.entry_widgets[column_name] = entry

            # Button to print entered values
        # button = customtkinter.CTkButton(form_frame, text="Submit", command=self.submit_form)
        # button.grid(row=(len(self.selected_columns) // 2) + 2, column=0, columnspan=2, pady=20)

        # Button to go to the previous view
        button_prev = customtkinter.CTkButton(form_frame, text="Prev", command=self.show_features_view)
        button_prev.grid(row=(len(self.selected_columns) // 2) + 2, column=0, padx=10, pady=20, sticky="w")

        # Button to submit the form
        button_submit = customtkinter.CTkButton(form_frame, text="Submit", command=self.submit_form)
        button_submit.grid(row=(len(self.selected_columns) // 2) + 2, column=1, padx=10, pady=20, sticky="e")


        return form_frame

    def submit_form(self):
        form_data = {col: self.entry_widgets[col].get() for col in self.selected_columns}
        print("Form data:", form_data)

    def create_models_view(self):
        if self.df is None:
            self.show_upload_view()
            return

        model_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent" , bg_color="red")
        model_frame.grid(row=0, column=0, sticky="nsew")  # Assuming you are using grid layout

        # Title
        title_label = customtkinter.CTkLabel(model_frame, text="Dataset and Model Information", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create dataset table
        dataset_table_frame = customtkinter.CTkFrame(model_frame, fg_color="transparent")
        dataset_table_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        dataset_table = ttk.Treeview(dataset_table_frame, show="headings")
        dataset_table["columns"] = list(self.df.columns)

        for col in self.df.columns:
            dataset_table.heading(col, text=col)
            dataset_table.column(col, anchor="center",width=100)

        for index, row in self.df.iterrows():
            dataset_table.insert("", "end", values=list(row))

        dataset_table.grid(row=0, column=0, sticky="nsew")

        # Create model statistics table
        model_table_frame = customtkinter.CTkFrame(model_frame, fg_color="transparent")
        model_table_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10, sticky="nsew")

        model_table = ttk.Treeview(model_table_frame, columns=("Model", "Accuracy", "Model Loss"), show="headings")
        model_table.heading("Model", text="Model")
        model_table.heading("Accuracy", text="Accuracy")
        model_table.heading("Model Loss", text="Model Loss")

        model_table.column("Model", anchor="center", width=100)
        model_table.column("Accuracy", anchor="center", width=100)
        model_table.column("Model Loss", anchor="center", width=100)

        # Add sample data to the model table
        for i in range(1, 4):  # Assuming we have 3 models for demonstration
            model_name = f"Model #{i}"
            target_name = self.target if self.target else "Not Set"
            model_label = f"{model_name}, Target: {target_name}"
            accuracy = f"{i * 10}%"  # Placeholder accuracy
            model_loss = f"{i * 0.1:.2f}"  # Placeholder model loss

            # Insert a row with a predict button
            model_table.insert("", "end", values=(model_label, accuracy, model_loss))

        model_table.grid(row=0, column=0, sticky="nsew")



        model_frame.grid_rowconfigure(1, weight=1)
        model_frame.grid_columnconfigure(0, weight=1)

        return model_frame



    def predict(self, model_name):
        print(f"Predicting with {model_name}")

    def show_view(self, view):
        # Remove any existing widgets in the main content frame
        for widget in self.main_content_frame.winfo_children():
            widget.grid_forget()
        # Add the new view to the main content frame
        view.grid(row=0, column=0, sticky="nsew")

    def show_upload_view(self):
        self.show_view(self.upload_view)

    def show_target_view(self):
        self.target_view = self.create_target_view()
        self.show_view(self.target_view)
    
    def show_features_view(self):
        self.targetExist = True
        self.target = self.selected_option.get()
        print(self.target)
        self.features_view = self.create_features_view()
        
        self.show_view(self.features_view)

    def show_columns_form_view(self):
        self.selected_columns = [col for col, var in self.selected_options.items() if var.get()]
        print("Selected columns:", self.selected_columns)
        self.columns_form_view = self.create_columns_form_view()
        self.show_view(self.columns_form_view)

    def show_models_view(self):
        self.models_view = self.create_models_view()
        self.show_view(self.models_view)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def target_existe(self):
        self.targetExist = False
        self.show_features_view()

if __name__ == "__main__":
    app = App()
    app.mainloop()
