
# ✈️ uBilet - Terminal Travel Planner

Welcome to the **uBilet Terminal Travel Planner** project! This is a command-line based application designed to simulate a complete travel booking experience — all within your terminal! 🧳🖥️

---

## 🧭 Project Overview

This project aims to create an interactive **CLI travel assistant** that supports:

- ✈️ **Flight Ticket Booking**  
- 🚌 **Bus Ticket Booking**  
- 🚆 **Train Ticket Booking**  
- 🏨 **Hotel Reservations**  
- 🚗 **Car Rentals**

All functionalities are presented **without a graphical user interface**, making it perfect for terminal enthusiasts or educational purposes.

---


## 🛠️ Technologies & Tools

- 🐍 **Python 3.9+**
- 🗃️ **OpenAI API**
- 🧪 **LangChain**
- 🧑‍💻 **VSCode or Cursor** (for development)
- 🌳 **Git** (for version control)
- ⚡ **FastAPI**
- 🚀 **Streamlit**

---

## 👥 User Roles

There are two types of users in the system:

- 🔐 **Admin**  
  - Can add, remove, and update travel options (flights, buses, trains, hotels, cars).
- 👤 **Basic User**  
  - Can book tickets, make reservations, and simulate payments.

User credentials are stored in a simple JSON structure with hashed passwords for security.

---

## 📁 Project Structure

The project follows a modular directory structure, clearly separating each booking module (flights, buses, etc.), user authentication, and admin operations. All placeholder data is kept in the `data/` directory as JSON files.

---

## 🎯 Key Features

- 🔜 Terminal-based interaction (CLI only)
- 🔜 Role-based access control (admin vs. basic user)
- 🔜 Simulated payment flow
- 🔜 Placeholder travel data with easy extensibility
- 🔜 JSON-based local data storage (can later be upgraded to databases/APIs)

---

## 🔍 Future Enhancements

- 🌐 API integration for real travel data
- 💾 Database support (e.g., SQLite, PostgreSQL)
- 🌍 Multi-language support
- 📧 Email-based user registration and recovery

---

## 🧪 Testing Scenarios

- Input validation for each module (dates, cities, card info, etc.)
- Simulated payment success/failure messages
- Menu navigation robustness
- Error handling for invalid operations

---

## 🚀 Getting Started

1. Clone the repo  
2. Run the main script using Python  
3. Log in or register  
4. Enjoy your travel booking experience – from your terminal! 🎉

---

## 📝 License

This project is created for educational and learning purposes. Feel free to modify and enhance it as needed!

---

## 💬 Feedback

If you like this project or have suggestions for improvement, feel free to open an issue or contribute via pull requests.

Happy travels! 🧭🛫🛣️🚉🏨🚗
