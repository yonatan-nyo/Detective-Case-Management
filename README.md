# Ketebak

A desktop application built with **PyQt6** for managing tasks using an MVC architecture and a PostgreSQL database.

## Features

- **Case Management**: Add ....
- **Modern UI**: Built using PyQt6 for a clean and user-friendly interface.

---

## Prerequisites

Before running the application, ensure the following tools are installed:

- **Python**: Version 3.11.4.
- **PostgreSQL**: For database storage.
- **pip**: Python package manager.

---

## How to Run

Follow these steps to set up and run the application:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set Up a Virtual Environment

To keep dependencies isolated, create a Python virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows (BASH)
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

- Create a PostgreSQL database.
- Set up a `.env` file in the project root with the following content (adjust values as needed):

```env
DATABASE_URL=postgresql://<username>:<password>@localhost/<database_name>
```

### 5. Run the Application

Launch the application with:

```bash
python main.py
```

---

## Folder Structure

```plaintext
project/
├── .venv/              # will be created after step 2.Set Up a Virtual Environment
├── doc/                # Documentation files
├── img/                # Images and visual resources
├── src/                # Source code directory
│   ├── __init__.py     # Initialize the src package
│   ├── __pycache__/    # Compiled Python files (auto-generated)
│   ├── controllers/    # Controller logic (handles business operations)
│   ├── models/         # Database models and initialization scripts
│   └── views/          # PyQt6-based UI components
├── tests/              # Unit tests and testing framework
├── .env
├── .gitignore
├── main.py             # Entry point of the application
├── README.md           # Project documentation
└── requirements.txt    # List of Python dependencies

```

## Modules

## Database
