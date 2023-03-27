# Companion Web App for MaNGOS Quest Tracker

A simple web app to display quests accepted, abandoned, and completed in your server. This tool may assist developers with identifying quests that are frequently abandoned (likely broken!) or require GM assistance in completing (likely broken too!).

In order to begin to populate your QuestTracker database table, make sure to enable Quest Tracker in the mangosd.conf from your MaNGOS server installation.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine. Tested on Ubuntu 20.04 WSL.

### Prerequisites

Run the following:
- `sudo apt-get install libmariadb-dev python3-dev`
- `sudo git clone https://github.com/i-am-fyre/MaNGOS-QuestTracker`
- `cd MaNGOS-QuestTracker`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

### Configuration

You can set your database information in `config.ini`.

### Starting Up

Once the pre-requisites above have been installed and configurations are set, do the following:
- `export FLASK_APP=main.py`
- `flask run`
Your local server should then be running at http://localhost:5000

If you want to see raw data for all quests, go to: http://localhost:5000/all
