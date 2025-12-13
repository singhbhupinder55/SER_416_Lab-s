# CERT Disaster Preparedness Application  
### SER 416 – Software Enterprise Projects & Process  
### Final Project – Developer Route  
### Author: Bhupinder Singh (bsingh55)

---

## **Overview**
This project is a command-line prototype application developed for the Community Emergency Response Team (CERT).  
The purpose of this tool is to allow CERT volunteers to collect and manage household information that may be critical during emergencies such as floods, earthquakes, or fires.

Furthermore, this prototype intentionally focuses on core household-data workflows required by CERT for emergency preparedness. Features such as record deletion, duplicate detection, and centralized multi-user access are not part of the Phase 1 specification and will be considered in future development phases.

This application fulfills the **Phase 1 (Developer Route)** requirements described in the CERT Software Project Charter, including:

- Local, offline execution
- SQLite data storage
- Ability to add, view, edit, import, and export household records
- Full input validation
- A clean, modular Python codebase suitable for future expansion into a web application

---

## **Features Implemented**

### **1. Main Menu Interface**
The program runs in the terminal and provides the following menu options:

1. View Records  
2. Add New Record  
3. Import Records from CSV  
4. Export Records to CSV  
5. Quit  

Each option validates input and returns to the menu when finished.

---

### **2. Add New Household Record**
The system collects three types of questions:

#### **Required Questions**
- Number of adults  
- Number of children  
- Pets? (follow-up: dogs?)  
- Critical medications? (follow-up: require refrigeration?)  
- Special needs / evacuation concerns  
- Large propane tank?  
- Natural gas connection?  
- Address  

All required fields must be valid and cannot be left blank.

#### **Optional Questions**
- Phone number  
- Email address  
- Medical training  
- Know neighbors  
- Have a neighbor’s key  
- Want the CERT newsletter  
- Allow non-disaster contact  

Optional inputs may be skipped but are validated if entered.

Records are saved into the local SQLite database.

---

### **3. View and Edit Existing Records**
- Displays a clean numbered list of all households.  
- Pressing Enter returns to the main menu.  
- Selecting a number opens the selected record for editing.  
- Each field shows its current value in brackets (`[value]`).  
- Pressing Enter keeps the existing value.  
- All updated fields are saved back into the database with a new timestamp.

This matches the charter’s required editing behavior.

---

### **4. Export Records to CSV**
- Exports all records to the `output/` directory.  
- Automatically generates timestamped filenames:
- Exported Records YYYY-MM-DD_HH-MM-SS.csv
- Includes all database fields, including timestamps.  
- Displays success and the export path.

---

### **5. Import Records from CSV (Implemented, Minor Adjustment Pending)**
- Reads a user-specified CSV file path.  
- Validates required headers.  
- Converts fields to correct data types.  
- Inserts valid rows into the database.  
- Tracks how many rows succeeded vs. failed.  

---

## **Project Structure**
cert_app/
|
├── main.py            # Application entry point & menu
├── db.py              # SQLite connection, schema, CRUD operations
├── records.py         # Add, view, and edit record workflows
├── validation.py      # Input validation utilities
├── utils.py           # Formatting & console helpers
├── io_csv.py          # CSV import/export logic
│
├── cert_records.db    # SQLite database (auto-created)
└── output/            # Exported CSV files
All modules are documented with headers and docstrings for clarity.

---

## **Technical Stack**
- **Python 3**
- **SQLite3** (local file-based database for offline use)
- **CSV (Built-in Python CSV Module)**  
- **Modular Python design** with reusable components

---

## **How to Run**

1. Navigate to the project directory:
   ```bash
   cd cert_app
2.	Run the application:
```bash
python3 main.py
```
- The database is created automatically on first run.

## Example CSV Export File Included
- An example exported CSV file is provided inside the output/ directory, as required by the assignment submission instructions.

## Future Enhancements (Phase 2 – Web Migration)
Although not required for this offline Phase 1 prototype, the project charter outlines a long-term plan for transitioning CERT’s data collection system into a secure, web-based platform.
The current modular Python design and SQLite backend provide a strong foundation for these enhancements.

Below are realistic deliverables for Phase 2.

⸻

1. Duplicate Record Detection

As more volunteers use the system, preventing duplicate entries becomes important.
Future enhancements may include:
	•	Detecting duplicates based on address or household composition
	•	Warning the user when importing a CSV that contains existing data
	•	Options to skip, merge, or update duplicate records

⸻

2. Ability to Delete Household Records

Record deletion was not required for Phase 1, but would be appropriate in a more advanced version.

Phase 2 could add:
	•	A “Delete Record” option
	•	Soft-delete (archiving) with timestamps
	•	Admin-only permissions for deletion

⸻

3. Stronger Validation Rules

The prototype validates format, but Phase 2 could introduce:
	•	Address validation (regex pattern for street, city, state, ZIP)
	•	Consistent phone formatting
	•	Expanded email rules
	•	Logical validation (example: “dogs = yes” only when “pets = yes”)

⸻

4. Full Web Application Migration

A modern CERT system would run securely online so volunteers can access it from any device.

Technologies that could support this:
	•	Flask or Django REST API
	•	PostgreSQL or MySQL for scalable storage
	•	Web front-end (HTML/CSS/JS or React/Vue)
	•	Authentication and session management
	•	Role-Based Access Control (RBAC)

⸻

5. Cloud Hosting & Automated Backups

To ensure reliability during emergencies:
	•	Deployment to AWS EC2, Lightsail, Azure, or Google Cloud
	•	Automated database backups
	•	Disaster recovery procedures
	•	Encrypted storage

⸻

6. Mapping & Visualization Tools

CERT teams benefit from situational awareness.

A Phase 2 system could include:
	•	Interactive maps using Google Maps or Leaflet
	•	Icons showing households with special needs or risks
	•	Filters (medical needs, mobility issues, pets, etc.)
	•	Route planning for emergency checks

⸻

7. Reporting & Bulk Operations

Useful enhancements include:
	•	Export filtered subsets of households
	•	Bulk editing actions
	•	Printable reports for field deployment
	•	CSV summaries by neighborhood or risk category

⸻

8. Database Security Enhancements

A web-based system must include:
	•	HTTPS encryption
	•	Secure password handling
	•	Role-based permissions
	•	Audit logs for record changes


## Submission

This ZIP contains:
	•	Entire Python source code
	•	SQLite database schema (auto-created)
	•	Example exported CSV file
	•	Full project structure

This completes the Developer Route (Phase 1) implementation.

⸻
