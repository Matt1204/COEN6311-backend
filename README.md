# Flask Application Setup Guide

This guide provides detailed steps on how to set up and run the Flask application locally.

## Prerequisites

Before you begin, ensure you have Python installed on your system. This project requires Python 3.x.

## Setting Up Your Development Environment

1. **Clone the Repository**
   - First, clone the repository to your local machine using the following command:
     ```
     git clone <REPOSITORY_URL>
     ```
   - Replace `<REPOSITORY_URL>` with the URL of the repository.

2. **Navigate to the Project Directory**
   - Change directory to the project:
     ```
     cd path/to/backend
     ```

3. **Create a Virtual Environment**
   - Run the following command to create a virtual environment named `venv`:
     ```
     python -m venv venv
     ```

4. **Activate the Virtual Environment**
   - On Windows, activate the virtual environment by running:
     ```
     .\venv\Scripts\activate
     ```

5. **Install Dependencies**
   - Install the required Python packages using:
     ```
     pip install -r requirements.txt
     ```

## Configuration

- **Environment Variables**
  - Copy the `.env.example` file to a new file named `.env`.
  - Modify the `.env` file with your local settings.
  - Example:
    ```
    cp .env.example .env
    ```

## Running the Application

To run the application, use the following command:

    flask --app app.py --debug run
    

This command will start the Flask server in debug mode, which includes an automatic reloader and a debugger.

## Additional Information

- Make sure to check the `.gitignore` file to ensure sensitive files like `.env` are not committed to the repository.
- For any contributions, please create a new branch and use pull requests to merge changes.

## Support

For any additional help or issues, feel free to contact the development team or raise an issue in the repository.
