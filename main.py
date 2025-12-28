import movies
import seating
import bookings
import storage
import reports

def main():
    """
    The entry point of the application.
    Initializes the system state and manages the primary navigation loop
    between Customer and Admin roles.
    """
    base_dir = 'data/'
    # Load initial data from storage
    showtimes, seat_maps, bookings_list = storage.load_state(base_dir)
    all_movies = movies.load_movies(f"{base_dir}movies.json")

    while True:
        print("\n=== MOVIE TICKET BOOKING SYSTEM ===")
        print("1. Customer Menu")
        print("2. Admin Menu")
        print("3. Exit")
        choice = input("Select Role: ")

        if choice == '1':
            customer_flow(showtimes, seat_maps, bookings_list, base_dir)
        elif choice == '2':
            admin_flow(all_movies, showtimes, seat_maps, bookings_list, base_dir)
        elif choice == '3':
            # Save final state before closing
            storage.save_state(base_dir, showtimes, seat_maps, bookings_list)
            print("System closed. Data saved.")
            break

def customer_flow(showtimes, seat_maps, bookings_list, base_dir):
    """
    Handles the customer-facing interface for viewing shows,
    booking seats, and cancelling existing tickets.
    """
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. List Showtimes & Book Ticket")
        print("2. Cancel Booking")
        print("3. Back to Main Menu")
        choice = input("Select: ")

        if choice == '1':
            # List available showtimes
            active_shows = movies.list_showtimes(showtimes)
            for s in active_shows:
                print(f"{s['showtime_id']} {s['date']} {s['time']} - {s['theatre_screen']}")

            sid = input("\nEnter Showtime ID: ")
            if sid not in seat_maps:
                print("ERROR: Invalid Showtime ID.")
                continue

            # Display visual seat map
            print(seating.render_seat_map(seat_maps[sid]))

            seat_code = input("Select Seat: ").upper()
            if not seating.is_seat_available(seat_maps[sid], seat_code):
                print("ERROR: Seat is already sold, reserved, or invalid.")
                continue

            # Finalize booking with confirmation
            confirm = input(f"Confirm booking for {seat_code}? (y/n): ")
            if confirm.lower() == 'y':
                seating.reserve_seat(seat_maps[sid], seat_code)
                email = input("Enter email: ")

                new_res = {
                    "showtime_id": sid,
                    "seats": [seat_code],
                    "customer_email": email,
                    "total_price": 100.0,
                    "status": "Confirmed"
                }
                final_res = bookings.create_booking(showtimes, seat_maps, new_res)
                bookings_list.append(final_res)
                storage.save_state(base_dir, showtimes, seat_maps, bookings_list)
                print(f"Success! Booking ID: {final_res['booking_id']}")

        elif choice == '2':
            # Cancellation with ID verification and confirmation
            bid = input("Enter Booking ID to cancel: ")
            confirm = input(f"Are you sure you want to cancel {bid}? (y/n): ")
            if confirm.lower() == 'y':
                if bookings.cancel_booking(bookings_list, bid, seat_maps):
                    storage.save_state(base_dir, showtimes, seat_maps, bookings_list)
                    print("Cancellation successful.")
                else:
                    print("ERROR: Booking ID not found.")

        elif choice == '3':
            break

def admin_flow(all_movies, showtimes, seat_maps, bookings_list, base_dir):
    """
    Handles administrative tasks such as adding movies,
    scheduling new showtimes, and viewing occupancy reports.
    """
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add Movie")
        print("2. Schedule Showtime")
        print("3. View Occupancy Report")
        print("4. Back to Main Menu")
        choice = input("Select: ")

        if choice == '1':
            # Add a new movie to the catalog
            m_data = {"id": input("ID: "), "title": input("Title: ")}
            movies.add_movie(all_movies, m_data)
            movies.save_movies(f"{base_dir}movies.json", all_movies)
            print("Movie added.")

        elif choice == '2':
            # Schedule a movie for a specific time and screen
            sid = input("Showtime ID: ")
            st_data = {
                "showtime_id": sid,
                "movie_id": input("Movie ID: "),
                "theatre_screen": input("Screen Name: "),
                "date": input("Date (YYYY-MM-DD): "),
                "time": input("Time (HH:MM): ")
            }
            movies.schedule_showtime(showtimes, st_data)
            # Initialize a fresh seat map for the new showtime
            seat_maps[sid] = seating.initialize_seat_map({"rows": ["A", "B", "C"], "cols": 10})
            storage.save_state(base_dir, showtimes, seat_maps, bookings_list)
            print("Showtime scheduled.")

        elif choice == '3':
            # Generate and display a report of current seat occupancy
            report = reports.occupancy_report(showtimes, seat_maps, bookings_list)
            for sid, data in report.items():
                print(f"Show {sid}: {data['occupancy_rate']} full ({data['sold']}/{data['total']} seats)")

        elif choice == '4':
            break

if __name__ == "__main__":
    main()