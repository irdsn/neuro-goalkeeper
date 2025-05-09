##################################################################################################
#                                      START WINDOW (SCREEN 1)                                   #
#                                                                                                #
# Initial welcome screen for the NeuroGoalkeeper application.                                    #
# Displays project and author information and provides access to training modes.                 #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import PhotoImage, Label, Button
from gui.training_type_window import TrainingTypeWindow
from utils.paths import resource_path

##################################################################################################
#                                        START WINDOW CLASS                                      #
#                                                                                                #
# Displays the welcome screen with project credits and a button to start training.               #
##################################################################################################

class StartWindow(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Title and Author Info ---
        Label(self, text="\nFINAL BACHELOR DEGREE PROJECT (v2)\n", font=('Helvetica', 24, 'bold')).pack(fill=tk.BOTH, expand=True)
        Label(self, text=" ~ Author: Íñigo Rodríguez Sánchez\n", font=('Helvetica', 18, 'bold'), anchor="w").pack(fill=tk.BOTH)

        # --- Project Description ---
        Label(self,
              text=" # NeuroGoalkeeper simulates a goalkeeper training system based on real shot patterns and user interaction.",
              font=('Helvetica', 18), anchor="w").pack(fill=tk.BOTH)
        Label(self,
              text=" # The system uses a supervised learning approach powered by an Artificial Neural Network (ANN), which learns to predict the goalkeeper’s response.",
              font=('Helvetica', 18), anchor="w").pack(fill=tk.BOTH)
        Label(self,
              text=" # Users can train the ANN with predefined shot datasets or generate custom ones to adapt the training to specific weaknesses or game strategies.",
              font=('Helvetica', 18), anchor="w").pack(fill=tk.BOTH)
        Label(self,
              text=" # The interface allows users to launch simulations, train the model, and visualize its learning performance over time.",
              font=('Helvetica', 18), anchor="w").pack(fill=tk.BOTH)
        Label(self,
              text=" # The current ANN architecture is composed of a feedforward network with backpropagation, tailored for regression-based output predictions, as follows:",
              font=('Helvetica', 18), anchor="w").pack(fill=tk.BOTH)

        # --- Network Architecture Image ---
        image_path = resource_path("images/ann_structure.GIF")
        image = PhotoImage(file=image_path)
        Label(self, image=image).pack(fill=tk.BOTH, expand=True)
        self.image = image  # Keep reference to avoid garbage collection

        # --- Start Button ---
        Button(
            self,
            text="Start Training!",
            command=lambda: controller.show_frame(TrainingTypeWindow),
            width=36,
            font=('Helvetica', 20, 'bold')
        ).pack(padx=40, pady=20, expand=True)
