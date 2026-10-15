"""Manage seat reservations for a small movie theater."""

import hashlib
import json
import os


SHOWS = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a valid seat and optionally record the operation in system_logs."""
    if system_logs is None:
        system_logs = []

    if show_id not in SHOWS:
        system_logs.append(f"Unknown show: {show_id}")
        return False

    show = SHOWS[show_id]
    if not isinstance(seat_number, int) or isinstance(seat_number, bool):
        system_logs.append("Seat number must be an integer")
        return False
    if not 1 <= seat_number <= show["seats"]:
        system_logs.append(f"Seat number must be between 1 and {show['seats']}")
        return False
    if seat_number in show["booked"]:
        system_logs.append(f"Seat {seat_number} already taken for {show_id}")
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat; return False if the show or seat is not found."""
    if show_id not in SHOWS:
        return False
    try:
        SHOWS[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False
    return True


def ticket_code(show_id, seat_number):
    """Return a short SHA-256-based ticket identifier."""
    ticket_data = f"{show_id}:{seat_number}".encode("utf-8")
    return hashlib.sha256(ticket_data).hexdigest()[:8]


def dump_reservations(file_path="seats.json"):
    """Save the current seating plan as JSON using a context manager."""
    with open(file_path, "w", encoding="utf-8") as reservation_file:
        json.dump(SHOWS, reservation_file, indent=2)
    try:
        os.chmod(file_path, 0o600)
    except OSError:
        # File permissions may not be supported on every platform.
        pass


def load_reservations(file_path="seats.json"):
    """Load seating data from JSON, leaving current data unchanged on failure."""
    global SHOWS
    with open(file_path, "r", encoding="utf-8") as reservation_file:
        loaded_shows = json.load(reservation_file)

    if not isinstance(loaded_shows, dict):
        raise ValueError("Reservation data must be a JSON object")
    SHOWS = loaded_shows


def print_seating_summary():
    """Print the number of free seats and the booked seats for each show."""
    for show in SHOWS.values():
        free_seats = show["seats"] - len(show["booked"])
        print(
            f"{show['title']}: {free_seats} seats free, "
            f"booked = {show['booked']}"
        )


def main():
    """Demonstrate reservations, persistence, and the seating summary."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    print("Ticket code:", ticket_code("SHOW-1", 5))

    seat_input = input("Seat number to book for SHOW-2 (Enter for 4): ").strip()
    try:
        seat_number = int(seat_input) if seat_input else 4
    except ValueError:
        print("Invalid input: enter a whole-number seat number.")
    else:
        reserve_seat("SHOW-2", seat_number, logs)

    dump_reservations()
    load_reservations()
    print_seating_summary()


if __name__ == "__main__":
    main()
