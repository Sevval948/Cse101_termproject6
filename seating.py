def initialize_seat_map(screen_config: dict) -> dict:
    """
    Creates a new seat map based on the provided screen dimensions and row labels.

    Args:
        screen_config (dict): Configuration containing "rows" (list of letters)
                             and "cols" (integer number of columns).

    Returns:
        dict: A dictionary mapping seat codes (e.g., 'A1') to their status and price multiplier.
    """
    rows = screen_config.get("rows", ["A", "B", "C", "D", "E", "F", "G", "H"])
    cols = screen_config.get("cols", 12)
    seat_map = {}
    for row in rows:
        for col in range(1, cols + 1):
            seat_code = f"{row}{col}"
            seat_map[seat_code] = {"status": "available", "price_multiplier": 1.0}
    return seat_map

def render_seat_map(seat_map: dict) -> str:
    """
    Generates a visual string representation of the theater layout for the CLI.

    Args:
        seat_map (dict): The current state of seats for a specific showtime.

    Returns:
        str: A formatted string showing the grid layout and a status legend.
    """
    rows = sorted(list(set(code[0] for code in seat_map.keys())))
    cols = sorted(list(set(int(code[1:]) for code in seat_map.keys())))
    legend = "\nLEGEND: [.] Available  [R] Reserved  [X] Sold\n"
    output = "   " + " ".join(f"{c:2}" for c in cols) + "\n"
    for row in rows:
        row_str = f"{row}  "
        for col in cols:
            code = f"{row}{col}"
            status = seat_map[code]["status"]
            char = "." if status == "available" else "R" if status == "reserved" else "X"
            row_str += f"{char}  "
        output += row_str + "\n"
    return legend + output

def is_seat_available(seat_map: dict, seat_code: str) -> bool:
    """
    Checks if a specific seat is currently available for booking.

    Args:
        seat_map (dict): The seat layout dictionary.
        seat_code (str): The unique code of the seat (e.g., 'B5').

    Returns:
        bool: True if the seat exists and is 'available', False otherwise.
    """
    return seat_map.get(seat_code, {}).get("status") == "available"

def reserve_seat(seat_map: dict, seat_code: str) -> dict:
    """
    Changes the status of a seat to 'reserved' if it is available.

    Args:
        seat_map (dict): The seat layout dictionary.
        seat_code (str): The unique code of the seat to reserve.

    Returns:
        dict: The updated seat map.
    """
    if is_seat_available(seat_map, seat_code):
        seat_map[seat_code]["status"] = "reserved"
    return seat_map

def release_seat(seat_map: dict, seat_code: str) -> dict:
    """
    Reverts a seat status back to 'available'.

    Args:
        seat_map (dict): The seat layout dictionary.
        seat_code (str): The unique code of the seat to release.

    Returns:
        dict: The updated seat map.
    """
    if seat_code in seat_map:
        seat_map[seat_code]["status"] = "available"
    return seat_map