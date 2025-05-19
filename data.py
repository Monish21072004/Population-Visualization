import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class PopulationVisualizer(tk.Tk):
    DEFAULT_CSV = r"C:\Users\Monish V\OneDrive\Documents\RANDOM_PROJECTS\Data-Science\Dataset\Wolrd Population Data.csv"

    def __init__(self):
        super().__init__()
        self.title("🌍 World Population Visualizer")
        self.geometry("1100x720")
        self.configure(bg="#f7f7f7", padx=10, pady=10)

        self.df = None
        self.population_col = 'Population'

        # Style
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=6, font=('Segoe UI', 11), background="#4CAF50", foreground="white")
        style.configure('TLabel', padding=5, font=('Segoe UI', 11), background="#f7f7f7")
        style.configure('TFrame', background='#f7f7f7')
        style.configure('TLabelframe', background='#e0e0e0', padding=10, font=('Segoe UI', 11))
        style.configure('TSpinbox', arrowsize=16)
        style.configure('TRadiobutton', background="#e0e0e0", font=('Segoe UI', 11))

        self._create_widgets()
        self._layout_widgets()

        self._show_placeholder()

    def _create_widgets(self):
        # Left control panel
        self.left_frame = ttk.Frame(self, width=250, relief=tk.RIDGE, padding=10)

        self.load_btn = ttk.Button(self.left_frame, text="📂 Load CSV", command=self._load_default_or_choose)
        self.file_label = ttk.Label(self.left_frame, text=os.path.basename(self.DEFAULT_CSV), foreground="gray")

        # Mode Selection
        self.mode_var = tk.StringVar(value='Top N')
        mode_frame = ttk.Labelframe(self.left_frame, text="Select Mode", relief=tk.RIDGE)
        self.radio_top = ttk.Radiobutton(mode_frame, text="Top N", variable=self.mode_var, value='Top N', command=self._update_mode)
        self.radio_range = ttk.Radiobutton(mode_frame, text="Range", variable=self.mode_var, value='Range', command=self._update_mode)
        self.radio_all = ttk.Radiobutton(mode_frame, text="All", variable=self.mode_var, value='All', command=self._update_mode)

        # Top N controls
        self.topn_var = tk.IntVar(value=10)
        self.topn_label = ttk.Label(self.left_frame, text="Top N:")
        self.topn_spin = ttk.Spinbox(self.left_frame, from_=1, to=100, textvariable=self.topn_var, width=7)

        # Range controls
        self.start_var = tk.IntVar(value=1)
        self.end_var = tk.IntVar(value=10)
        self.start_label = ttk.Label(self.left_frame, text="Start Rank:")
        self.start_spin = ttk.Spinbox(self.left_frame, from_=1, to=100, textvariable=self.start_var, width=7)
        self.end_label = ttk.Label(self.left_frame, text="End Rank:")
        self.end_spin = ttk.Spinbox(self.left_frame, from_=1, to=100, textvariable=self.end_var, width=7)

        # Chart Buttons
        self.pie_btn = ttk.Button(self.left_frame, text="🥧 Pie Chart", command=self._plot_pie)
        self.vbar_btn = ttk.Button(self.left_frame, text="📊 Vertical Bar", command=self._plot_bar)
        self.hbar_btn = ttk.Button(self.left_frame, text="📈 Horizontal Bar", command=self._plot_hbar)
        self.hist_btn = ttk.Button(self.left_frame, text="📚 Histogram", command=self._plot_hist)
        self.scatter_btn = ttk.Button(self.left_frame, text="🎯 Scatter Plot", command=self._plot_scatter)

        self.plot_frame = ttk.Frame(self, relief=tk.SUNKEN)
        self.status = ttk.Label(self, text="✅ Ready", anchor=tk.W, relief=tk.SUNKEN, font=('Segoe UI', 10, 'italic'))

    def _layout_widgets(self):
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.load_btn.pack(fill=tk.X, pady=(0, 5))
        self.file_label.pack(fill=tk.X, pady=(0, 10))

        mode_frame = self.left_frame.winfo_children()[2]
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        self.radio_top.pack(anchor=tk.W, pady=2)
        self.radio_range.pack(anchor=tk.W, pady=2)
        self.radio_all.pack(anchor=tk.W, pady=2)

        self.topn_label.pack(anchor=tk.W, pady=(5,0))
        self.topn_spin.pack(fill=tk.X)

        self.start_label.pack(anchor=tk.W, pady=(10,0))
        self.start_spin.pack(fill=tk.X)
        self.end_label.pack(anchor=tk.W)
        self.end_spin.pack(fill=tk.X)

        for btn in (self.pie_btn, self.vbar_btn, self.hbar_btn, self.hist_btn, self.scatter_btn):
            btn.pack(fill=tk.X, pady=4)

        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.status.pack(fill=tk.X, side=tk.BOTTOM, pady=(5,0))

        self._update_mode()

    def _update_mode(self):
        mode = self.mode_var.get()
        if mode == 'Top N':
            self.topn_spin.config(state='normal')
            self.start_spin.config(state='disabled')
            self.end_spin.config(state='disabled')
        elif mode == 'Range':
            self.topn_spin.config(state='disabled')
            self.start_spin.config(state='normal')
            self.end_spin.config(state='normal')
        else:
            self.topn_spin.config(state='disabled')
            self.start_spin.config(state='disabled')
            self.end_spin.config(state='disabled')

    def _load_default_or_choose(self):
        path = self.DEFAULT_CSV if os.path.exists(self.DEFAULT_CSV) else None
        if not path:
            path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:
            return
        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror("Error", "Failed to load CSV:\n"+str(e))
            return

        df = self._prepare_dataframe(df)
        self.df = df.sort_values('Rank') if 'Rank' in df.columns else df
        self.file_label.config(text=os.path.basename(path), foreground="black")
        self.status.config(text=f"✅ Loaded {len(self.df)} countries.")
        total = len(self.df)
        self.topn_spin.config(to=total)
        self.start_spin.config(to=total)
        self.end_spin.config(to=total)
        self._show_placeholder()

    def _prepare_dataframe(self, df):
        df = df.copy()
        if 'Population (2024)' in df.columns:
            df[self.population_col] = df['Population (2024)'].str.replace(',', '').astype(int)
        elif 'Population' in df.columns:
            df[self.population_col] = pd.to_numeric(df['Population'].str.replace(',', ''), errors='coerce')
        else:
            raise KeyError("Population column not found.")
        if 'Rank' in df.columns:
            df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        return df

    def _show_placeholder(self):
        self._clear_plot()
        lbl = ttk.Label(self.plot_frame, text="📈 Load data & select chart to visualize.", font=('Segoe UI', 14), foreground='gray')
        lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _clear_plot(self):
        for w in self.plot_frame.winfo_children():
            w.destroy()

    def _embed(self, fig):
        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _get_subset(self):
        if self.df is None:
            return None
        mode = self.mode_var.get()
        if mode == 'All':
            return self.df
        if mode == 'Top N':
            return self.df.head(self.topn_var.get())
        start, end = self.start_var.get(), self.end_var.get()
        if start < 1 or end < start or end > len(self.df):
            messagebox.showwarning("Invalid Range", "Please ensure 1 ≤ start ≤ end ≤ total countries.")
            return None
        return self.df.iloc[start-1:end]

    def _plot_pie(self):
        subset = self._get_subset()
        if subset is None:
            return
        fig, ax = plt.subplots(figsize=(6,6))
        colors = plt.cm.tab20.colors
        ax.pie(subset[self.population_col], labels=subset['Country'], autopct='%1.1f%%', startangle=140, colors=colors)
        ax.set_title("🌍 Population Share")
        ax.axis('equal')
        self._display(fig)

    def _plot_bar(self):
        subset = self._get_subset()
        if subset is None:
            return
        fig, ax = plt.subplots(figsize=(8,5))
        bars = ax.bar(subset['Country'], subset[self.population_col], color=plt.cm.viridis(range(len(subset))))
        ax.set_xticklabels(subset['Country'], rotation=45, ha='right')
        ax.set_ylabel("Population")
        ax.set_title("📊 Population by Country")
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"{int(b.get_height()):,}", ha='center', va='bottom')
        fig.tight_layout()
        self._display(fig)

    def _plot_hbar(self):
        subset = self._get_subset()
        if subset is None:
            return
        fig, ax = plt.subplots(figsize=(8,5))
        bars = ax.barh(subset['Country'], subset[self.population_col], color=plt.cm.plasma(range(len(subset))))
        ax.set_xlabel("Population")
        ax.set_title("📈 Population by Country")
        max_val = max(subset[self.population_col])
        for b in bars:
            ax.text(b.get_width() + max_val * 0.01, b.get_y() + b.get_height()/2, f"{int(b.get_width()):,}", va='center')
        fig.tight_layout()
        self._display(fig)

    def _plot_hist(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Load data first.")
            return
        fig, ax = plt.subplots(figsize=(8,5))
        ax.hist(self.df[self.population_col], bins=30, color="#3f51b5", edgecolor="white")
        ax.set_xlabel("Population")
        ax.set_ylabel("Number of Countries")
        ax.set_title("📚 Population Distribution")
        fig.tight_layout()
        self._display(fig)

    def _plot_scatter(self):
        if self.df is None or 'Rank' not in self.df.columns:
            messagebox.showwarning("No Data", "Load data with 'Rank' column.")
            return
        fig, ax = plt.subplots(figsize=(8,5))
        scatter = ax.scatter(self.df['Rank'], self.df[self.population_col], c=self.df['Rank'], cmap='coolwarm')
        ax.set_xlabel("Rank")
        ax.set_ylabel("Population")
        ax.set_title("🎯 Population vs. Rank")
        ax.invert_xaxis()
        fig.tight_layout()
        self._display(fig)

    def _display(self, fig):
        self._clear_plot()
        self._embed(fig)

if __name__ == "__main__":
    app = PopulationVisualizer()
    app.mainloop()