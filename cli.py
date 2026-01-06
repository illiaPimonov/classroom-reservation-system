from reservation_book import ReservationBook
from errors import ReservationConflictError, NotFoundError
from validator import Validator
from storage import Storage
import handlers


MENU_TEXT = """
=== Classroom Reservation System ===
1) Create new reservation book (clear current)
2) Save reservation book to file
3) Load reservation book from file
4) Insert new classroom
5) Insert new reservation
6) Display all classrooms
7) Display reservations (all / filter by room / filter by date)
8) Remove a reservation (optionally filtered list)
9) Remove ALL reservations
10) Delete reservation book completely (classrooms + reservations)
0) Exit
"""


class AppContext:
    def __init__(self):
        self.reservation_book = ReservationBook()
        self.validator = Validator()
        self.storage = Storage()


def read_user_input(prompt_text):
    try:
        return input(prompt_text).strip()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        raise SystemExit


def run_cli():
    app_context = AppContext()

    command_handlers = {
        "1": lambda: handlers.create_new_book(app_context),
        "2": lambda: handlers.save_book_to_file(app_context, read_user_input),
        "3": lambda: handlers.load_book_from_file(app_context, read_user_input),
        "4": lambda: handlers.add_classroom(app_context, read_user_input),
        "5": lambda: handlers.add_reservation(app_context, read_user_input),
        "6": lambda: handlers.show_classrooms(app_context),
        "7": lambda: handlers.show_reservations(app_context, read_user_input),
        "8": lambda: handlers.remove_reservation(app_context, read_user_input),
        "9": lambda: handlers.remove_all_reservations(app_context),
        "10": lambda: handlers.delete_reservation_book(app_context),
    }

    while True:
        print(MENU_TEXT)
        user_choice = read_user_input("Choose an option: ")

        if user_choice == "0":
            print("Bye!")
            return

        selected_handler = command_handlers.get(user_choice)
        if selected_handler is None:
            print("Unknown option.")
            continue

        try:
            selected_handler()
        except ReservationConflictError as error:
            print("[CONFLICT] {}".format(error))
        except (ValueError, NotFoundError, OSError, FileNotFoundError) as error:
            print("[ERROR] {}".format(error))
