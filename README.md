## Population Visualization

A desktop GUI application for exploring and visualizing country-level population data from a CSV file. Users can load their own dataset or use the default `World Population Data.csv`, then generate pie charts, bar charts, histograms, and scatter plots for Top N, ranked ranges, or all countries.

---

## Features

* **Load CSV**

  * Load the default CSV at `DEFAULT_CSV` or pick any CSV file via standard file dialog
* **Mode Selection**

  * **Top N**: visualize only the top N countries by population
  * **Range**: visualize a custom rank range (start–end)
  * **All**: include every country in the dataset
* **Chart Types**

  * **Pie Chart**: population share per country
  * **Vertical Bar**: population values with data labels
  * **Horizontal Bar**: population values with data labels
  * **Histogram**: distribution of country populations
  * **Scatter Plot**: population vs. rank (inverted x-axis)
* **Status Bar**

  * Displays “✅ Ready” or “✅ Loaded X countries.” messages at the bottom

---

## Requirements

* Python 3.7+
* Tkinter (built-in with most Python installs)
* pandas ≥ 1.0.0
* matplotlib ≥ 3.0.0

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Monish21072004/Population-Visualization.git
   cd Population-Visualization
   ```
2. **Install dependencies**

   ```bash
   pip install pandas matplotlib
   ```

   *(Tkinter is included with standard Python distributions.)*

---

## Usage

1. **Run the application**

   ```bash
   python data.py
   ```
2. **Load your data**

   * Click **Load CSV** and select a CSV file containing at least a `Country` column and a `Population` column
3. **Select mode & parameters**

   * Choose **Top N**, **Range**, or **All**, and adjust the spinboxes as needed
4. **Generate charts**

   * Click the desired chart button (Pie, Vertical Bar, Horizontal Bar, Histogram, Scatter) to display the plot in the right panel

---

## File Structure

```
Population-Visualization/
├── data.py              # Main tkinter GUI application
├── Dataset/             # (Optional) sample CSV files
├── LICENSE              # GPL-3.0 License
└── README.md            # This file
```

---

## Contributing

1. Fork the repository
2. Create a branch (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m "Add new visualization"`)
4. Push to your branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the [GPL-3.0](LICENSE) license.
