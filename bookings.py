import uuid

def calculate_booking_total(seats: list[str], pricing: dict, tax_rate: float, discounts: list[dict] = None) -> dict:
    """
    Calculates the total booking amount including base price, discounts, and taxes.

    Args:
        seats (list[str]): List of selected seat codes (e.g., ['A1', 'A2']).
        pricing (dict): Mapping of seat codes or categories to their respective prices.
        tax_rate (float): The tax percentage to be applied (e.g., 0.18).
        discounts (list[dict], optional): List of discount dictionaries containing 'rate'.

    Returns:
        dict: A breakdown containing base_price, discount amount, tax amount, and final total.
    """
    base_price = sum(pricing.get(seat, pricing.get("standard", 0)) for seat in seats)
    total_discount = 0
    if discounts:
        for d in discounts:
            total_discount += base_price * d.get("rate", 0)

    subtotal = base_price - total_discount
    tax_amount = subtotal * tax_rate
    total_price = subtotal + tax_amount

    return {
        "base_price": base_price,
        "discount": total_discount,
        "tax": tax_amount,
        "total": total_price
    }


def create_booking(showtimes: list, seat_maps: dict, booking_data: dict) -> dict:
    """
    Generates a unique booking ID and updates the seat map to mark seats as sold.

    Args:
        showtimes (list): List of all available showtimes.
        seat_maps (dict): Dictionary containing seat layouts for each showtime.
        booking_data (dict): Dictionary containing showtime_id and selected seats.

    Returns:
        dict: The updated booking data with a newly generated 'booking_id'.
    """
    booking_id = str(uuid.uuid4())[:8].upper()
    booking_data["booking_id"] = booking_id

    showtime_id = booking_data["showtime_id"]
    seat_map = seat_maps.get(showtime_id)

    for seat in booking_data["seats"]:
        seat_map[seat]["status"] = "sold"

    return booking_data


def cancel_booking(bookings: list, booking_id: str, seat_maps: dict) -> bool:
    """
    Cancels an existing booking and reverts the status of its seats to 'available'.

    Args:
        bookings (list): List of current active bookings.
        booking_id (str): The unique ID of the booking to be cancelled.
        seat_maps (dict): Dictionary containing seat layouts to be updated.

    Returns:
        bool: True if the cancellation was successful, False if the booking_id was not found.
    """
    for i, b in enumerate(bookings):
        if b["booking_id"] == booking_id:
            showtime_id = b["showtime_id"]
            for seat in b["seats"]:
                seat_maps[showtime_id][seat]["status"] = "available"
            bookings.pop(i)
            return True
    return False


def list_customer_bookings(bookings: list, email: str) -> list:
    """
    Filters and returns all bookings associated with a specific customer email.

    Args:
        bookings (list): List of all bookings.
        email (str): Customer's email address to filter by.

    Returns:
        list: A list of bookings belonging to the specified customer.
    """
    return [b for b in bookings if b["email"] == email]


def generate_ticket(booking: dict, directory: str) -> str:
    """
    Creates a physical text file representing the ticket for a confirmed booking.

    Args:
        booking (dict): The booking details used to populate the ticket.
        directory (str): The folder path where the ticket file will be saved.

    Returns:
        str: The full file path of the generated ticket.
    """
    ticket_content = f"TICKET ID: {booking['booking_id']}\nSHOW: {booking['showtime_id']}\nSEATS: {','.join(booking['seats'])}\nTOTAL: {booking['total_price']}"
    filename = f"{directory}/ticket_{booking['booking_id']}.txt"
    with open(filename, "w") as f:
        f.write(ticket_content)
    return filename