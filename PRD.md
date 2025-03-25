# uBilet - Interactive Travel Planner (CLI) ✈️🚌🚆🏨🚗

This document outlines the product details for an interactive travel planner application that runs entirely in the terminal (CLI). It covers the project purpose, directory structure, user management, modules, and other essential aspects.

---

## 1. Project Purpose and General Structure

### Project Purpose
- **Objective:** Create an interactive travel planner application using a command-line interface.
- **Services Offered:** Book plane, bus, train tickets, hotel reservations, and car rentals—all within one application.

### General Scope
- **CLI-Only Interface:** No graphical interface; all interactions are done via the command line.
- **Mandatory Fields for Flights:** Requires first name, last name, Turkish Republic ID number, and mobile phone number.
- **Version 1 Data:** Uses simple placeholder data or JSON files for ticket purchase and rental sections (bus, train, hotel, car rental).
- **Role-Based Features:** Incorporates a user login system and an admin panel to manage functionalities based on user roles.

### Tools to be Used
- **Programming Language:** Python 3.9+
- **Version Control:** Git
- **Editors:** VSCode and Cursor

---

## 2. User Login (auth.py) 🔐

- **User Registration & Role Management:**  
  - Define user registration with username, password, and role.
  - Users can have either an “admin” or “basic” (normal user) role.

- **Login Flow:**  
  - On startup, prompt for username and password.
  - If verification is successful, admin users are directed to the admin panel and basic users to the normal menu.

- **Data Storage:**  
  - User data is stored in a JSON file (e.g., `users.json`).
  - Passwords are stored securely using a hash function (e.g., `hashlib`).

---

## 3. Admin Panel (admin.py) 🛠️

### Admin Panel Main Menu
- **Options:**
  1. Add/Remove/Update Flight
  2. Add/Remove/Update Bus Service
  3. Add/Remove/Update Train Service
  4. Add/Remove/Update Hotel
  5. Add/Remove/Update Car
  6. Exit Admin Panel

### Key Features
- **Data Management:**  
  - Open specific JSON files (e.g., `flights.json`) to add, remove, or update records based on admin input.
  - Similar logic applies to bus, train, hotel, and car data.

- **Saving & Exiting:**  
  - After changes, update the JSON file using methods like `json.dump(...)`.
  - Exiting returns the user to the main menu or login screen.

---

## 4. Main Menu and Application Flow (main.py) 🚀

- **User Login:**  
  - Call the `login()` function to verify user credentials.
  - Direct users to the admin panel or normal menu based on their role.

- **Normal User Menu:**  
  - Presents options for booking plane tickets, bus tickets, train tickets, hotel reservations, and car rentals.
  - Users can exit the application by typing “exit” or selecting the corresponding option.

- **Admin Role Menu:**  
  - Provides an option to access the admin panel either automatically or via a menu selection.
  - After admin tasks, the application returns to the login screen or terminates.

---

## 5. Plane Ticket Module (flight.py) 🛫

- **Information Collection:**  
  - Gather details such as departure city, arrival city, travel date (dd.mm.yyyy), number of passengers, first name, last name, Turkish Republic ID number, and mobile phone number.

- **Placeholder Data:**  
  - Use data from `flights.json` or a Python list to display available flight options.

- **Payment Simulation:**  
  - After a schedule is selected, proceed with a payment simulation that confirms the ticket booking.

---

## 6. Bus Ticket Module (bus.py) 🚌

- **Details Collected:**  
  - Information such as departure, arrival, date, and optional seat selection.

- **Schedule Listing:**  
  - Use placeholder data from `buses.json` to show available bus schedules.

- **Payment Flow:**  
  - Simulate a payment process to complete the booking if the user proceeds.

---

## 7. Train Ticket Module (train.py) 🚆

- **Data Source:**  
  - Train schedules are stored in `trains.json` or similar data structures.

- **User Input:**  
  - Prompt the user for departure and arrival stations, date, and optionally, schedule time or wagon/seat options.

- **Filtering & Booking:**  
  - Display matching schedules and, upon selection, initiate a payment simulation to confirm the booking.

---

## 8. Hotel Reservation Module (hotel.py) 🏨

- **Information Collection:**  
  - Request details such as city, check-in/check-out dates, and number of guests.

- **Hotel Listings:**  
  - Filter hotels from `hotels.json` based on city and dates.

- **Payment Simulation:**  
  - Once a hotel is selected, run a simulated payment process and display a reservation code if successful.

---

## 9. Car Rental Module (car.py) 🚗

- **Rental Details:**  
  - Collect information on pickup and drop-off locations/dates.

- **Car Options:**  
  - Filter available cars (economy, mid, luxury) using data from `cars.json`.

- **Additional Checks:**  
  - Optionally enforce restrictions based on driver’s license issue year, age, etc.

- **Booking Completion:**  
  - Finalize the rental reservation through a payment simulation.

---

## 10. Payment Simulation (payment.py) 💳

- **Functionality:**  
  - Simulate a payment by asking for card number, expiry date, and CVV.
  
- **Validation:**  
  - Basic checks, such as verifying the card number’s length, are performed.
  
- **Outcome:**  
  - Display a “Payment failed” message if validations do not pass.
  - If successful, show a confirmation message along with a reservation/ticket code.

---

## 11. Test Scenarios and Error Handling 🔍

- **Input Validation:**  
  - The application should display clear warnings for incorrect inputs (e.g., wrong city names, invalid dates, etc.).
  
- **Menu Navigation:**  
  - Ensure that users can repeatedly navigate through the menus and exit gracefully.

- **Payment Validation:**  
  - The system must properly handle cases of invalid card details by showing a “Payment failed” message when necessary.

---

## 12. Project Completion and Future Developments 🚧

- **Documentation:**  
  - A comprehensive README.md file is provided, summarizing installation and usage instructions.
  
- **Version Control:**  
  - Use Git to track changes and manage versions effectively.
  
- **Planned Enhancements:**  
  - Transition from JSON files to databases (SQLite, PostgreSQL, etc.).
  - Integrate real-time data via external APIs.
  - Add multilingual support and an advanced user registration system.
  - Enhance security and improve payment validation.

---

## 13. Summary and Conclusion 🎉

This CLI-based travel planner aims to provide a seamless booking experience for plane, bus, train tickets, hotel reservations, and car rentals—all from the terminal.  
- **User Roles:** Admins manage data through an admin panel, while basic users enjoy a simplified booking process.
- **Data Handling:** Uses JSON-based storage with placeholder data, setting the stage for future upgrades.
- **Payment Simulation:** A simple payment flow confirms bookings and enhances reliability.

Happy coding and safe travels! 🌍✈️🚌🚆🏨🚗
