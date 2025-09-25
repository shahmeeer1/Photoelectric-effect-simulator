<h1 align="center">
<a><img src="https://github.com/shahmeeer1/Photoelectric-effect-simulator/blob/main/phet.png" width="200"></a>
<br>
Photoelectric Effect Simulator
<br>
</h1>
<h4 align="center">An experimental physics simulator built in Python</a>.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/language-Python-blue.svg" alt="Language">
  <img src="https://img.shields.io/badge/GUI-Pygame-lightgrey.svg" alt="GUI">
  <img src="https://img.shields.io/badge/database-SQLite-blue.svg" alt="Database">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

## 📖 About The Project

This project is an interactive simulator for the photoelectric effect built entirely in Python to visualize and analyze the photoelectric effect. 
It serves as an educational tool designed to help students, educators, and physics enthusiasts visualize and understand the fundamental principles of the photoelectric effect in an engaging way.

Users can conduct virtual experiments by selecting different metallic surfaces, adjusting the wavelength and intensity of incident light, and observing the resulting emission of photoelectrons. 
The simulator provides real-time feedback on key physical quantities and includes robust data logging and analysis features.

## ✨ Features

*   **Interactive Simulation:** Dynamically observe electron emission from different metals under varying light conditions.
*   **Metal Selection:** Choose from a list of predefined metals, each with its unique work function.
*   **Adjustable Light Properties:** Control the frequency (color) and intensity of incident light.
*   **Real-time Output:** View calculated values such as kinetic energy of emitted electrons and photocurrent.
*   **Data Recording:** Save simulation results to a local database for later analysis.
*   **Comprehensive Data Analysis:** Generate various graphs to visualize relationships:
    *   Current vs. Frequency
    *   Kinetic Energy vs. Frequency
    *   Current vs. Intensity
    *   Kinetic Energy vs. Intensity
*   **Regression Analysis:** Perform linear regression on generated data to extract physical constants (e.g., Planck's constant).
*   **Theoretical Background:** Access a dedicated section explaining the theory behind the photoelectric effect.
*   **Intuitive GUI:** Built with Pygame for a responsive and engaging user experience.

## 📚 Tech Stack

*   **Language:** Python
*   **GUI Framework:** Pygame, Pygame-GUI
*   **Data Storage:** SQLite (`.db` files)
*   **UI Styling:** Custom JSON themes for Pygame-GUI

## 🚀 Installation

Follow these steps to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shahmeeer1/Photoelectric-effect-simulator.git
    cd Photoelectric-effect-simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the application:**
    ```bash
    python src/app.py
    ```

## ▶️ Usage

Once the application launches, you can:
*   Navigate through the main menu.
*   Start a simulation to select metals and adjust light properties.
*   Record your experimental data.
*   Access the "View Data" section to review saved results.
*   Use the "Analyse" section to generate graphs and perform regression analysis on your recorded data.
*   Explore the "Theory" section for an educational overview of the photoelectric effect.
