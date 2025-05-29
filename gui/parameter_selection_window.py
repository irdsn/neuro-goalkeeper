##################################################################################################
#                              ANN PARAMETER CONFIGURATION SCREEN                                #
#                                                                                                #
# Allows the user to input training parameters for the ANN:                                      #
# - Number of hidden neurons                                                                     #
# - Learning rate                                                                                #
# - Number of epochs                                                                             #
# Constant parameters (input/output neurons) are pre-filled and locked.                          #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, messagebox
from gui.results_window import ResultsWindow

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class ParameterSelectionWindow(tk.Frame):
    """
    GUI window for configuring the training parameters of the artificial neural network (ANN).

    This window allows the user to specify:
    - Number of neurons in the hidden layer
    - Learning rate
    - Number of training epochs

    It also displays fixed input/output neuron information based on dataset characteristics.

    Attributes:
        controller (tk.Tk): Main application controller for screen transitions.
        dataset (list): List of input patterns to be used for training.
        dataset_path (str): Optional path to the dataset source.
    """

    def __init__(self, parent, controller, dataset, dataset_path=None):
        super().__init__(parent)
        self.controller = controller
        self.dataset = dataset
        self.dataset_path = dataset_path

        # --- Main title ---
        Label(self, text="ARTIFICIAL NEURAL NETWORK PARAMETERS", font=('Helvetica', 24, 'bold')) \
            .grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

        Label(self, text="Please specify the parameters to configure the neural network training process:\n",
              font=('Helvetica', 20), anchor="w") \
            .grid(row=1, column=0, columnspan=2, sticky="w")

        # --- Hidden layer neurons ---
        Label(self, text=" HIDDEN LAYER NEURONS", font=('Helvetica', 20, 'bold'), anchor="w") \
            .grid(row=2, column=0, sticky="new")
        self.hidden_desc = Label(self,
                                 text="Defines the number of neurons in the hidden layer. Affects the network’s ability to capture non-linear relationships.\n\nTypical values: 2, 3, 4.",
                                 font=('Helvetica', 18), justify="left", anchor="w")
        self.hidden_desc.grid(row=3, column=0, sticky="new", pady=10)
        self.entry_hidden = Entry(self, font=('Helvetica', 24, 'bold'), justify="center")
        self.entry_hidden.grid(row=3, column=1, sticky="n", padx=25)

        # --- Learning rate ---
        Label(self, text=" LEARNING RATE", font=('Helvetica', 20, 'bold'), anchor="w") \
            .grid(row=4, column=0, sticky="new")
        self.rate_desc = Label(self,
                               text="Controls the adjustment speed of the model's weights during training. Lower values train slower but more precisely.\n\nTypical values: 0.3, 0.5, 0.8.",
                               font=('Helvetica', 18), justify="left", anchor="w")
        self.rate_desc.grid(row=5, column=0, sticky="new", pady=10)
        self.entry_rate = Entry(self, font=('Helvetica', 24, 'bold'), justify="center")
        self.entry_rate.grid(row=5, column=1, sticky="n", padx=25)

        # --- Epochs ---
        Label(self, text=" EPOCHS", font=('Helvetica', 20, 'bold'), anchor="w") \
            .grid(row=6, column=0, sticky="new")
        self.epochs_desc = Label(self,
                                 text="Number of times the full training dataset is passed through the network. More epochs generally mean better learning.\n\nTry: 100, 1000, 10000.",
                                 font=('Helvetica', 18), justify="left", anchor="w")
        self.epochs_desc.grid(row=7, column=0, sticky="new", pady=10)
        self.entry_epochs = Entry(self, font=('Helvetica', 24, 'bold'), justify="center")
        self.entry_epochs.grid(row=7, column=1, sticky="n", padx=25)

        # --- Fixed parameters info ---
        Label(self, text="The following parameters are fixed:", font=('Helvetica', 20)) \
            .grid(row=8, column=0, columnspan=2, sticky="w", pady=(20, 10))

        # --- Input neurons ---
        Label(self, text=" INPUT NEURONS", font=('Helvetica', 20, 'bold'), anchor="w") \
            .grid(row=9, column=0, sticky="new")
        self.input_desc = Label(self,
                                text="Determined by the dataset structure. Each input neuron receives one feature from a shot pattern.",
                                font=('Helvetica', 18), justify="left", anchor="w")
        self.input_desc.grid(row=10, column=0, sticky="new", pady=10)
        self.entry_inputs = Entry(self, font=('Helvetica', 24, 'bold'), justify="center", state="normal")
        self.entry_inputs.insert(0, str(len(self.dataset[0]) - 1))
        self.entry_inputs.config(state="readonly")
        self.entry_inputs.grid(row=10, column=1, sticky="n", padx=25)

        # --- Output neurons ---
        Label(self, text=" OUTPUT NEURONS", font=('Helvetica', 20, 'bold'), anchor="w") \
            .grid(row=11, column=0, sticky="new")
        self.output_desc = Label(self,
                                 text="Fixed to 2. Represents the two possible goalkeeper responses (e.g. stop vs. goal).",
                                 font=('Helvetica', 18), justify="left", anchor="w")
        self.output_desc.grid(row=12, column=0, sticky="new", pady=10)
        self.entry_outputs = Entry(self, font=('Helvetica', 24, 'bold'), justify="center", state="normal")
        self.entry_outputs.insert(0, "2")
        self.entry_outputs.config(state="readonly")
        self.entry_outputs.grid(row=12, column=1, sticky="n", padx=25)

        # --- Continue Button ---
        Button(self, text="Continue", command=self.validate_and_start, font=('Helvetica', 20), width=20) \
            .grid(row=13, column=1, pady=30)

        # --- Expansión para grid ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(14):
            self.grid_rowconfigure(i, weight=1)

    def validate_and_start(self):
        """
        Validate user-provided ANN parameters and launch the training results screen.

        Validates that:
        - Hidden layer neurons is a positive integer
        - Learning rate is a float between 0 and 1
        - Epochs is a positive integer

        On success, navigates to the ResultsWindow with the collected parameters and dataset.
        On error, shows an error message prompting the user to correct the inputs.
        """

        try:
            if not self.entry_hidden.get() or not self.entry_rate.get() or not self.entry_epochs.get():
                raise ValueError("Missing fields.")

            n_hidden = int(self.entry_hidden.get())
            l_rate = float(self.entry_rate.get())
            n_epoch = int(self.entry_epochs.get())

            if n_hidden <= 0 or not (0 < l_rate <= 1) or n_epoch <= 0:
                raise ValueError("Invalid parameter values.")

            # Launch ANN results view
            self.controller.show_frame(ResultsWindow, n_hidden=n_hidden, l_rate=l_rate, n_epoch=n_epoch, dataset_input=self.dataset, dataset_path=self.dataset_path)

        except ValueError:
            messagebox.showerror(
                "Invalid Parameters",
                "Please enter valid values for all fields:\n"
                "- Hidden neurons: integer > 0\n"
                "- Learning rate: decimal between 0 and 1\n"
                "- Epochs: integer > 0"
            )
