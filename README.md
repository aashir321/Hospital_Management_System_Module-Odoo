# Hospital Management System – Odoo

A custom Hospital Management System developed as an Odoo ERP module using Python and XML. The module provides hospital-related functionality for managing patients, doctors, appointments, medical records, billing, and patient reports.

It also extends Odoo's existing Sales and Accounting modules with custom quotation approval workflows, reference numbers, and invoice integration.

## Overview

The Hospital Management System is designed to organize essential hospital operations within Odoo.

It provides dedicated models and views for patients, doctors, and appointments while integrating with Odoo's built-in Contacts, Sales, Accounting, and Mail functionalities.

The module also includes PDF and Excel reporting capabilities to make patient information easier to access and maintain.

## Features

### 1. Patient Management
- Create and manage patient profiles.
- Store personal and contact information.
- Maintain blood groups, gender, and date of birth.
- Automatically calculate patient age.
- Maintain patient medical history.
- Store emergency contact and guardian information.
- Automatically create a related customer record in Odoo Contacts.
- Track appointments associated with each patient.
- Calculate consultation fees, medicine charges, taxes, discounts, and grand totals.
- Archive patient records.

### 2. Doctor Management
- Register doctors with their professional information.
- Maintain doctor names, departments, phone numbers, and email addresses.
- Store medical license numbers.
- Add additional notes about doctors.
- Search and group doctors by department.

### 3. Appointment Management
- Create appointments for registered patients.
- Assign doctors and departments.
- Maintain appointment dates, booking dates, and appointment times.
- Automatically retrieve patient email and doctor department information.
- Record symptoms, diagnosis, prescriptions, and doctor notes.
- Manage appointment priorities:
  - Low
  - Medium
  - High
  - Very High
- Track appointment status:
  - Draft
  - In Consultation
  - Done
  - Cancelled
- Add medical services to appointments.
- Automatically calculate service subtotals and appointment grand totals.

### 4. Billing and Invoicing
- Add services to patient appointments using Odoo products.
- Automatically retrieve product prices.
- Calculate service subtotals based on quantity and unit price.
- Generate customer invoices directly from appointments.
- Maintain patient invoice history.
- View invoices through a smart button.
- Extend Odoo Accounting with a custom sale reference field.

### 5. Patient Reports

**PDF Reports**
- Generate patient medical reports using Odoo QWeb templates.
- Include patient personal information and medical history.
- Display appointment and doctor information.
- Include symptoms, diagnosis, prescriptions, and doctor notes.
- Display emergency contact information.
- Include billing details and grand totals.
- Add report generation date, time, and user information.
- Include hospital branding and signature sections.

**Excel Reports**
- Export individual patient information into Excel format.
- Generate formatted worksheets using XlsxWriter.
- Include patient information, medical history, emergency contacts, and billing details.
- Apply formatting for headers, labels, dates, and financial totals.

### 6. Sales Order Approval Workflow

The module extends Odoo's existing Sales Order functionality.

- Generate unique quotation reference numbers using Odoo sequences.
- Introduce a custom quotation approval status.
- Allow users to send quotations for approval.
- Notify approvers through Odoo activities.
- Introduce a dedicated Sales Order Approver group.
- Allow authorized approvers to approve quotations.
- Record the approver and approval date.
- Restrict quotation confirmation until approval is completed.
- Automatically approve quotations created by authorized approvers.
- Track quotation creation and confirmation activities through Odoo Chatter.

### 7. Odoo Integration
The module integrates with the following standard Odoo applications:

- Contacts
- Sales
- Accounting
- Mail and Activities
- Product Management

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend logic and business models |
| Odoo ORM | Database operations and model relationships |
| XML | Forms, lists, search views, menus, and reports |
| QWeb | PDF report templates |
| CSV | Model access rights |
| XlsxWriter | Excel report generation |
| Odoo Mail | Chatter and activity tracking |
| Odoo Sequences | Automatic reference generation |

## Project Structure

