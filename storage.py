import json
import os
import shutil
from datetime import datetime

def load_state(base_dir: str) -> tuple:
    """
    Initializes the system state by loading showtimes and bookings from JSON files.
    Dynamically reconstructs seat maps by marking seats as 'sold' based on existing bookings.

    Args:
        base_dir (str): The directory where data files are stored.

    Returns:
        tuple: A tuple containing (showtimes list, seat_maps dictionary, bookings list).
    """
    showtimes_path = os.path.join(base_dir, 'showtimes.json')
    bookings_path = os.path.join(base_dir, 'bookings.json')

    showtimes = []
    if os.path.exists(showtimes_path):
        with open(showtimes_path, 'r', encoding='utf-8') as f:
            showtimes = json.load(f)

    bookings_list = []
    if os.path.exists(bookings_path):
        with open(bookings_path, 'r', encoding='utf-8') as f:
            bookings_list = json.load(f)

    seat_maps = {}
    for s in showtimes:
        sid = s['showtime_id']
        seat_maps[sid] = {
            f"{r}{c}": {"status": "available", "price": 100.0}
            for r in ["A", "B", "C", "D"] for c in range(1, 11)
        }

    for b in bookings_list:
        sid = b['showtime_id']
        if sid in seat_maps:
            for seat in b['seats']:
                if seat in seat_maps[sid]:
                    seat_maps[sid][seat]["status"] = "sold"

    return showtimes, seat_maps, bookings_list


def save_state(base_dir: str, showtimes: list, seat_maps: dict, bookings: list) -> None:
    """
    Persists the current application state to JSON files in the specified directory.

    Args:
        base_dir (str): The target directory for saving data.
        showtimes (list): The list of current showtimes.
        seat_maps (dict): The current seat layouts and statuses.
        bookings (list): The list of all processed bookings.
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    files_data = {
        'showtimes.json': showtimes,
        'seat_maps.json': seat_maps,
        'bookings.json': bookings
    }

    for filename, data in files_data.items():
        path = os.path.join(base_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


def backup_state(base_dir: str, backup_dir: str) -> list:
    """
    Creates a timestamped backup of all JSON data files.

    Args:
        base_dir (str): The source directory containing active data files.
        backup_dir (str): The destination directory for backup copies.

    Returns:
        list: A list of full file paths for the created backup files.
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_files = []

    for filename in os.listdir(base_dir):
        if filename.endswith('.json'):
            src = os.path.join(base_dir, filename)
            dst = os.path.join(backup_dir, f"{timestamp}_{filename}")
            shutil.copy2(src, dst)
            backup_files.append(dst)
    return backup_files


def validate_showtime(showtime: dict) -> bool:
    """
    Validates that a showtime dictionary contains all required business fields.

    Args:
        showtime (dict): The showtime entry to validate.

    Returns:
        bool: True if all required keys are present, False otherwise.
    """
    required_keys = ["showtime_id", "movie_id", "theatre_screen", "date", "time"]
    return all(key in showtime for key in required_keys)