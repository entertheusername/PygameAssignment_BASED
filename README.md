## Installation Guide

Follow the steps below to set up and run the system successfully:

1. **Download and Extract Files**
   * Download this project as ZIP file.
   * Extract the contents to a desired location on your computer.

2. **Set Up the Database**
   * Launch **WampServer**.
   * Open **phpMyAdmin** from localhost.
   * Create a new database.
   * Import the provided SQL file into the newly created database.

3. **Configure the Python Environment**
   * Open any Python-compatible IDE (e.g., **Visual Studio Code**, **PyCharm**).
   * Ensure latest Python version is installed and added to your system PATH (preferably Python 3.12 or Python 3.13).
   * Open the project folder.
   * Navigate to the terminal and install the required dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application**
   * Navigate to the `/FrontEnd` folder in your editor.
   * Run the main application script `/FrontEnd/Main.py`.
   * If using **Visual Studio Code**, run the main application script using the pre-configured `launch.json` file.

---

### Troubleshooting

1. If encountering issues related to missing modules, ensure `requirements.txt` is fully installed without errors.
   * Potential root cause: Multiple Python versions are installed on the same machine, and the IDE might be running with a different Python interpreter where the modules aren't installed.
   * Solution:
     1. Verify the list of modules installed in the current python intepreter by running:
        ```bash
        python -m pip list
        ```
     2. Verify the current Python version by running:
        ```bash
        python --version
        ```
     3. For **VSC**, use the command palette (Ctrl + Shift + P) → `Python: Select Interpreter` to change the inteperter.
     4. FOR **PyCharm**, go to *Settings* → *Project: \[Your Project]* → *Python Interpreter* to change the interpreter.
2. If WampServer is not working properly, verify that no other services are using port 80 or 3306.
     
