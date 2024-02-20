# Team Number 3

## Members
1. Kamron Hopkin
2. Jeremiah Teele
3. Curtis Moore

## Project Management Tools
Jira Project Management Link - https://seng4235-team3.atlassian.net/jira/software/projects/ST/boards/1

Microsoft Teams - https://teams.microsoft.com/l/team/19%3AUtx_ME2TggtrbhQU5uUTFnj5bokJVm0vI61l5bFdnsA1%40thread.tacv2/conversations?groupId=48a114f7-4d30-4a52-b92c-ca86e5259313&tenantId=17143cbb-385c-4c45-a36a-c65b72e3eae8


# Project Setup Guide

This guide will walk you through setting up the project environment for [course-project-group-3](https://github.com/ECU-SENG4235/course-project-group-3.git) using GitHub Desktop and PyCharm.

## Prerequisites

- Install [GitHub Desktop](https://desktop.github.com/)
- Install [PyCharm](https://www.jetbrains.com/pycharm/download/)
- Ensure [Git](https://git-scm.com/downloads) is installed on your system

## Cloning the Repository with GitHub Desktop

1. **Open GitHub Desktop** and sign in with your GitHub account.
2. **Clone the repository**:
   - Go to `File` > `Clone Repository`.
   - In the dialog that appears, switch to the `URL` tab.
   - Paste the repository URL `https://github.com/ECU-SENG4235/course-project-group-3.git` into the URL field.
   - Choose a local path where you want the repository to be saved.
   - Click `Clone`.

## Opening the Project in PyCharm

1. **Open PyCharm**.
2. Choose `Open` on the welcome screen or go to `File` > `Open` if you have another project open.
3. **Navigate to the cloned repository** folder on your computer and select the project folder.
4. Click `OK` to open the project in PyCharm.

## Activating the Virtual Environment

1. **Open the PyCharm Terminal**:
   - In PyCharm, find the Terminal tab at the bottom of the window and click it to open the command line within PyCharm.
2. **Navigate to your project directory** (if not already there) using the `cd` command.
3. **Activate the virtual environment**:
   - For **Windows**, run:
     ```
     .venv\Scripts\activate
     ```
   - For **macOS and Linux**, run:
     ```
     source .venv/bin/activate
     ```
   - Replace `.venv` with your virtual environment's name if it differs.

## Running the Program

1. **Ensure the virtual environment is activated**.
2. Run the program using the PyCharm built-in command line:
   - Type the command to run your program (e.g., `python script.py`) in the terminal within PyCharm.
   - Replace `script.py` with the path to the main script of your project.

## Additional Notes

- If you encounter any issues with the virtual environment, ensure that you have Python installed and that PyCharm is configured to use the correct interpreter.
- For detailed documentation on PyCharm's features and settings, refer to the [PyCharm Documentation](https://www.jetbrains.com/pycharm/documentation/).

---

To run a Django server and view your project in a browser, you would typically follow these steps after setting up your project environment in PyCharm and activating your virtual environment. Here are the additional commands and steps needed:

### Install Project Dependencies

First, ensure that all project dependencies are installed. This is usually done via a `requirements.txt` file that lists all the necessary Python packages.

1. **Navigate to the project directory** in the PyCharm Terminal (if you are not already there).
2. **Install dependencies** by running:
   ```sh
   pip install -r requirements.txt
   ```
   Make sure your virtual environment is activated before running this command.

### Apply Migrations

Django uses migrations to propagate changes made to models (adding a new field, deleting a model, etc.) into the database schema. Before running the server for the first time, you need to apply these migrations.

1. **Apply migrations** by running:
   ```sh
   python manage.py migrate
   ```
   This command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your `settings.py` file and the migration files in your project.

### Run the Development Server

Django comes with a built-in web server for development purposes. To start this server:

1. **Run the server** by executing:
   ```sh
   python manage.py runserver
   ```
2. By default, the server runs on port 8000. You can specify a different port by appending it to the command (e.g., `python manage.py runserver 8080` to run on port 8080).

### View the Project in a Browser

After starting the development server:

1. **Open a web browser** of your choice.
2. **Navigate to** `http://127.0.0.1:8000/` or `http://localhost:8000/` (replace `8000` with your chosen port if different).

This will open the home page of your Django project. From here, you can navigate through your site based on the URLs you've defined in your project.

To SHUT DOWN the development server:

1. **Returm to the command-line** of your IDE of choice where the project is open.
2. **Press** `CONTROL+C` and hit ENTER.

This will deactivate the virtual environment and shut down the development server.

### Additional Commands

- **Creating a superuser** for Django admin:
  ```sh
  python manage.py createsuperuser
  ```
  Follow the prompts to create a user. You can then access the Django admin by navigating to `/admin` on your site.

- **Collecting static files** (if your project uses them):
  ```sh
  python manage.py collectstatic
  ```
  This command collects all static files from your apps (and any other locations specified by the STATICFILES_DIRS setting) into the STATIC_ROOT directory.

These commands will help you get your Django project running on your local development server and allow you to view and interact with it in a web browser.
