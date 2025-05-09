##################################################################################################
#                                   NEUROGOALKEEPER MAIN APP                                     #
#                                                                                                #
# Entry point of the application.                                                                #
# Sets up the root Tkinter window and manages screen transitions.                                #
#                                                                                                #
# Author: Íñigo Rodríguez Sánchez                                                                #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import tkinter as tk
from gui.start_window import StartWindow

##################################################################################################
#                                     MAIN APPLICATION CLASS                                     #
#                                                                                                #
# Main application class.                                                                        #
# Initializes the main window and handles switching between frames (views).                      #
##################################################################################################

class NeuroGoalkeeperApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("NeuroGoalkeeper")

        # --- Open in full screen ---
        self.attributes("-fullscreen", True)  # Fullscreen
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))  # Allow exit with Esc

        # --- Alternative: maximize window without fullscreen ---
        # self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        self.resizable(False, False)

        # --- Main container ---
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- Frame manager ---
        self.frames = {}  # Store active frames by class name
        self.show_frame(StartWindow)
    def show_frame(self, frame_class, *args, **kwargs):
        """
        Displays the given frame by creating it if not already created.
        Reuses it otherwise to allow returning to previous states.
        """
        if frame_class not in self.frames:
            frame = frame_class(parent=self.container, controller=self, *args, **kwargs)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            # --- SAVE REFERENCE FOR RETURN PATHS (e.g., from PredictionsWindow) ---
            if frame_class.__name__ == "ResultsWindow":
                self.results_window_class = frame_class
        else:
            frame = self.frames[frame_class]

        frame.tkraise()

##################################################################################################
#                                      APPLICATION LAUNCHER                                      #
#                                                                                                #
# Entry point for launching the NeuroGoalkeeper interface.                                       #
##################################################################################################

if __name__ == "__main__":
    print("[INFO] NeuroGoalkeeper program starting...")
    app = NeuroGoalkeeperApp()
    app.mainloop()
    print("[INFO] NeuroGoalkeeper program finished...")