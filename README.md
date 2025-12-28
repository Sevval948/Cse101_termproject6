# Movie Ticket Booking System

A modular Python-based CLI application for managing movie theater showtimes, seat reservations, and sales reporting. This system is designed with a clear separation of concerns, featuring dedicated modules for movies, bookings, seating, and storage.

## Features

* **Dual-Role Access:** Separate workflows for Customers (viewing/booking/cancelling) and Admins (adding movies, scheduling, and reporting).
* **Dynamic Seating Map:** Real-time visual representation of theater seats with status indicators (`.` for available, `R` for reserved, `X` for sold).
* **State Persistence:** Automatic loading and saving of system data using JSON files.
* **Validation Logic:** Prevents double-booking and validates user inputs during the booking process.
* **Reporting:** Administrative tools to view occupancy rates and revenue summaries.
* **Backup System:** Includes functionality to create timestamped backups of the entire database.

## Project Structure

```text
├── main.py            # Entry point of the application
├── movies.py          # Movie catalog and showtime scheduling logic
├── bookings.py        # Ticket reservation, total calculation, and cancellation
├── seating.py         # Seat map initialization and rendering
├── storage.py         # JSON data handling, state persistence, and backups
├── reports.py         # Occupancy and sales report generation
├── tests.py           # Unit tests for core business logic
└── data/              # Directory for JSON database files

```

## Installation and Usage

1. **Prerequisites:** Ensure you have Python 3.10+ installed.
2. **Navigate to Project:** Open your terminal and go to the project directory.
3. **Run the Application:**
```bash
python main.py

```


4. **Run Tests:**
To verify the system logic and validation rules:
```bash
python -m unittest tests.py -v

```



## Testing Coverage

The system includes automated unit tests for:

* **Seat Availability:** Ensuring valid selection and preventing overlapping bookings.
* **Price Calculation:** Accurate total computation including base prices.
* **Cancellation Flow:** Verifying that seats are correctly released back to 'available' status upon cancellation.

## Configuration

* **Database:** Data is stored in `data/movies.json`, `data/showtimes.json`, and `data/bookings.json`.
* **Seating:** Default theater size is configurable via `seating.py`.

---
