# CourtSync

A comprehensive **Law Firm Management System** designed to streamline and automate the administrative and operational processes of a law firm. This project offers an intuitive graphical user interface (GUI) built using **Tkinter**, with robust database management powered by **MySQL**. 

### **Key Features**
1. **Client Management**:
   - Add, update, view, and delete client information.
   - Manage critical client details such as contact information, case history, and personal data.

2. **Lawyer Management**:
   - Manage lawyer profiles including specialization, contact details, and case allocations.

3. **Case Management**:
   - Record and track case details including hearing dates, case status, and involved parties.

4. **Appointment Scheduling**:
   - Schedule and manage client-lawyer meetings with date, time, and status tracking.

5. **Billing and Invoicing**:
   - Generate and manage bills for legal services, with fields for payment status and history.

6. **Error Handling and Validation**:
   - Comprehensive error handling for both GUI interactions and database operations.
   - Ensures smooth operations with clear and concise error messages for users.

7. **Scrollable Views**:
   - Fully scrollable tables for viewing large datasets dynamically.

8. **Responsive Navigation**:
   - Multiple pages with clear navigation buttons for CRUD operations, table views, and returning to the home page.

---

### **Technology Stack**
- **Frontend**: Tkinter (Python's GUI library)
- **Backend**: MySQL (Database)
- **Database Connectivity**: pymysql library
- **Development Environment**: Python 3.x

---

### **Use Case**
The system is tailored for law firms to efficiently manage clients, lawyers, and cases while improving productivity. It is particularly useful for:
- Automating routine tasks like data entry and record management.
- Reducing manual errors in billing and scheduling.
- Providing quick access to data for decision-making and case preparation.

---

### **Installation Instructions**
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd law-firm-management-system
   ```

2. **Set Up the MySQL Database**:
   - Create a MySQL database named `law_firm_management`.
   - Import the provided SQL file to set up the tables.

3. **Install Dependencies**:
   ```bash
   pip install pymysql
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

---

### **Database Tables**
The system uses the following tables:
- `clients`: To manage client information.
- `lawyers`: To manage lawyer profiles.
- `cases`: To manage case details.
- `appointments`: To manage scheduling.
- `billing`: To manage invoicing and payments.

---

### **Contribution Guidelines**
We welcome contributions to enhance the project. Please follow the steps below:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with descriptive messages.
4. Submit a pull request.

---

### **License**
This project is open-source and licensed under the [MIT License](LICENSE).
