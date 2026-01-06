from classroom import Classroom
from reservation import Reservation


def create_new_book(app_context):
    app_context.reservation_book.clear_all()
    print("Created a new empty reservation book.")


def save_book_to_file(app_context, read_user_input):
    filename = app_context.validator.require_non_empty_text(
        read_user_input("Filename to save (e.g. data.json): "),
        "Filename",
    )
    app_context.storage.save_to_file(app_context.reservation_book, filename)
    print("Saved to {}".format(filename))


def load_book_from_file(app_context, read_user_input):
    filename = app_context.validator.require_non_empty_text(
        read_user_input("Filename to load: "),
        "Filename",
    )
    app_context.reservation_book = app_context.storage.load_from_file(filename)
    print("Loaded from {}".format(filename))


def add_classroom(app_context, read_user_input):
    room_id = app_context.validator.require_non_empty_text(
        read_user_input("Room identifier (e.g. B101): "),
        "Room ID",
    )
    building_name = app_context.validator.require_non_empty_text(
        read_user_input("Building name: "),
        "Building",
    )
    capacity = app_context.validator.require_positive_integer(
        read_user_input("Capacity (int > 0): "),
        "Capacity",
    )
    equipment_list = app_context.validator.parse_equipment_list(
        read_user_input("Equipment (comma-separated, can be empty): ")
    )

    classroom = Classroom(
        room_id=room_id,
        building_name=building_name,
        capacity=capacity,
        equipment_list=equipment_list,
    )
    app_context.reservation_book.add_classroom(classroom)
    print("Classroom added.")


def add_reservation(app_context, read_user_input):
    room_id = app_context.validator.require_non_empty_text(read_user_input("Room identifier: "), "Room ID")
    person_name = app_context.validator.require_non_empty_text(read_user_input("Person name: "), "Person")
    reservation_purpose = app_context.validator.require_non_empty_text(read_user_input("Purpose: "), "Purpose")
    reservation_date = app_context.validator.parse_iso_date(read_user_input("Date (YYYY-MM-DD): "))
    start_time = app_context.validator.parse_hhmm_time(read_user_input("Start time (HH:MM): "))
    end_time = app_context.validator.parse_hhmm_time(read_user_input("End time (HH:MM): "))

    reservation = Reservation(
        room_id=room_id,
        person_name=person_name,
        reservation_purpose=reservation_purpose,
        reservation_date=reservation_date,
        start_time=start_time,
        end_time=end_time,
    )
    app_context.reservation_book.add_reservation(reservation)
    print("Reservation added.")


def show_classrooms(app_context):
    classroom_list = app_context.reservation_book.list_classrooms()
    if not classroom_list:
        print("No classrooms.")
        return

    for classroom in classroom_list:
        equipment_text = ", ".join(classroom.equipment_list) if classroom.equipment_list else "-"
        print("- {} | {} | cap={} | eq={}".format(
            classroom.room_id,
            classroom.building_name,
            classroom.capacity,
            equipment_text,
        ))


def show_reservations(app_context, read_user_input):
    print("Filter: 1) none  2) by room  3) by date")
    filter_choice = read_user_input("Choose filter: ")

    if filter_choice == "1":
        reservation_list = app_context.reservation_book.list_reservations()
    elif filter_choice == "2":
        room_id = app_context.validator.require_non_empty_text(read_user_input("Room identifier: "), "Room ID")
        reservation_list = app_context.reservation_book.list_reservations(room_id=room_id)
    elif filter_choice == "3":
        reservation_date = app_context.validator.parse_iso_date(read_user_input("Date (YYYY-MM-DD): "))
        reservation_list = app_context.reservation_book.list_reservations(reservation_date=reservation_date)
    else:
        print("Unknown filter; showing all.")
        reservation_list = app_context.reservation_book.list_reservations()

    if not reservation_list:
        print("No reservations.")
        return

    for number, reservation in enumerate(reservation_list, start=1):
        print("{} ) {} {}-{} | room={} | {} | {}".format(
            number,
            reservation.reservation_date.isoformat(),
            reservation.start_time.strftime("%H:%M"),
            reservation.end_time.strftime("%H:%M"),
            reservation.room_id,
            reservation.person_name,
            reservation.reservation_purpose,
        ))


def remove_reservation(app_context, read_user_input):
    print("You can remove from a filtered list.")
    print("Filter: 1) none  2) by room  3) by date")
    filter_choice = read_user_input("Choose filter: ")

    selected_room_id = None
    selected_date = None

    if filter_choice == "2":
        selected_room_id = app_context.validator.require_non_empty_text(
            read_user_input("Room identifier: "),
            "Room ID",
        )
    elif filter_choice == "3":
        selected_date = app_context.validator.parse_iso_date(read_user_input("Date (YYYY-MM-DD): "))

    visible_reservations = app_context.reservation_book.list_reservations(
        room_id=selected_room_id,
        reservation_date=selected_date,
    )

    if not visible_reservations:
        print("No reservations.")
        return

    for number, reservation in enumerate(visible_reservations, start=1):
        print("{} ) {} {}-{} | room={} | {} | {}".format(
            number,
            reservation.reservation_date.isoformat(),
            reservation.start_time.strftime("%H:%M"),
            reservation.end_time.strftime("%H:%M"),
            reservation.room_id,
            reservation.person_name,
            reservation.reservation_purpose,
        ))

    reservation_number = app_context.validator.require_positive_integer(
        read_user_input("Enter reservation number to remove: "),
        "Index",
    )

    removed = app_context.reservation_book.remove_reservation(
        reservation_number,
        room_id=selected_room_id,
        reservation_date=selected_date,
    )

    print("Removed: {} {}-{} room={}".format(
        removed.reservation_date.isoformat(),
        removed.start_time.strftime("%H:%M"),
        removed.end_time.strftime("%H:%M"),
        removed.room_id,
    ))


def remove_all_reservations(app_context):
    app_context.reservation_book.remove_all_reservations()
    print("All reservations removed.")


def delete_reservation_book(app_context):
    app_context.reservation_book.clear_all()
    print("Reservation book deleted (classrooms + reservations).")
