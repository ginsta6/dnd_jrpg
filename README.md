# DnD JRPG Project

A text-based RPG inspired by Dungeons & Dragons (DnD), with a custom combat system, character creation, and management. This project aims to bring a simplified but immersive RPG experience, combining aspects of traditional tabletop gaming with interactive, dynamic gameplay mechanics.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [User's Guide](#users-guide)

---

## Installation

To get started with this project, follow these steps to install the required dependencies and set up the environment:

1. **Clone the repository**:
   `git clone https://github.com/your-username/dnd_jrpg.git`
   `cd dnd_jrpg`

2. **Create a virtual environment** (optional but recommended):
   `python -m venv venv`

3. **Activate the virtual environment**:
   - **Windows**:
     `venv\Scripts\activate`
   - **Mac/Linux**:
     `source venv/bin/activate`

4. **Install the required dependencies**:
   `pip install -r requirements.txt`

This will ensure that all necessary packages are installed and the project is set up correctly in your local environment.

## Usage

1. To start the game, run the `main.py` file:
   `python src/game/main.py`

2. Follow the on-screen instructions to  engage in combat.

## User's Guide

### Basic Gameplay

- The player can click a button to perform an attack or use a special ability.
  
  - **Berserker**: Has a *Grapple* special attack that restrains enemies, granting them disadvantage on their attacks.
  - **Acolyte**: Has a *Heal* special ability to restore health to themselves or allies.

### Combat

- After selecting an action, the player must choose a target.
- Once the target is selected, the action is performed, and the combat progresses.
- The *Console* will provide in-game details, such as which action was taken, which enemy was targeted, and the results of the action (e.g., damage dealt, health restored, etc.).

### Progression

- As the player defeats enemies, stronger ones will appear to challenge them.
- The goal is to continue defeating enemies while managing your own health.

