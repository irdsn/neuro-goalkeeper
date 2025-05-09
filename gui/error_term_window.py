##################################################################################################
#                                    ERROR TERM EVOLUTION WINDOW                                 #
#                                                                                                #
# Displays the evolution of the error term throughout training epochs.                           #
# Includes scrollable display of values and matplotlib graph.                                    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Button, RIGHT, Y, BOTH, LEFT, END
import matplotlib.pyplot as plt

##################################################################################################
#                                 ERROR TERM WINDOW CLASS                                        #
#                                                                                                #
# Handles parsing and display of the ANN's error term over training epochs.                      #
# Offers both textual data and a graph using matplotlib.                                         #
##################################################################################################

class ErrorTermWindow(tk.Frame):

    def __init__(self, parent, controller, error_lines, **kwargs):
        super().__init__(parent)
        self.controller = controller
        self.return_to = kwargs.get("return_to")  # reference to previous frame, passed explicitly

        Label(self, text="\nERROR TERM EVOLUTION\n", font=('Helvetica', 24, 'bold')).pack(fill=BOTH)

        Label(
            self,
            text=" # The error term measures the difference between predicted and expected outputs\n"
                 " # It adjusts neuron weights at every training epoch.",
            font=('Helvetica', 20),
            anchor="w",
            justify="left"
        ).pack(fill=BOTH)

        # Scrollable listbox for error values
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(
            self,
            font=('Helvetica', 15),
            yscrollcommand=scrollbar.set,
            selectborderwidth=2
        )

        for line in error_lines:
            if "ERROR TERM EVOLUTION" in line:
                continue
            listbox.insert(END, line.strip())

        listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Extract float values from error lines
        error_values = []
        epochs = []

        for line in error_lines:
            if '>>epoch' in line and 'error=' in line:
                try:
                    # Ejemplo de línea: >>epoch=0, error=3.278
                    parts = line.strip().replace('>>epoch=', '').split(', error=')
                    epoch = int(parts[0])
                    error = float(parts[1])
                    epochs.append(epoch)
                    error_values.append(error)
                except (IndexError, ValueError):
                    continue

        # Plotting
        def show_graph():
            fig = plt.figure("Error Term Evolution", figsize=(9, 7))
            plt.plot(epochs, error_values, marker='o')
            plt.xlabel("Epoch", fontsize=12)
            plt.ylabel("Error Term", fontsize=12)
            plt.title("ERROR TERM EVOLUTION\n", fontsize=24)
            plt.grid(True)
            plt.tight_layout()
            fig.show()

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text="Show Graph",
            command=show_graph,
            font=('Helvetica', 20),
            width=15
        ).pack(side=LEFT, padx=20)

        Button(
            button_frame,
            text="Back",
            command=lambda: self.controller.frames[self.return_to].tkraise(),
            width=14,
            font=('Helvetica', 20)
        ).pack(side=LEFT, padx=20)
