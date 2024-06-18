import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter
from tkinter import ttk
from AlgoMl import AlgoML


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Machine Learning Application")
        self.geometry(f"{1100}x{580}")

        #Initialize Class
        self.algos = AlgoML()

        # Dataset
        self.df = None
        self.dfPreprocessed = None
        self.target = ""
        self.selected_columns = []
        self.inputs = []
        self.targetExist = False
        self.chosenAlgorithm = "Linear Regression"
        self.encoding_dict = {}
        
        
        # Configure grid layout for the main window
        self.grid_columnconfigure(0, minsize=140)  # Sidebar width
        self.grid_columnconfigure(1, weight=1)      # Main content area
        self.grid_rowconfigure(0, weight=1)         # Only the first row expands by default

        # Create sidebar frame with widgets
        self.sidebar_frame = tk.Frame(self, bg="lightgray")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=("Arial", 20, "bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Upload Data", command=self.show_upload_view)
        self.sidebar_button_1.pack(padx=20, pady=10, anchor="w")

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="List of \nDatasets", command=self.show_models_view)
        self.sidebar_button_2.pack(padx=20, pady=10, anchor="w")

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
        upload_button = customtkinter.CTkButton(frame, text="Upload, Excel \n or \n CSV Format", font=("Helvetica", 20, "bold"), command=self.upload_dataset)
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
        title_label = customtkinter.CTkLabel(target_frame, text="Choose the target", font=("Helvetica", 20, "bold"))
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

        button_prev = customtkinter.CTkButton(buttons_frame, text="Skip", command=self.skipTarget)
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
        button_next = customtkinter.CTkButton(buttons_frame, text="Next", command=self.show_models_view)
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

                if column_name in self.encoding_dicto:
                    # Create a dropdown for categorical columns with readable labels
                    values = list(self.encoding_dicto[column_name].keys())
                    entry = customtkinter.CTkComboBox(form_frame, values=values)
                else:
                    # Create an entry widget for numerical columns
                    entry = customtkinter.CTkEntry(form_frame, placeholder_text=column_name)

                entry.grid(row=row, column=column*2+1, padx=10, pady=5, sticky="w")

                # Store the entry widget
                self.entry_widgets[column_name] = entry

        # Button to go to the previous view
        button_prev = customtkinter.CTkButton(form_frame, text="Prev", command=self.show_models_view)
        button_prev.grid(row=(len(self.selected_columns) // 2) + 2, column=0, padx=10, pady=20, sticky="w")

        # Button to submit the form
        button_submit = customtkinter.CTkButton(form_frame, text="Submit", command=self.submit_form)
        button_submit.grid(row=(len(self.selected_columns) // 2) + 2, column=1, padx=10, pady=20, sticky="e")

        # Add label at the end of the form
        self.prediction = customtkinter.CTkLabel(form_frame, text=f"Prediction of target {self.target} is ")
        self.prediction.grid(row=(len(self.selected_columns) // 2) + 3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        return form_frame



    def AlgorithmChosen(self, algorithm):
        result = None
        match algorithm:
            case "Decision Tree Classifier":
                result = AlgoML.DecisionTreeClassifierModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "Random Forest Classifier":
                result = AlgoML.RandomForestClassifierModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "Logistic Regression":
                result = AlgoML.LogisticRegressionModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "Linear Regression":
                result = AlgoML.LinearRegressionModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "Decision Tree Regressor":
                result = AlgoML.DecisionTreeRegressionModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "Random Forest Regressor":
                result = AlgoML.RandomForestRegressionModel(self,self.dfPreprocessed,self.target,self.selected_columns,self.inputs)
            case "K-Means":
                pass
            case "DBSCAN":
                pass
            case "PCA Variance Explained":
                pass
            case "t-SNE":
                pass
        
        return result

    # def submit_form(self):
    #     # form_data = {col: self.entry_widgets[col].get() for col in self.selected_columns}
    #     form_data = []
    #     for col in self.selected_columns:
    #         form_data.append(self.entry_widgets[col].get())
    #     self.inputs = form_data
    #     result = self.AlgorithmChosen(self.chosenAlgorithm)
    #     self.prediction.configure(text=f"Prediction of target {self.target} is {result[0]}")

    def submit_form(self):
        # Collect the values from the form
        form_data = []
        for col in self.selected_columns:
            if col in self.encoding_dicto:
                # If the column is categorical, get the selected readable value from the dropdown
                selected_value = self.entry_widgets[col].get()
                # Convert the readable value to the corresponding numerical value
                form_data.append(self.encoding_dicto[col][selected_value])
            else:
                # Otherwise, get the text value from the entry widget and convert to float
                form_data.append(float(self.entry_widgets[col].get()))

        self.inputs = form_data
        result = self.AlgorithmChosen(self.chosenAlgorithm)
        self.prediction.configure(text=f"Prediction of target {self.target} is {result[0]}")


    def create_models_view(self):
        if self.df is None:
            self.show_upload_view()
            return

        model_frame = customtkinter.CTkFrame(self.main_content_frame, fg_color="transparent")
        model_frame.grid(row=0, column=0, sticky="nsew")

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
            dataset_table.column(col, anchor="center", width=100)

        for index, row in self.df.iterrows():
            if(index == 50):
                break
            dataset_table.insert("", "end", values=list(row))

        dataset_table.grid(row=0, column=0, sticky="nsew")

        # Create model statistics table with custom layout
        model_table_frame = customtkinter.CTkFrame(model_frame, fg_color="transparent")
        model_table_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10, sticky="nsew")

        # Add header for the model table
        # headers = ["Model", "Accuracy", "Model Loss"]
        headers = ["Model", "Action", "Accuracy"]

        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(model_table_frame, text=header, font=("Helvetica", 12, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        i = 1
        self.dfPreprocessed , self.encoding_dicto = AlgoML.preprocess_data(self.df)
        print(self.encoding_dicto)
        results = AlgoML.apply_ml_algorithms(self,self.dfPreprocessed,self.target)
        for algo, score in results.items():
            model_number = f"Model #{i} : "
            model_name = f"{algo}"
            target_name = self.target if hasattr(self, 'target') else "Not Set"
            model_label = f"{model_number}{model_name}\n- Target: {target_name}"
            accuracy = f"{round(score*100,2)}%"
            #model_loss = f"{i * 0.1:.2f}"

            # Add model label
            model_label_widget = customtkinter.CTkLabel(model_table_frame, text=model_label)
            model_label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # Add predict button
            predict_button = customtkinter.CTkButton(model_table_frame, text="PREDICT", command=lambda m=model_name: self.predict(m))
            predict_button.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            # Add model loss label
            loss_label = customtkinter.CTkLabel(model_table_frame, text=accuracy)
            loss_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")
            i = i +1

        model_frame.grid_rowconfigure(1, weight=1)
        model_frame.grid_columnconfigure(0, weight=1)

        return model_frame

    def predict(self, model_name):
        self.chosenAlgorithm = model_name
        print(self.chosenAlgorithm)
        self.show_columns_form_view()

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
        if self.target:
            self.features_view = self.create_features_view()
            self.show_view(self.features_view)
        else:
            # messagebox.showwarning("No Selection", "Please select a target column.")s
            self.target = "unkown"
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

    def skipTarget(self):
        self.targetExist = False
        self.show_features_view()

        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
