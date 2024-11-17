# 🏥 Hospital Management System - Bed Booking & Appointment Web App

Welcome to the **Hospital Management System**! This full-stack web application helps users manage hospital bookings and appointments efficiently. Built with Flask, SQLAlchemy, and front-end technologies, this project provides a seamless user experience for both doctors and patients. 🚀

## 📝 Project Overview
This web app includes functionalities such as:
- 🧑‍💻 **User Authentication**: Secure sign-up, login, and logout.
- 🩺 **Doctor Management**: Add and view doctor information.
- 🧑‍⚕️ **Patient Booking**: Patients can book and edit appointments.
- 📅 **Appointment Viewing**: Patients can see their booking details.
- ✉️ **Email Notifications**: Confirmation emails for patients after booking.
- 🔒 **User Authorization**: Restrict editing and deletion to authorized users.

## ⚙️ Technologies Used
- **Backend**: Flask, Flask-Login, Flask-Mail, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 🎨
- **Database**: MySQL
- **Other**: JSON for configuration, Python for logic

## 🚦 Getting Started
Follow these steps to set up the project:

### 🛠 Prerequisites
Ensure you have the following installed:
- Python 3.x 🐍
- MySQL

### 📥 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hospital-management-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hospital-management-system
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `config.json` with your Gmail credentials for email notifications.

### 📂 Database Setup
- Create a MySQL database named `hms`.
- Update your database URI in `app.config`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hms'
   ```

### 🏃‍♂️ Running the App
Start the Flask server:
```bash
python app.py
```
Access the app at `http://127.0.0.1:5000/` 🌐

## 🖥 Features

### 🔑 User Authentication
- **Sign Up**: New users can register securely.
- **Login**: Existing users can log in.
- **Logout**: Users can log out safely.

### 👨‍⚕️ Doctor Management
- Add and manage doctor records with their department.

### 🏥 Patient Appointment Booking
- Patients can book slots, specifying details like name, time, date, and department.

### 📧 Email Notifications
- Confirmation emails sent to users upon successful booking.

### 📝 Edit & Delete Appointments
- Users can modify or cancel their appointments if necessary.

## 🖼 Screenshots
- **Home Page** 🏠
- **Login Page** 🔐
- **Doctor Registration Form** 🩺
- **Patient Booking Form** 🏥

## 🚧 Future Enhancements
- Add **Admin Dashboard** for better management.
- Implement **SMS notifications** for bookings 📱.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License
This project is licensed under the MIT License.

---

### 📬 Contact
For any questions, feel free to reach out:
- **Email**: support@hospitalapp.com 📧
- **GitHub**: [YourUsername](https://github.com/yourusername) 🖥

Thank you for using the **Hospital Management System**! We hope it simplifies your hospital booking process. 😊

