##################################################################################################
#                                     PREDICTIONS WINDOW                                         #
#                                                                                                #
# Displays the individual predictions made by the trained ANN.                                   #
# Allows access to final statistics from predictions phase.                                      #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Button, RIGHT, Y, BOTH, LEFT, END
from gui.stats_window import StatsWindow

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class PredictionsWindow(tk.Frame):
    """
    GUI window for displaying the predictions made by the trained ANN.

    Shows the prediction results in a scrollable list and provides access to
    final prediction statistics.

    Attributes:
        controller (tk.Tk): The main application controller for screen transitions.
        predictions (list): List of strings representing prediction outcomes.
        stats (dict): Dictionary containing computed statistics for the predictions.
    """

    def __init__(self, parent, controller, predictions, stats, **kwargs):
        super().__init__(parent)
        self.controller = controller
        self.predictions = predictions
        self.stats = stats

        Label(self, text="\nPREDICTIONS MADE BY THE NEURAL NETWORK\n", font=('Helvetica', 24, 'bold')).pack(fill=BOTH)

        # Scrollable prediction list
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(
            self,
            font=('Helvetica', 15),
            yscrollcommand=scrollbar.set,
            selectborderwidth=2
        )

        for line in predictions:
            if 'PREDICTIONS MADE BY THE NEURAL NETWORK' in line:
                continue
            listbox.insert(END, line)

        listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Action buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text="Statistics",
            command=lambda: self.controller.show_frame(
                StatsWindow,
                stats=self.stats,
                predictions=self.predictions,
                return_to=PredictionsWindow
            ),
            font=('Helvetica', 20),
            width=15
        ).pack(side=LEFT, padx=20)

        Button(
            button_frame,
            text="Back",
            command=lambda: self.controller.frames[self.controller.results_window_class].tkraise(),
            width=14,
            font=('Helvetica', 20)
        ).pack(side=LEFT, padx=20)

