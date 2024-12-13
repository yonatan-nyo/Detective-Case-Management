# Ketebak

A desktop application built with **Flet** for managing tasks using an MVC architecture and a PostgreSQL database.

---

## Features

-   **Case Management**

    -   Allows users to manage and view cases.

-   **Suspect Management**

    -   Displays and manages suspect information.

-   **Victim Management**

    -   Manages and displays information about victims in cases.

-   **Search**

    -   Facilitates searching across both suspect and victim data.

-   **Visualization Chart**

    -   Provides charts and visual representations of statistical data related to cases, suspects, or victims.

-   **Report**

    -   Generates reports based on case data.

-   **Database Handler**

    -   Manages the database for storing and retrieving case, victim, and suspect information.

-   **Calendar Module**
    -   Displays and allows interaction with the case scheduling.

---

## Prerequisites

Before running the application, ensure the following tools are installed:

-   **Python**: Version 3.11.4.
-   **PostgreSQL**: For database storage.
-   **pip**: Python package manager.

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

-   Create a PostgreSQL database.
-   Set up a `.env` file in the project root with the following content (adjust values as needed):

```env
DATABASE_URL=postgresql://<username>:<password>@localhost/<database_name>
```

### 5. Run the Application

Launch the application with:

```bash
flet run
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
│   ├── controllers/    # Controller logic (handles business operations)
│   ├── models/         # Database models and initialization scripts
│   ├── routes/         # Routing
│   ├── views/          # PyQt6-based UI components
│   └── main.py         # Entry point of the application
├── tests/              # Unit tests and testing framework
├── .env
├── .gitignore
├── README.md           # Project documentation
└── requirements.txt    # List of Python dependencies

```

## Modules

| No  | Daftar Modul        | Nama Modul                 | Pembagian Tugas                     |
| --- | ------------------- | -------------------------- | ----------------------------------- |
| 1.  | Case Management     | Case View                  | 13523008 13523012 13523036          |
| 2.  | Suspect Management  | Suspect View               | 13523008 13523036                   |
| 3.  | Victim Management   | Victim View                | 13523008 13523012 13523036 13523092 |
| 4.  | Search              | Suspect View & Victim View | 13523036 13523044 13523092          |
| 5.  | Vizualization Chart | Statistic View             | 13523008                            |
| 6.  | Report              | Case View                  | 13523008                            |
| 7.  | Database Handler    | Database                   | 13523036                            |
| 8.  | Calendar Module     | Schedule View              | 13523008 13523036                   |


### Case

![Case](doc\case_view.png)

### Suspect

![Suspect](doc\suspect_view.png)

### Victim

![Victim](doc\victim_view.png)

### Schedule

![Schedule](doc\schedule_view.png)

### Statistic

![Statistic](doc\statistic_view.png)

## Database

#### `cases`

| Column      | Type    | Description             |
| ----------- | ------- | ----------------------- |
| id          | Integer | Primary key.            |
| progress    | Integer | Progress percentage.    |
| startDate   | Date    | Start date of the case. |
| description | Text    | Case description.       |
| detective   | String  | Detective assigned.     |
| priority    | String  | Priority level.         |

#### `suspects`

| Column       | Type    | Description       |
| ------------ | ------- | ----------------- |
| id           | Integer | Primary key.      |
| nik          | String  | National ID.      |
| picture_path | String  | Path to picture.  |
| name         | String  | Name of suspect.  |
| age          | Integer | Age of suspect.   |
| gender       | Boolean | Gender.           |
| note         | Text    | Additional notes. |

#### `victims`

| Column          | Type    | Description                   |
| --------------- | ------- | ----------------------------- |
| id              | Integer | Primary key.                  |
| nik             | String  | National ID.                  |
| picture_path    | String  | Path to picture.              |
| name            | String  | Name of victim.               |
| age             | Integer | Age of victim.                |
| forensic_result | Text    | Results of forensic analysis. |

#### `case_suspects`

| Column     | Type       | Description              |
| ---------- | ---------- | ------------------------ |
| case_id    | ForeignKey | Reference to `cases`.    |
| suspect_id | ForeignKey | Reference to `suspects`. |

#### `case_victims`

| Column    | Type       | Description             |
| --------- | ---------- | ----------------------- |
| case_id   | ForeignKey | Reference to `cases`.   |
| victim_id | ForeignKey | Reference to `victims`. |
