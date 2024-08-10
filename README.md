# IntegriNews

![IntegriNews](https://github.com/user-attachments/assets/e90c1064-e9e8-40bb-b7cf-cb99d99d0d3c)

**IntegriNews AI** is a cutting-edge Fake News Classifier application, leveraging a custom-built TensorFlow model trained on the WELFake dataset. With an accuracy rate exceeding 98%, IntegriNews offers a robust solution for identifying and classifying misinformation.

![App Screenshot](https://github.com/AizazL/IntegriNews/assets/17864654/0e803f27-7e4b-4428-8bfd-f89fe243e327)

## Application Features

- **Article Classification**: Enter an article title and text, then press classify to view the results. You can input text manually or upload a supported file (`.pdf`, `.txt`, `.docx`). The text will automatically be extracted and displayed in the application.
- **Export Results**: Easily export all classification results from your current session into a `.csv` file with a single click.
- **Dark Mode**: Toggle between dark and light mode at any time using the checkbox located at the top right corner of the interface.
- **Live Pie Chart**: View an interactive pie chart that dynamically updates to reflect the classification ratios for the current session.

## Getting Started

### Running the Application

You can run the application in two ways:

1. **Executable**: Run the `.exe` file located in `dist/IntegriNews`. Ensure you have the `_internal` folder, which contains all the necessary libraries.
2. **Source Code**: If you have the correct Python version and all required libraries installed, you can run `main.py` directly.

### Prerequisites

- **Python Version**: Ensure you have Python 3.x installed. 
  ```bash
  pip install -r requirements.txt
