##################################################################################################
#                                    STATS WINDOW                                                #
#                                                                                                #
# Displays the final training statistics from the ANN training process.                          #
# Uses a scrollable listbox to show accuracy, success rate, etc.                                 #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Button, RIGHT, Y, BOTH, LEFT, END

##################################################################################################
#                                   STATS WINDOW CLASS                                           #
#                                                                                                #
# Displays all lines classified as final statistics, collected from the training output.         #
# Automatically skips headers and separators.                                                    #
##################################################################################################

class StatsWindow(tk.Frame):

    def __init__(self, parent, controller, stats=None, predictions=None, **kwargs):
        super().__init__(parent)
        self.controller = controller
        self.stats = stats
        self.predictions = predictions

        from gui.predictions_window import PredictionsWindow

        Label(self, text="\nFINAL TRAINING STATISTICS\n", font=('Helvetica', 24, 'bold')).pack(fill=BOTH)

        # Scrollable area
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(
            self,
            font=('Helvetica', 20, 'bold'),
            yscrollcommand=scrollbar.set,
            bg="#000",
            fg="#fff",
            selectborderwidth=2
        )

        for line in self.stats:
            if line.strip() == "FINAL RESULTS:":
                continue
            listbox.insert(END, "\n")
            listbox.insert(END, line.strip())

        listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text="Back",
            command=lambda: self.controller.frames[PredictionsWindow].tkraise(),
            font=('Helvetica', 20),
            width=14
        ).pack(side=LEFT, padx=20)

