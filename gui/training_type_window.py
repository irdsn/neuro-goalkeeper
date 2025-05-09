##################################################################################################
#                                  TRAINING TYPE SELECTION SCREEN                                #
#                                                                                                #
# This screen lets the user choose the type of goalkeeper training:                              #
# - General: full coverage with 84 pre-defined shots                                             #
# - External: uses patterns from a user-supplied CSV file                                        #
# - Custom: allows manual generation of patterns by clicking on goal areas                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Button, messagebox
from utils.paths import resource_path
from gui.custom_training_window import CustomTrainingWindow
from gui.dataset_view_window import DatasetViewWindow
from ann import neural_network

##################################################################################################
#                                   TRAINING TYPE WINDOW CLASS                                   #
#                                                                                                #
# Displays training mode options and allows the user to choose how to continue.                  #
##################################################################################################

class TrainingTypeWindow(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(1, weight=1)

        # --- Intro ---
        Label(self, text="\nSELECT TRAINING TYPE\n", font=('Helvetica', 24, 'bold')).grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

        # --- General Training Option ---
        Label(self, text=" GENERAL", font=('Helvetica', 20, 'bold'), anchor="w").grid(row=1, column=0, sticky="new")
        self.general_desc = Label(self,
                                  text="Includes 84 shots distributed evenly across the full goal area. This mode is ideal for assessing the goalkeeper's overall skill level, identifying weak spots, and monitoring performance evolution over time. All shots follow a consistent distribution to ensure full area coverage.\n\n- Avg. Distance: 7 (m)   – Avg. Speed: 90 (km/h)",
                                  font=('Helvetica', 18), justify="left", anchor="w", wraplength=1200)
        self.general_desc.grid(row=2, column=0, sticky="new", pady=10)

        # --- External Training Option ---
        Label(self, text=" EXTERNAL", font=('Helvetica', 20, 'bold'), anchor="w").grid(row=3, column=0, sticky="new")
        self.external_desc = Label(self,
                                   text="Loads shot sequences from a custom CSV file (`dataset_external.csv`). This mode is intended for advanced users who want to simulate specific training patterns or reproduce real match data. Full control is available over each shot parameter:\n\n- x in [0, 3.16] m     y in [0, 2.08] m     Distance in [7, 10] m     Speed in [85, 110] km/h\n\n* Note: Incorrect or unrealistic values may lead to unexpected behavior or unrepresentative results.",
                                   font=('Helvetica', 18), justify="left", anchor="w", wraplength=1200)
        self.external_desc.grid(row=4, column=0, sticky="new", pady=10)

        # --- Custom Training Option ---
        Label(self, text=" CUSTOM", font=('Helvetica', 20, 'bold'), anchor="w").grid(row=5, column=0, sticky="new")
        self.custom_desc = Label(self,
                                 text="Enables the user to manually select goal areas for personalized goalkeeper training. Shot positions and trajectories are generated based on the selected zone, simulating realistic but randomized attack patterns within that area. This mode helps focus training on specific weaknesses or tactical scenarios.\n\n- Randomized distance in [6.90, 10.50] m     Speed in [85, 110] km/h",
                                 font=('Helvetica', 18), justify="left", anchor="w", wraplength=1200)
        self.custom_desc.grid(row=6, column=0, sticky="new", pady=10)

        Label(self, text=" * Shots are always taken from a frontal position.\n\n", font=('Helvetica', 18), anchor="w").grid(row=8, column=0, columnspan=2, sticky="w")

        # --- Buttons ---
        Button(self, text="Select", font=('Helvetica', 20), width=20, command=self.load_general).grid(row=2, column=1, sticky="n", padx=25, pady=(10, 20))

        Button(self, text="Select", font=('Helvetica', 20), width=20, command=self.load_external).grid(row=4, column=1, sticky="n", padx=25, pady=(10, 20))

        Button(self, text="Select", font=('Helvetica', 20), width=20,  command=self.load_custom).grid(row=6, column=1, sticky="n", padx=25, pady=(10, 20))

        # Allow columns to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Allow rows to expand
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

    def load_general(self):
        messagebox.showinfo("TRAINING", "General training selected.")
        dataset_path = resource_path("datasets/dataset_general.csv")
        dataset = neural_network.load_csv(dataset_path)
        self.controller.show_frame(DatasetViewWindow, dataset=dataset, dataset_path=dataset_path)

    def load_external(self):
        messagebox.showinfo("TRAINING", "External training selected.")
        dataset_path = resource_path("datasets/dataset_external.csv")
        dataset = neural_network.load_csv(dataset_path)
        self.controller.show_frame(DatasetViewWindow, dataset=dataset, dataset_path=dataset_path)

    def load_custom(self):
        messagebox.showinfo("TRAINING", "Custom training selected.")
        self.controller.show_frame(CustomTrainingWindow)
