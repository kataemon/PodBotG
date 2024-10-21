#!/bin/bash

# Function to install Homebrew
install_homebrew() {
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "Homebrew installed successfully."
}

# Function to install Python 3 using Homebrew
install_python3() {
    echo "Installing Python 3..."
    brew install python
    echo "Python 3 installed successfully."
}

# Function to install ffmpeg using Homebrew
install_ffmpeg() {
    echo "Installing ffmpeg..."
    brew install ffmpeg
    echo "ffmpeg installed successfully."
}

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Do you want to install Homebrew? (y/n)"
    read answer
    if [ "$answer" != "${answer#[Yy]}" ]; then
        install_homebrew
    else
        echo "Homebrew is required for Python 3 and ffmpeg installation. Exiting."
        exit
    fi
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Do you want to install Python 3? (y/n)"
    read answer
    if [ "$answer" != "${answer#[Yy]}" ]; then
        install_python3
    else
        echo "Python 3 is required to continue. Exiting."
        exit
    fi
fi

# Create a directory for the virtual environment
VENV_DIR="PodBot"

# Create a virtual environment
echo "Creating Python virtual environment in $VENV_DIR..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages from requirements.txt
REQUIREMENTS_FILE="requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "No requirements.txt file found. Skipping package installation."
fi

# Install ffmpeg
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg is not installed. Installing ffmpeg..."
    install_ffmpeg
else
    echo "ffmpeg is already installed. Skipping."
fi
