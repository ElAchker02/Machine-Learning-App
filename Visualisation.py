import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sklearn.preprocessing import LabelEncoder


class DataVisualizerClass(tk.Tk):
    def __init__(self):
        super().__init__()


    @staticmethod
    def show_histograms_view(self,dfP):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Warning", "No dataset loaded!")
            return

        # Create a new window for histograms
        histograms_window = tk.Toplevel(self)
        histograms_window.title("Histograms")

        # Canvas and scrollbar for histograms
        canvas = tk.Canvas(histograms_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(histograms_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame inside canvas to contain histograms
        histograms_frame = ttk.Frame(canvas)
        histograms_frame.pack(fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=histograms_frame, anchor=tk.NW)

        # Preprocess data
        self.df  =  dfP

        # Create histograms for each column
        num_columns = len(self.df.columns)
        for i, col in enumerate(self.df.columns):
            if i % 2 == 0:
                # Create a new row frame for every two histograms
                row_frame = ttk.Frame(histograms_frame)
                row_frame.pack(fill=tk.BOTH, padx=10, pady=10)

            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(self.df[col], kde=True, color='blue', ax=ax)
            ax.set_title(f'Histogram of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.grid(True)

            # Embedding matplotlib plot into tkinter
            canvas = FigureCanvasTkAgg(fig, master=row_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

        # Configure scrollbar and canvas
        histograms_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.config(yscrollcommand=scrollbar.set)

    @staticmethod
    def show_heatmap_view(self,dfP):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Warning", "No dataset loaded!")
            return

        # Create a new window for heatmap
        heatmap_window = tk.Toplevel(self)
        heatmap_window.title("Heatmap")

        # Frame to contain the heatmap plot
        heatmap_frame = ttk.Frame(heatmap_window)
        heatmap_frame.pack(fill=tk.BOTH, expand=True)

        # Preprocess data (fill missing values and encode categorical variables if needed)
        self.df = dfP

        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap')
        ax.set_xlabel('Features')
        ax.set_ylabel('Features')

        # Embedding matplotlib plot into tkinter
        canvas = FigureCanvasTkAgg(fig, master=heatmap_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @staticmethod
    def show_pie_chart_view(self,dfP):
        if self.df is None or self.df.empty:
            messagebox.showwarning("Warning", "No dataset loaded!")
            return

        # Find all categorical columns
        categorical_columns = self.df.select_dtypes(include=['object']).columns

        if len(categorical_columns) == 0:
            messagebox.showwarning("Warning", "No categorical columns available!")
            return

        # Create a new window for Pie Charts
        pie_charts_window = tk.Toplevel(self)
        pie_charts_window.title("Pie Charts")
        
        self.df = dfP
        
        # Iterate over each categorical column
        for col in categorical_columns:
            # Frame to contain the Pie Chart plot for each column
            pie_chart_frame = ttk.Frame(pie_charts_window)
            pie_chart_frame.pack(fill=tk.BOTH, expand=True)

            counts = self.df[col].value_counts()

            # Plotting Pie Chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
            ax.set_title(f'Pie Chart of {col}')

            # Embedding matplotlib plot into tkinter
            canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)