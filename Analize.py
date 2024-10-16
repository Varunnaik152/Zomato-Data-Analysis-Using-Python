import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import Button, Label, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the data
dataframe = pd.read_csv("C:\\Users\\Varun\\Python Project\\Zomato data .csv")

# Handle the 'rate' column
def handleRate(value):
    value = str(value).split('/')
    value = value[0]
    try:
        return float(value)
    except ValueError:
        return np.nan

dataframe['rate'] = dataframe['rate'].apply(handleRate)

# Prepare plots
def plot1():
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='listed_in(type)', data=dataframe, ax=ax, palette='Set2')
    ax.set_xlabel("Type of Restaurant", fontsize=12, fontweight='bold')
    ax.set_title("Count of Restaurants by Type", fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot2():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(dataframe['rate'].dropna(), bins=15, color='skyblue', edgecolor='black')
    ax.set_title("Ratings Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Rating", fontsize=12, fontweight='bold')
    ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot3():
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='online_order', y='rate', data=dataframe, ax=ax, palette='Set1')
    ax.set_title("Boxplot of Ratings by Online Order", fontsize=14, fontweight='bold')
    ax.set_xlabel("Online Order", fontsize=12, fontweight='bold')
    ax.set_ylabel("Rating", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot4():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(dataframe['approx_cost(for two people)'], bins=20, kde=False, ax=ax, color='coral')
    ax.set_title("Approx Cost Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Approx Cost", fontsize=12, fontweight='bold')
    ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot5():
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt='d', ax=ax, cbar_kws={'label': 'Count'})
    ax.set_title("Heatmap of Online Order by Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Online Order", fontsize=12, fontweight='bold')
    ax.set_ylabel("Listed In (Type)", fontsize=12, fontweight='bold')
    return fig

def plot6():
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
    result = pd.DataFrame({'votes': grouped_data})
    ax.plot(result, c="green", marker="o", linestyle='-', linewidth=2)
    ax.set_xlabel("Type of Restaurant", fontsize=12, fontweight='bold', color="red")
    ax.set_ylabel("Votes", fontsize=12, fontweight='bold', color="red")
    ax.set_title("Votes by Restaurant Type", fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot_top5():
    top5 = dataframe[['name', 'rate']].dropna().nlargest(5, 'rate')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='rate', y='name', data=top5, ax=ax, palette='viridis')
    ax.set_title("Top 5 Restaurants by Rating", fontsize=14, fontweight='bold')
    ax.set_xlabel("Rating", fontsize=12, fontweight='bold')
    ax.set_ylabel("Restaurant Name", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

def plot_last5():
    last5 = dataframe[['name', 'rate']].dropna().nsmallest(5, 'rate')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='rate', y='name', data=last5, ax=ax, palette='coolwarm')
    ax.set_title("Last 5 Restaurants by Rating", fontsize=14, fontweight='bold')
    ax.set_xlabel("Rating", fontsize=12, fontweight='bold')
    ax.set_ylabel("Restaurant Name", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

# Setup Tkinter GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualization")

        # Include the new plot function in the list
        self.plot_functions = [plot1, plot2, plot3, plot4, plot5, plot6, plot_top5, plot_last5]
        self.current_plot = 0

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        self.next_button = Button(self.button_frame, text="Next", command=self.next_plot)
        self.next_button.pack(side=tk.RIGHT)

        self.preview_button = Button(self.button_frame, text="Preview", command=self.preview_plot)
        self.preview_button.pack(side=tk.LEFT)

        self.save_button = Button(self.button_frame, text="Save Plot", command=self.save_plot)
        self.save_button.pack(side=tk.LEFT)

        self.title_label = Label(root, text=self.plot_functions[self.current_plot]().__doc__)
        self.title_label.pack()

        self.canvas = None  # Initialize canvas variable
        self.show_plot()

    def show_plot(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()  # Remove the previous canvas widget

        plt.close('all')  # Close any previously opened plot
        fig = self.plot_functions[self.current_plot]()
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Update the plot title label
        self.title_label.config(text=fig.axes[0].get_title())

    def next_plot(self):
        self.current_plot = (self.current_plot + 1) % len(self.plot_functions)
        self.show_plot()

    def preview_plot(self):
        self.current_plot = (self.current_plot - 1) % len(self.plot_functions)
        self.show_plot()

    def save_plot(self):
        fig = self.plot_functions[self.current_plot]()
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            fig.savefig(file_path)

root = tk.Tk()
app = App(root)
root.mainloop()
