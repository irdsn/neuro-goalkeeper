##################################################################################################
#                                DATASET VIEW SCREEN (PRE-TRAINING)                              #
#                                                                                                #
# Displays the dataset generated or loaded prior to ANN training.                                #
# Shows structure of each pattern and allows user to proceed to parameter selection.             #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Button, RIGHT, BOTH, Y
from gui.parameter_selection_window import ParameterSelectionWindow

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class DatasetViewWindow(tk.Frame):
    """
    A GUI window that displays the input dataset before neural network training.

    This window renders each training pattern in a scrollable list and shows
    the data structure format. It allows users to proceed to the ANN parameter
    selection window once they have reviewed the dataset.

    Attributes:
        controller (tk.Tk): Reference to the main app controller for window navigation.
        dataset (list): List of training patterns to display.
        dataset_path (str): Optional path or label indicating the dataset origin.
    """

    def __init__(self, parent, controller, dataset=None, dataset_path=None):
        super().__init__(parent)
        self.controller = controller
        self.dataset = dataset
        self.dataset_path = dataset_path

        # Header
        Label(self, text="\nINPUT PATTERNS\n", font=('Helvetica', 24, 'bold')).pack(fill=BOTH)
        Label(
            self,
            text=" Pattern structure:    [Distance (m), Speed (km/h), x (m), y (m), Expected Output (0/1)]\n",
            font=('Helvetica', 20, 'bold')
        ).pack(fill=BOTH)

        # Scrollbar and listbox
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(self, font=('Helvetica', 15), yscrollcommand=scrollbar.set, selectborderwidth=2)
        for pattern in dataset:
            listbox.insert(tk.END, str(pattern))
        listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Navigation buttons
        Button(
            self,
            text="Continue",
            command=self.proceed_to_parameters,
            width=20,
            font=('Helvetica', 20)
        ).pack(pady=20)

    def proceed_to_parameters(self):
        """
        Navigates to the ANN parameter selection window.

        Transfers the current dataset and dataset path to the next screen for
        training configuration.
        """

        self.controller.show_frame(ParameterSelectionWindow, dataset=self.dataset, dataset_path=self.dataset_path)
