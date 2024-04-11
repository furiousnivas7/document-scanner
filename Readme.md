# Flask Document Scanner to PDF

This Flask application allows users to upload multiple images of documents, which are then processed and compiled into a single PDF file. Users can then download this PDF. The application uses Flask as the web application framework, Pillow for image manipulation, and FPDF for generating PDF documents.

## Features

- **Multiple Image Upload**: Users can select and upload multiple images simultaneously.
- **PDF Conversion**: Uploaded images are automatically converted and merged into a single PDF file.
- **PDF Download**: Users can download the resulting PDF directly from the web interface.

## Prerequisites

Before you begin, ensure you have installed Python and pip on your system. This application has been tested with Python 3.6 and above.

## Installation

Follow these steps to set up the project locally:

### Clone the Repository

```bash
git clone https://github.com/furiousnivas7/document-scanner.git
cd flask-document-scanner-to-pdf


### Create a Virtual Environment
 python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install requirments.txt

### Run the application
python app.py


### Additional Notes:

1. **Repository URL**: Replace `https://your-repository-url.git` with your actual repository URL where this code is hosted.
2. **Testing Instructions**: Additional testing instructions might be necessary if the application has specific requirements or setup details not covered here.
3. **License File**: If you mention a license like MIT, make sure to include a `LICENSE` file in your repository.

This `README.md` provides a comprehensive overview and guide for setting up and using your Flask application, tailored for GitHub users and contributors. It's structured to be both informative and easy to follow for new users.
