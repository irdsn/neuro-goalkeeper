# NeuroGoalkeeper Architecture

## Project Structure

```bash
neuro-goalkeeper/
├── ann/                                         # ANN logic and training process (forward/backward propagation, training loop)
│   └── neural_network.py
│
├── datasets/                                    # CSV datasets used as input for training
│   ├── dataset_external.csv
│   └── dataset_general.csv
│
├── docs/
│   ├── images/                                  # Images used only for project documentation
│   │   ├── start_window.png
│   │   ├── training_type_window.png
│   │   └── shot_map.png
│   └── ARCHITECTURE.md
│
├── gui/                                         # Tkinter-based GUI modules for all application screens
│   ├── custom_training_window.py
│   ├── dataset_view_window.py
│   ├── error_term_window.py
│   ├── parameter_selection_window.py
│   ├── predictions_window.py
│   ├── results_window.py
│   ├── start_window.py
│   ├── stats_window.py
│   └── training_type_window.py
│
├── images/                                      # Static visual assets
│   ├── goal_axes.png                            # Goal interface for custom training
│   └── ann_structure.GIF                        # Architecture diagram shown in start window
│
├── outputs/                                     # Training session results and exported artifacts
│   ├── training_summary.txt                     # Full ANN output from last session
│   ├── training_report_YYYYMMDD_HHMMSS.md       # Markdown training report (auto-generated)
│   ├── Error_Term_Evolution_YYYYMMDD_HHMMSS.png # Error plot (auto-generated)
│   └── Shot_Map_YYYYMMDD_HHMMSS.png             # Shot coordinates visualization (auto-generated)
│
├── utils/                                       # Utility modules used throughout the app
│   └── paths.py                                 # Path resolution utilities
│
├── neuro_goalkeeper.py                                       # Main application launcher
├── requirements.txt                             # Python dependencies
├── .gitignore                                   # Ignored files and folders
└── README.md                                    # Project documentation
```

## Script Overview

| File                                | Description                                                                                                    |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `neuro_goalkeeper.py`               | Main launcher of the application; handles window transitions and fullscreen behavior                           |
| `ann/neural_network.py`             | Full implementation of the artificial neural network and training logic                                        |
| `gui/custom_training_window.py`     | Interactive shot generation interface using goal layout                                                        |
| `gui/dataset_view_window.py`        | Displays selected dataset before training                                                                      |
| `gui/error_term_window.py`          | Graph of error term evolution during training                                                                  |
| `gui/parameter_selection_window.py` | Collects ANN hyperparameters from the user                                                                     |
| `gui/predictions_window.py`         | Lists ANN predictions with input and output values                                                             |
| `gui/results_window.py`             | Shows training log, predictions, and access to graphs                                                          |
| `gui/start_window.py`               | Initial project description screen and ANN summary                                                             |
| `gui/stats_window.py`               | Final performance metrics                                                                                      |
| `gui/training_type_window.py`       | Mode selection window (general, external, custom)                                                              |
| `utils/paths.py`                    | Provides project-root-relative file resolution to reliably load datasets and images from any script or module. |
