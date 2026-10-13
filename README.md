# ALFRED Neutronics and Reactivity Analysis

## Overview
This repository contains the numerical modeling and transport calculation code developed as part of my Bachelor's Degree thesis in Nuclear Engineering. The project focuses on the neutronic analysis and reactivity coefficient evaluations for **ALFRED** (Advanced Lead Fast Reactor), a Generation IV heavy liquid metal-cooled fast reactor concept.

The codebase is designed with a modular structure in Python, orchestrated through a Jupyter Notebook to perform high-fidelity core analysis and post-processing.

## Key Features
- **Modular Assembly Modeling:** Dedicated Python modules in `src/` (`fuel_inner.py`, `fuel_outer.py`, `control_rods.py`, `safety_rods.py`, `dummy_elements.py`, `materials.py`) defining geometry and material compositions.
- **Neutronics & Reactivity Calculations:** Implementation of routines to compute effective multiplication factor ($k_{eff}$), Doppler and coolant temperature coefficients, control rod worth, fuel depletion, and isotopic evolution over operational cycles.
- **Automated Workflow:** Orchestrated via the Jupyter Notebook (`notebooks/core.ipynb`) for end-to-end analysis and plotting.
- **Numerical Results & Data:** Structured `.csv` results, perturbation data, and burnup steps stored in `data/`.
- **Data Visualization:** Comprehensive plots for core layouts, flux distributions, reactivity curves and burnup evolution.

## Repository Structure

```text
ALFRED-Neutronics/
│
├── README.md               # Project documentation
├── data/                   # Calculated keff values, temperature perturbations, and control rod steps
├── img/                    # Core maps, flux distributions, reactivity plots and burnup plots
├── notebooks/              # Main Jupyter Notebook for calculations (core.ipynb)
└── src/                    # Core Python modules for assemblies and materials
```

## Requirements
- Python 3.x
- NumPy, SciPy, Matplotlib, Jupyter
- Neutronic transport code / cross-section libraries configured locally

## Author
Giulia Ravicini, 
 Engineering Student
