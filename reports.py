def occupancy_report(showtimes: list, seat_maps: dict, bookings: list) -> dict:
    """
    Calculates the seat occupancy statistics for each scheduled showtime.

    Args:
        showtimes (list): List of all scheduled showtimes.
        seat_maps (dict): Dictionary containing the seat layouts for each showtime.
        bookings (list): List of all current bookings.

    Returns:
        dict: A report indexed by showtime_id containing total seats, sold seats, and occupancy rate.
    """
    report = {}
    for show in showtimes:
        s_id = show["showtime_id"]
        total_seats = len(seat_maps.get(s_id, {}))
        sold_seats = sum(1 for b in bookings if b["showtime_id"] == s_id for _ in b["seats"])
        rate = (sold_seats / total_seats * 100) if total_seats > 0 else 0
        report[s_id] = {"total": total_seats, "sold": sold_seats, "occupancy_rate": f"%{rate:.2f}"}
    return report

def revenue_summary(bookings: list, period: tuple[str, str] = None) -> dict:
    """
    Generates a summary of total earnings and ticket sales metrics.

    Args:
        bookings (list): List of all current bookings.
        period (tuple[str, str], optional): A start and end date tuple to filter revenue (logic to be implemented).

    Returns:
        dict: Summary containing total revenue, ticket count, and average price per ticket.
    """
    total_revenue = sum(b["total_price"] for b in bookings)
    ticket_count = sum(len(b["seats"]) for b in bookings)
    return {
        "total_revenue": total_revenue,
        "total_tickets_sold": ticket_count,
        "average_ticket_price": total_revenue / ticket_count if ticket_count > 0 else 0
    }

def top_movies(bookings: list, showtimes: list, limit: int = 5) -> list:
    """
    Identifies the most popular movies based on the number of tickets sold.

    Args:
        bookings (list): List of all current bookings.
        showtimes (list): List of all showtimes to map bookings to specific movies.
        limit (int): The maximum number of top movies to return. Default is 5.

    Returns:
        list: A sorted list of tuples (movie_id, ticket_count) in descending order.
    """
    movie_sales = {}
    showtime_to_movie = {s["showtime_id"]: s["movie_id"] for s in showtimes}
    for b in bookings:
        m_id = showtime_to_movie.get(b["showtime_id"])
        movie_sales[m_id] = movie_sales.get(m_id, 0) + len(b["seats"])
    sorted_movies = sorted(movie_sales.items(), key=lambda x: x[1], reverse=True)
    return sorted_movies[:limit]

def export_report(report: dict, filename: str) -> str:
    """
    Exports a generated report dictionary to a plain text file.

    Args:
        report (dict): The report data to be exported.
        filename (str): The name or path of the file to be created.

    Returns:
        str: The path of the successfully created report file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in report.items():
            f.write(f"{key}: {value}\n")
    return filename