##################################################################################################
#                                       ANN TRAINING RESULTS                                     #
#                                                                                                #
# Displays the full training output after ANN training:                                          #
# - Scrollable summary of the output file                                                        #
# - Final statistics shown automatically if present                                              #
# - Optional graph of shot coordinates                                                           #
# - Access to prediction and error term windows                                                  #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Button, RIGHT, Y, BOTH, LEFT, END, W
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import copy
import sys
from ann import neural_network
from gui.predictions_window import PredictionsWindow
from gui.error_term_window import ErrorTermWindow
from gui.stats_window import StatsWindow
import os
from datetime import datetime

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class ResultsWindow(tk.Frame):
    """
    GUI window that displays the complete output of the ANN training process.

    Features:
    - Runs the ANN training process with user-defined parameters.
    - Displays scrollable training logs.
    - Provides access to predictions, error term graph, shot map, and statistics.
    - Automatically exports a structured Markdown report summarizing the session.

    Attributes:
        controller (tk.Tk): The application controller that manages screen transitions.
        n_hidden (int): Number of hidden neurons.
        l_rate (float): Learning rate for training.
        n_epoch (int): Number of training epochs.
        dataset_input (list): List of training patterns.
        dataset_path (str): File path of the training dataset used.
        predictions (list): List of prediction output lines.
        error_lines (list): List of error term evolution lines.
        stats (list): Final evaluation statistics extracted from the training output.
    """

    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent)
        self.controller = controller

        # Extract ANN parameters from kwargs
        self.n_hidden = kwargs.get("n_hidden")
        self.l_rate = kwargs.get("l_rate")
        self.n_epoch = kwargs.get("n_epoch")
        self.dataset_input = kwargs.get("dataset_input")
        self.dataset_path = kwargs.get("dataset_path")

        # --- Defensive check in case any required value is missing ---
        if None in (self.n_hidden, self.l_rate, self.n_epoch, self.dataset_input):
            raise ValueError("[ERROR] Missing ANN parameters for ResultsWindow.")

        Label(self, text="\nTRAINING RESULTS\n", font=('Helvetica', 24, 'bold')).pack(fill=BOTH)
        Label(
            self,
            text=" # Below is the complete output of the training process (saved on /outputs/training_summary.txt):",
            font=('Helvetica', 20),
            anchor=W
        ).pack(fill=BOTH)

        # --- ANN training and results processing ---
        output_file = neural_network.complete_training(self.n_hidden, self.l_rate, self.n_epoch, self.dataset_input)

        full_output = []
        error_lines = []
        self.predictions = []
        stats = []

        with open(output_file, 'r') as f:
            for line in f:
                if '---------' in line:
                    continue
                if 'ERROR TERM EVOLUTION' in line or '>>epoch' in line:
                    error_lines.append(line)
                if 'PREDICTIONS MADE BY THE NEURAL NETWORK' in line or '**VALUES' in line or '--[x,y]:' in line:
                    self.predictions.append(line)
                if 'FINAL RESULTS:' in line or '~' in line:
                    stats.append(line)
                full_output.append(line)


        # Scrollable training summary
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_widget = tk.Text(
            self,
            font=('Helvetica', 15),
            yscrollcommand=scrollbar.set,
            wrap="word"  # Ensures that content is not cut horizontally
        )
        text_widget.pack(fill=BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        for line in full_output:
            text_widget.insert(END, line)


        # --- Save variables as attributes for access from other methods ---
        self.error_lines = error_lines
        self.stats = stats

        # --- Export Markdown version of the report ---
        self.export_markdown_report(output_txt_path=output_file)

        # Buttons for navigation and analysis
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text="Predictions",
            command=lambda: self.controller.show_frame(PredictionsWindow, predictions=self.predictions, stats=self.stats, return_to=ResultsWindow),
            font=('Helvetica', 20),
            width=15
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="Shot Map",
            command=self.show_shot_map,
            font=('Helvetica', 20),
            width=15
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="Error Term",
            command=lambda: self.controller.show_frame(ErrorTermWindow, error_lines=self.error_lines, return_to=ResultsWindow),
            font=('Helvetica', 20),
            width=15
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="Exit",
            command=lambda: sys.exit(),
            width=14,
            font=('Helvetica', 20)
        ).pack(side=RIGHT, padx=10)

        # Auto-launch statistics if present
        if self.stats:
            self.controller.show_frame(StatsWindow, stats=self.stats)

    def show_shot_map(self):
        """
        Generates a matplotlib visualization of shot coordinates over the goal image.

        Shots are colored based on prediction correctness:
        - Blue: Correct prediction
        - Red: Wrong prediction

        Coordinates are rescaled to real dimensions (meters).
        """

        # Plot of launch coordinates
        dataset_for_plot = copy.deepcopy(self.dataset_input)
        predictions = self.predictions  # Helper to extract predictions if needed

        fig = plt.figure("5.2. Shot Map", figsize=(9, 7))
        background = plt.imread("images/goal_axes.png")
        ax = plt.axes([0.08, 0.05, 0.9, 0.9])

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Correct prediction', markerfacecolor='blue',
                   markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Wrong prediction', markerfacecolor='red', markersize=10)
        ]

        for i, pattern in enumerate(dataset_for_plot):
            try:
                x_coord = float(pattern[2]) * 3.16  # Rescale x normalized to meters
                y_coord = float(pattern[3]) * 2.08  # Rescale y normalized to meters
                line = predictions[i]
                predicted = int(line.split("Predicted:")[1].split()[0])
                expected = int(line.split("Expected:")[1].split()[0])
                color = "blue" if expected == predicted else "red"
                ax.scatter(x_coord, y_coord, c=color, marker='o', s=75, alpha=0.7)
            except (IndexError, ValueError):
                continue

        ax.imshow(background, extent=[0, 3.16, 0, 2.08])
        plt.xlim(0, 3.16)
        plt.ylim(0, 2.08)
        plt.xlabel('x (m)', fontsize=12)
        plt.ylabel('y (m)', fontsize=12)
        plt.title('SHOT MAP\n', fontsize=15)
        plt.subplots_adjust(bottom=0.25)
        ax.legend(handles=legend_elements, loc='lower right')
        plt.show()

    def export_markdown_report(self, output_txt_path):
        """
        Creates a structured Markdown training report based on ANN output.

        The report includes:
        - Configuration details
        - Explanation of training modes
        - Raw output from the ANN
        - Final evaluation metrics (if available)

        Args:
            output_txt_path (str): Path to the text file with ANN training results.
        """

        timestamp_slug = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_md_path = f"outputs/training_report_{timestamp_slug}.md"

        # --- Extract dataset name ---
        dataset_name = os.path.basename(self.dataset_path)

        # --- Timestamp ---
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(output_md_path, "w") as f:
            # --- Header ---
            f.write("# 🧠 NeuroGoalkeeper – Training Report\n\n")
            f.write(
                "This document summarizes the results of a goalkeeper training session using an artificial neural network (ANN).  \n")
            f.write("Generated automatically by the **NeuroGoalkeeper** application.\n\n")
            f.write("---\n\n")

            # --- Configuration Section ---
            f.write("## ⚙️ ANN Configuration\n\n")
            f.write(f"- **Hidden neurons**: {self.n_hidden}  \n")
            f.write(f"- **Learning rate**: {self.l_rate}  \n")
            f.write(f"- **Epochs**: {self.n_epoch}  \n")
            f.write(f"- **Training dataset**: `{dataset_name}`  \n")
            f.write(f"- **Timestamp**: {timestamp}  \n\n")
            f.write("---\n\n")

            # --- Explanation Section ---
            f.write("## 🧪 Training Type Explanation\n\n")
            f.write("This ANN was trained using shot data representing goalkeeper responses.  \n")
            f.write(
                "Each pattern includes position (`x`, `y`), distance, and speed. The output represents whether the shot was **stopped** or resulted in a **goal**.\n\n")
            f.write("You can select different training modes in the application:\n\n")
            f.write("- **General**: preloaded dataset with 84 uniformly distributed shots.  \n")
            f.write("- **External**: load your own CSV with custom shots.  \n")
            f.write("- **Custom**: define shots interactively on the goal map.  \n\n")
            f.write("---\n\n")

            # --- Raw Output Section ---
            f.write("## 📊 Raw Training Output\n\n")
            f.write("```text\n")
            with open(output_txt_path, "r") as result_file:
                for line in result_file:
                    f.write(line)
            f.write("```\n\n")

            # --- Final Stats Section (if any) ---
            if self.stats:
                f.write("## 🧾 Final Evaluation Metrics\n\n")
                f.write("```text\n")
                for line in self.stats:
                    f.write(line)
                f.write("```\n\n")

            f.write("---\n")
            f.write("_End of report._\n")
