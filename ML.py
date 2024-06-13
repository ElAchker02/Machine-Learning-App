from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        #Dataset
        self.df = None

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Upload Data", command=self.show_upload_view)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_target_view)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=self.show_columns_form_view)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                    command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create main content area
        self.main_content_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        
        # Set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Initialize the views
        self.upload_view = self.create_upload_view()
        self.target_view = self.create_target_view()
        self.columns_form_view = self.create_columns_form_view()
        
        # Show the default view
        self.show_upload_view()

        # Button to open a new window
        # self.open_window_button = customtkinter.CTkButton(
        #     self.main_frame, 
        #     text="Open New Window", 
        #     command=self.open_new_window
        # )
        # self.open_window_button.pack(pady=20)

        

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
                messagebox.showinfo("Success", "Dataset loaded successfully!")
                self.show_target_view()
                return self.df
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {e}")
        return None
        
        
    def create_target_view(self):
        target_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")

        # Title
        title_label = customtkinter.CTkLabel(target_frame, text="Radio Button List", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # Variable to store the selected option
        self.selected_option = tk.StringVar()
        dataset = self.df
        # Create radio buttons for each column in the dataset
        for column_name in dataset.columns:
            radio_button = customtkinter.CTkRadioButton(target_frame, text=column_name, variable=self.selected_option, value=column_name)
            radio_button.pack(anchor="w", padx=20, pady=5)


        # Button to print selected option
        button = customtkinter.CTkButton(target_frame, text="Next", command=self.show_columns_form_view)
        button.pack(pady=20)

        
        return target_frame
        
    def create_columns_form_view(self):
        frame = customtkinter.CTkFrame(self.main_content_frame)
        label = customtkinter.CTkLabel(frame, text="Settings View")
        label.pack(padx=20, pady=20)
        return frame

    def show_view(self, view):
        # Remove any existing widgets in the main content frame
        for widget in self.main_content_frame.winfo_children():
            widget.pack_forget()
        # Add the new view to the main content frame
        view.pack(fill="both", expand=True)

    def show_upload_view(self):
        self.show_view(self.upload_view)

    def show_target_view(self):
        self.show_view(self.target_view)

    def show_columns_form_view(self):
        print(f"Selected option: {self.selected_option.get()}")
        self.show_view(self.columns_form_view)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
