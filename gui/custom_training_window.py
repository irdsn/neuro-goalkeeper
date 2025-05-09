##################################################################################################
#                                 CUSTOM TRAINING SCREEN (SHOOTING)                              #
#                                                                                                #
# Allows the user to simulate personalized shots by clicking goal zones.                         #
# Each click generates a realistic training pattern and adds it to the dataset.                  #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from tkinter import Label, Button, messagebox, Canvas
import random
from PIL import Image, ImageTk
from gui.dataset_view_window import DatasetViewWindow
from utils.paths import resource_path

##################################################################################################
#                                  CUSTOM TRAINING WINDOW CLASS                                  #
#                                                                                                #
# Displays a goal image and lets the user simulate shots in specific zones.                      #
# Generated patterns include: distance, speed, (x, y), and expected outcome.                     #
##################################################################################################

class CustomTrainingWindow(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.dataset = []

        # Load original image and store for scaling
        self.original_image = Image.open(resource_path("images/goal_axes.png"))
        self.image_width, self.image_height = self.original_image.size

        # Canvas for dynamic background
        self.canvas = Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.tk_image = None
        self.button_refs = {}

        # Bind resize event to redraw
        self.canvas.bind("<Configure>", self.redraw)

        # Labels
        self.info_label = Label(self, text="SHOOT AT THE GOAL!", font=('Helvetica', 24, 'bold'))
        self.info_label.place(relx=0.5, rely=0.03, anchor="n")

        self.zone_label = Label(self, font=('Helvetica', 17, 'bold'), width=25, anchor="w")
        self.zone_label.place(relx=0.02, rely=0.95, anchor="w")

        self.pattern_label = Label(self, font=('Helvetica', 17, 'bold'), width=45, anchor="w")
        self.pattern_label.place(relx=0.35, rely=0.95, anchor="w")

        # Continue button
        self.continue_button = Button(
            self,
            text="Continue",
            command=self.continue_to_dataset,
            width=16,
            height=1,
            font=('Helvetica', 20)
        )
        self.continue_button.place(relx=0.95, rely=0.97, anchor="se")

        # Button definitions relative to original image (x%, y%)
        self.button_positions = {
            "TOP LEFT": (0.15, 0.10),
            "TOP CENTER": (0.50, 0.10),
            "TOP RIGHT": (0.85, 0.10),
            "LEFT": (0.15, 0.50),
            "CENTER": (0.50, 0.50),
            "RIGHT": (0.85, 0.50),
            "BOTTOM LEFT": (0.15, 0.90),
            "BOTTOM CENTER": (0.50, 0.90),
            "BOTTOM RIGHT": (0.85, 0.90),
        }

        for label in self.button_positions:
            btn = Button(
                self,
                text=label,
                command=lambda zone=label: self.add_shot(zone),
                width=14,
                font=('Helvetica', 20, 'bold')
            )
            self.button_refs[label] = btn
            btn.place(x=0, y=0)  # Temporarily

    def redraw(self, event):
        """ Redraw image and reposition buttons. """
        # Reserve margins for top and bottom space
        margin_top_ratio = 0.08
        margin_bottom_ratio = 0.12
        available_height = int(event.height * (1 - margin_top_ratio - margin_bottom_ratio))
        offset_y = int(event.height * margin_top_ratio)

        # Resize and draw image within central area
        resized = self.original_image.resize((event.width, available_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.create_image(0, offset_y, image=self.tk_image, anchor="nw")

        # Reposition buttons
        for label, (relx, rely) in self.button_positions.items():
            abs_x = int(relx * event.width)
            abs_y = int(rely * available_height) + offset_y
            self.button_refs[label].place(x=abs_x, y=abs_y, anchor="center")

    def add_shot(self, zone):
        """
        Simulates a shot to a specific goal zone, generating a realistic pattern.
        """
        x_range, y_range = self.get_zone_coordinates(zone)

        distance = round(random.uniform(6.90, 10.50), 2)
        speed = round(random.uniform(85, 110), 2)
        x = round(random.uniform(*x_range), 2)
        y = round(random.uniform(*y_range), 2)
        expected = random.choice([0, 1])

        pattern = [str(distance), str(speed), str(x), str(y), str(expected)]
        self.dataset.append(pattern)

        self.zone_label.config(text=f"Shot to: {zone}")
        self.pattern_label.config(text=f"Pattern: {pattern}")

    def get_zone_coordinates(self, zone):
        """
        Returns the (x_range, y_range) of the goal zone to randomize shot position.
        """
        if zone == "TOP LEFT":
            return (0.00, 1.05), (1.39, 2.08)
        elif zone == "TOP CENTER":
            return (1.05, 2.11), (1.39, 2.08)
        elif zone == "TOP RIGHT":
            return (2.11, 3.16), (1.39, 2.08)
        elif zone == "LEFT":
            return (0.00, 1.05), (0.70, 1.39)
        elif zone == "CENTER":
            return (1.05, 2.11), (0.70, 1.39)
        elif zone == "RIGHT":
            return (2.11, 3.16), (0.70, 1.39)
        elif zone == "BOTTOM LEFT":
            return (0.00, 1.05), (0.00, 0.70)
        elif zone == "BOTTOM CENTER":
            return (1.05, 2.11), (0.00, 0.70)
        elif zone == "BOTTOM RIGHT":
            return (2.11, 3.16), (0.00, 0.70)

    def continue_to_dataset(self):
        """
        Proceed to the dataset view if enough shots have been created.
        """
        if len(self.dataset) < 2:
            messagebox.showerror("ERROR", "Please shoot at least twice before continuing.")
        else:
            self.controller.show_frame(DatasetViewWindow, dataset=self.dataset, dataset_path="custom_generated")

