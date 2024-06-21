import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np

class Unsupervised:
    def __init__(self):
        pass
    
    @staticmethod
    def apply_dbscan_and_show_results(df, selected_columns, eps=0.5, min_samples=5, inputs=None):
        if inputs is None:
            inputs = []

        # Apply DBSCAN clustering
        df_result, dbscan_model, scaler, clustering_info = Unsupervised.DBSCANClusteringModel(df, selected_columns, eps, min_samples)
        
        # Predict clusters for input data
        predictions = []
        for input_data in inputs:
            prediction = Unsupervised.predict_with_model_DBSCAN(dbscan_model, scaler, input_data)
            predictions.append(prediction)

        # Show clustering results and predictions
        Unsupervised.show_clustering_results(df_result, clustering_info, inputs, predictions)

    @staticmethod
    def show_clustering_results(df_result, clustering_info, inputs, predictions):
        # Create a new window for clustering results
        results_window = tk.Toplevel()
        results_window.title("Clustering Results")

        # Create a canvas with a scrollbar
        canvas = tk.Canvas(results_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(results_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame inside canvas to contain labels
        results_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=results_frame, anchor=tk.NW)

        # Display clustering information
        info_text = (
            f"Number of clusters: {clustering_info['n_clusters']}\n"
            f"Number of noise points: {clustering_info['n_noise']}\n"
            f"Cluster sizes:\n"
        )

        for cluster, size in clustering_info['cluster_sizes'].items():
            info_text += f"  Cluster {cluster}: {size} points\n"

        info_label = tk.Label(results_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(padx=20, pady=20, anchor=tk.W)

        # Display input data and their predicted clusters
        results_label = tk.Label(results_frame, text="Input Data and Predicted Clusters", font=("Arial", 14, "bold"))
        results_label.pack(pady=10, anchor=tk.W)

        for i, (input_data, prediction) in enumerate(zip(inputs, predictions)):
            result_text = f"Input {i + 1}: {input_data} --> Cluster: {prediction}"
            result_label = tk.Label(results_frame, text=result_text, wraplength=600, justify=tk.LEFT)
            result_label.pack(pady=5, anchor=tk.W)

        # Configure scrollbar and canvas
        results_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.config(yscrollcommand=scrollbar.set)

    @staticmethod
    def DBSCANClusteringModel(df, feat, eps=0.5, min_samples=5):
        # Extract the features for clustering
        X = df[feat]

        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan.fit(X_scaled)

        # Get the cluster labels
        labels = dbscan.labels_
        
        # Append the labels to the original dataframe
        df['Cluster'] = labels

        # Calculate clustering info
        clustering_info = {
            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
            'n_noise': list(labels).count(-1),
            'cluster_sizes': pd.Series(labels).value_counts().to_dict()
        }

        return df, dbscan, scaler, clustering_info

    @staticmethod
    def predict_with_model_DBSCAN(model, scaler, features):
        # Standardize the input features
        features_scaled = scaler.transform([features])
        
        # Predict the cluster for the new features
        prediction = model.fit_predict(features_scaled)
        return prediction[0]
    
    