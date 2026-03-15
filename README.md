# NeuroGoalkeeper: ANN-Based Training Simulator for Handball Goalkeepers

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Model](https://img.shields.io/badge/Model-Feedforward_ANN-blueviolet)
![Task](https://img.shields.io/badge/Task-Binary_Classification-orange)
![Last Updated](https://img.shields.io/badge/Last%20Updated-March%202026-brightgreen)

Simulated training environment for handball goalkeepers powered by a custom-built artificial neural network and an interactive Tkinter GUI. Originally developed as a bachelor thesis and later refined into a standalone application.

## Table of Contents

- [Introduction](#introduction)
- [Documentation](#documentation)
- [Key Features](#key-features)
- [Interface Overview](#interface-overview)
- [Refactor Overview](#refactor-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Important Notes](#important-notes)
- [Final Words](#final-words)

## Introduction

NeuroGoalkeeper is a modular training simulator for handball goalkeepers based on a custom-built artificial neural network (ANN). The system simulates goalkeeper responses to various shot patterns and learns from those interactions over multiple epochs.

Developed originally as an academic project, the application integrates data preprocessing, ANN logic, and visual interaction via a Tkinter-based interface. The training process is entirely self-contained: shot patterns are either loaded from a dataset or generated interactively, then normalized and used to train the ANN.

The project serves both as a pedagogical tool for neural network understanding and as a practical simulation platform for sports-oriented machine learning experimentation.

> This project was initially developed as a Bachelor Thesis at Universidad Politécnica de Madrid (UPM).  
> Official repository: [https://oa.upm.es/62850/](https://oa.upm.es/62850/)

## Documentation

Additional technical documentation is available in the `/docs` directory.

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**  
  Provides a detailed overview of the repository structure, application modules, and the role of each script within the NeuroGoalkeeper simulator.

This document explains how the project is organized and how the different components interact within the ANN training environment.

## Key Features

- Artificial neural network implemented from scratch and adapted for this simulator  
  > Core ANN logic originally based on a tutorial by Jason Brownlee, further extended and integrated into the full system.  
  > 📄 Source: [https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/](https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/)
- Simulated training environment for handball goalkeepers
- Three training modes: General, External (CSV-based), and Custom (interactive goal shooting)
- Clean and modular code structure with dedicated folders for GUI, ANN logic, and assets
- Full English translation of codebase and UI texts
- In-app training log viewer with scrollable and readable formatting
- Markdown training reports generated alongside raw `.txt` logs
- Timestamped training reports to preserve session history and avoid overwrites
- Dynamic GUI with improved layout and fullscreen support

## Interface Overview

Below are sample views of the application's interface and output visualizations:

| Initial Overview                                       |
|--------------------------------------------------------|
| <img src="docs/images/start_window.png" width="900"/>  |

| Training Type Selection                                       |
|---------------------------------------------------------------|
| <img src="docs/images/training_type_window.png" width="900"/> |

| Example Shot Map Output                              |
|------------------------------------------------------|
| <img src="docs/images/shot_map.png" width="900"/>    |

## Refactor Overview

This project is an extended and cleaned-up version of the original Bachelor's Thesis implementation. Key improvements include:

| Area                 | Original (TFG)                                | Current Version                                       |
|----------------------|-----------------------------------------------|-------------------------------------------------------|
| Interface Language   | Mixed (Spanish + English)                     | Fully in English                                      |
| Code Structure       | Monolithic, low modularity                    | Modular design with separate folders per component    |
| ANN Logic            | Embedded in single script                     | Isolated in its own module with improved logging      |
| Output Format        | Plain `.txt` log only                         | `.txt` + auto-generated `.md` report                  |
| Custom Training      | Present but visually inconsistent             | Fully refactored with dynamic button layout           |
| Dataset Handling     | Fixed logic, hardcoded paths                  | Robust path handling via `utils/paths.py`             |
| UI Design            | Fixed window sizes, limited responsiveness    | Fullscreen support, consistent layout across screens  |

These changes improve usability, maintainability, and adaptability for future enhancements.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/neuro-goalkeeper.git
cd neuro-goalkeeper
```

2. (Optional but recommended) Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Once installed, you can launch the application with:

```bash
python neuro_goalkeeper.py
```

This will open a graphical interface where you can select a training mode, configure the ANN parameters, and view training results and visualizations.

All outputs will be saved under the /outputs/ directory, including:

- training_summary.txt: full training log
- training_report.md: Markdown version of the training summary
- Plots and prediction visualizations

## Important Notes

- The application is designed for educational and experimental purposes; its ANN is not optimized for production-grade performance.
- All datasets must follow the expected CSV format with five columns: Distance, Speed, X, Y, and Expected Output.
- The ANN expects numeric inputs only. Incorrect formatting may lead to parsing errors.
- The `Custom Training` mode requires at least two simulated shots before continuing.
- If run outside the project root, some paths (e.g. to `/images` or `/datasets`) may fail unless properly adjusted.


## Contributing & Contact

This project was originally developed as part of a *Bachelor Thesis in Telecommunications Engineering* at Universidad Politécnica de Madrid, and later evolved into a standalone ANN-based simulator.

Whether you're a student exploring neural networks, a developer interested in sports simulations, or simply curious about machine learning from scratch, I hope this project offers value and insight.

Feel free to explore the code, test the different training modes, or adapt the project to new use cases.

**If you’ve found this project useful or inspiring — feel free to build on it, break it, or just drop a star ⭐.**

- Bugs / feature requests: please open an **Issue**.
- Direct contact: [inigo.rodsan@gmail.com](mailto:inigo.rodsan@gmail.com)

Developed & maintained by [Íñigo Rodríguez](https://github.com/irdsn).