```text
Hospital_Management_System_Module-Odoo/
│
└── github_repos/
    └── tutorials/
        └── module_hospital/
            │
            ├── __init__.py
            ├── __manifest__.py
            │
            ├── controllers/
            │   ├── __init__.py
            │   └── main.py
            │
            ├── models/
            │   ├── __init__.py
            │   ├── patient.py
            │   ├── doctor.py
            │   ├── appointment.py
            │   ├── appointment_line.py
            │   ├── sale_order.py
            │   ├── account_move.py
            │   └── sale_advance_payment_inv.py
            │
            ├── security/
            │   ├── ir.model.access.csv
            │   └── security.xml
            │
            ├── views/
            │   ├── menu.xml
            │   ├── patient_view.xml
            │   ├── doctor_view.xml
            │   ├── appointment_view.xml
            │   ├── female_patients_view.xml
            │   ├── sale_order_inherit_view.xml
            │   ├── sale_order_approval_view.xml
            │   ├── account_move_view.xml
            │   └── sale_advance_payment_inv_view.xml
            │
            ├── report/
            │   ├── __init__.py
            │   ├── patient_report.py
            │   ├── patient_report.xml
            │   ├── report.xml
            │   ├── report_style.xml
            │   └── sale_order_report.xml
            │
            ├── data/
            │   └── sequence.xml
            │
            └── static/
                └── description/
                    └── icon.png
```

## Installation and Setup

### Prerequisites

- Odoo Server
- Python
- PostgreSQL
- Required Odoo applications:
  - Sales
  - Accounting
  - Contacts
  - Mail
- Python package: XlsxWriter

### Step 1: Clone the Repository

```bash
git clone https://github.com/aashir321/Hospital_Management_System_Module-Odoo.git
```

### Step 2: Install Python Dependency

```bash
pip install XlsxWriter
```

### Step 3: Add the Module to Odoo

Copy the `module_hospital` directory into your Odoo custom addons directory.

Alternatively, configure the parent directory of `module_hospital` in the Odoo addons path.

### Step 4: Configure Odoo

Restart the Odoo server and ensure that the custom addons directory is included in the addons path.

### Step 5: Install the Module

1. Open your Odoo instance.
2. Activate Developer Mode.
3. Navigate to Apps.
4. Update the Apps List.
5. Search for **Hospital Management System**.
6. Install the module.

After installation, the Hospital menu will become available in the Odoo interface.

## Technical Implementation

### Custom Odoo Models

| Model | Responsibility |
|---|---|
| `hospital.patients` | Patient information and billing |
| `hospital.doctors` | Doctor information |
| `hospital.appointment` | Appointment management |
| `hospital.appointment.line` | Appointment services and pricing |

### Inherited Odoo Models

| Existing Model | Customization |
|---|---|
| `sale.order` | Reference numbers and approval workflow |
| `account.move` | Custom sale reference |
| `sale.advance.payment.inv` | Reference propagation to advance payment wizard |

### Important Odoo Concepts Used

- Model inheritance and custom models.
- Many2one and One2many relationships.
- Computed fields using `@api.depends`.
- Onchange methods using `@api.onchange`.
- ORM create method customization.
- Window and URL actions.
- XML view inheritance using XPath.
- Access control using `ir.model.access.csv`.
- User groups and role-based approval checks.
- QWeb PDF reporting.
- HTTP controllers and Excel generation.
- Chatter and scheduled activities.

## Learning Outcomes

This project demonstrates practical implementation of Odoo ERP customization, including:

- Developing custom Odoo modules.
- Designing relational data models.
- Implementing business logic using Python.
- Customizing existing Odoo applications.
- Creating interactive backend views.
- Implementing approval workflows.
- Generating PDF and Excel reports.
- Working with Odoo security and access rights.
- Integrating Sales and Accounting operations.

## Project Information

**Project:** Hospital Management System – Odoo Module

**Category:** Odoo ERP Development

**Backend:** Python

**Framework:** Odoo

**Author:** Aashir Azeem

**Repository:** [GitHub – Hospital Management System Module](https://github.com/aashir321/Hospital_Management_System_Module-Odoo)

---

*This project was developed as part of practical Odoo development and ERP customization work during an internship.*
