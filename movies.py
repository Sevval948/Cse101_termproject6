import json
import os

def load_movies(path: str) -> list:
    """
    Loads the movie database from a JSON file.

    Args:
        path (str): The file path to the movies JSON file.

    Returns:
        list: A list of dictionaries containing movie information.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_movies(path: str, movies: list) -> None:
    """
    Saves the current list of movies to a JSON file.

    Args:
        path (str): The file path where the movies should be saved.
        movies (list): The list of movie dictionaries to persist.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(movies, file, indent=4)

def load_showtimes(path: str) -> list:
    """
    Loads showtime schedules from a JSON file.
    Returns an empty list if the file does not exist.

    Args:
        path (str): The file path to the showtimes JSON file.

    Returns:
        list: A list of showtime dictionaries.
    """
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def add_movie(movies: list, movie_data: dict) -> dict:
    """
    Adds a new movie entry to the movies list.

    Args:
        movies (list): The existing list of movies.
        movie_data (dict): Data for the new movie (id, title, etc.).

    Returns:
        dict: The newly added movie data.
    """
    movies.append(movie_data)
    return movie_data

def schedule_showtime(showtimes: list, showtime_data: dict) -> dict:
    """
    Adds a new showtime entry to the schedule.

    Args:
        showtimes (list): The existing list of showtimes.
        showtime_data (dict): Details of the showtime (id, movie_id, time, etc.).

    Returns:
        dict: The newly scheduled showtime data.
    """
    showtimes.append(showtime_data)
    return showtime_data

def list_showtimes(showtimes: list, movie_id: str | None = None, date: str | None = None) -> list:
    """
    Filters the showtimes list based on movie ID and/or date.

    Args:
        showtimes (list): The list of showtimes to filter.
        movie_id (str, optional): Filter by a specific movie ID.
        date (str, optional): Filter by a specific date (YYYY-MM-DD).

    Returns:
        list: A list of showtimes matching the criteria.
    """
    filtered_showtimes = []

    for show in showtimes:
        if movie_id and show.get("movie_id") != movie_id:
            continue

        if date and show.get("date") != date:
            continue

        filtered_showtimes.append(show)

    return filtered_showtimes

def update_showtime(showtimes: list, showtime_id: str, updates: dict) -> dict:
    """
    Updates an existing showtime with new information.

    Args:
        showtimes (list): The list containing showtimes.
        showtime_id (str): The unique ID of the showtime to update.
        updates (dict): A dictionary of fields to update.

    Returns:
        dict: The updated showtime dictionary, or an empty dict if not found.
    """
    for show in showtimes:
        if show.get("showtime_id") == showtime_id:
            show.update(updates)
            return show
    return {}