# Auto Parts Inventory System

Desktop inventory management system developed in Python for managing automotive parts in a refaction shop environment. The application provides a graphical interface that allows users to manage inventory data, store product information, and track stock availability using a local SQLite database.

The system was designed to simplify inventory control by allowing users to register automotive parts, manage product details such as cost, price, brand, warranty, and stock levels, and generate reports of the stored inventory. The application combines a graphical user interface, database management, and reporting tools to create a complete desktop inventory solution.

---

# Features

* Graphical desktop interface built with Tkinter
* Local SQLite database for persistent storage
* Add new products to inventory
* Edit existing product information
* Delete products from the system
* Track stock availability
* Detect low stock items
* Export inventory data to Excel
* Generate PDF reports

---

# Inventory Information Stored

Each product in the system includes the following data:

* Product ID
* Product name
* Cost
* Retail price
* Wholesale price
* Product type
* Brand
* Quality category
* Warranty duration (months)
* Stock availability
* Product lifespan

---

# Technologies Used

* Python
* Tkinter (GUI)
* SQLite3 (database)
* OpenPyXL (Excel export)
* ReportLab (PDF report generation)
* Dataclasses

---

# Project Structure

```
auto-parts-inventory-system
│
├── app.py
├── inventario.py
├── seed_db.py
├── inventario.db
├── requirements.txt
└── README.md
```

---

# How to Run

Install dependencies:

```
pip install openpyxl reportlab
```

Run the application:

```
python app.py
```

---

# Example Use Case

This application can be used in small automotive parts shops or warehouses to keep track of inventory, manage product pricing, and monitor available stock levels.

---

# Educational Purpose

This project demonstrates how a complete desktop application can be developed in Python by combining graphical interfaces, database management, and report generation. It illustrates how programming can be applied to build practical tools for inventory management and business operations.
