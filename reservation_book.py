from errors import ReservationConflictError, NotFoundError
from classroom import classroom_from_dict
from reservation import reservation_from_dict


class ReservationBook:
    def __init__(self):
        self.classrooms_by_id = {}
        self.reservation_list = []

    def add_classroom(self, classroom):
        if classroom.room_id in self.classrooms_by_id:
            raise ValueError("Classroom '{}' already exists.".format(classroom.room_id))
        self.classrooms_by_id[classroom.room_id] = classroom

    def list_classrooms(self):
        return sorted(
            self.classrooms_by_id.values(),
            key=lambda classroom: (classroom.building_name, classroom.room_id),
        )

    def _time_intervals_overlap(self, first_start, first_end, second_start, second_end):
        return first_start < second_end and second_start < first_end

    def _check_reservation_conflicts(self, new_reservation):
        for existing_reservation in self.reservation_list:
            if existing_reservation == new_reservation:
                raise ReservationConflictError("Duplicate reservation: identical reservation already exists.")

            same_room = existing_reservation.room_id == new_reservation.room_id
            same_date = existing_reservation.reservation_date == new_reservation.reservation_date

            if same_room and same_date:
                exactly_same_interval = (
                    existing_reservation.start_time == new_reservation.start_time
                    and existing_reservation.end_time == new_reservation.end_time
                )
                if exactly_same_interval:
                    raise ReservationConflictError(
                        "Conflict: room '{}' is already reserved on {} for exactly {}-{}.".format(
                            new_reservation.room_id,
                            new_reservation.reservation_date.isoformat(),
                            new_reservation.start_time.strftime("%H:%M"),
                            new_reservation.end_time.strftime("%H:%M"),
                        )
                    )

                overlapping_time = self._time_intervals_overlap(
                    existing_reservation.start_time,
                    existing_reservation.end_time,
                    new_reservation.start_time,
                    new_reservation.end_time,
                )
                if overlapping_time:
                    raise ReservationConflictError(
                        "Conflict: room '{}' is already reserved on {} {}-{} by {} ({}).".format(
                            new_reservation.room_id,
                            new_reservation.reservation_date.isoformat(),
                            existing_reservation.start_time.strftime("%H:%M"),
                            existing_reservation.end_time.strftime("%H:%M"),
                            existing_reservation.person_name,
                            existing_reservation.reservation_purpose,
                        )
                    )

            same_person = existing_reservation.person_name == new_reservation.person_name
            if same_person and same_date:
                overlapping_time = self._time_intervals_overlap(
                    existing_reservation.start_time,
                    existing_reservation.end_time,
                    new_reservation.start_time,
                    new_reservation.end_time,
                )
                if overlapping_time:
                    raise ReservationConflictError(
                        "Conflict: '{}' already has a reservation on {} {}-{} in room '{}' ({}).".format(
                            new_reservation.person_name,
                            new_reservation.reservation_date.isoformat(),
                            existing_reservation.start_time.strftime("%H:%M"),
                            existing_reservation.end_time.strftime("%H:%M"),
                            existing_reservation.room_id,
                            existing_reservation.reservation_purpose,
                        )
                    )

    def add_reservation(self, reservation):
        reservation.room_id = reservation.room_id.strip()
        reservation.person_name = reservation.person_name.strip()
        reservation.reservation_purpose = reservation.reservation_purpose.strip()

        if reservation.room_id not in self.classrooms_by_id:
            raise NotFoundError("Classroom '{}' does not exist.".format(reservation.room_id))

        if reservation.start_time >= reservation.end_time:
            raise ValueError("Start time must be earlier than end time.")

        self._check_reservation_conflicts(reservation)
        self.reservation_list.append(reservation)

    def list_reservations(self, room_id=None, reservation_date=None):
        filtered_reservations = self.reservation_list

        if room_id is not None:
            filtered_reservations = [
                reservation for reservation in filtered_reservations
                if reservation.room_id == room_id
            ]

        if reservation_date is not None:
            filtered_reservations = [
                reservation for reservation in filtered_reservations
                if reservation.reservation_date == reservation_date
            ]

        return sorted(
            filtered_reservations,
            key=lambda reservation: (reservation.reservation_date, reservation.room_id, reservation.start_time),
        )

    def remove_reservation(self, reservation_number, room_id=None, reservation_date=None):
        visible_reservations = self.list_reservations(room_id=room_id, reservation_date=reservation_date)

        if reservation_number < 1 or reservation_number > len(visible_reservations):
            raise NotFoundError("Reservation index out of range.")

        reservation_to_remove = visible_reservations[reservation_number - 1]

        for index_in_master, reservation in enumerate(self.reservation_list):
            if reservation == reservation_to_remove:
                return self.reservation_list.pop(index_in_master)

        raise NotFoundError("Reservation not found.")

    def remove_all_reservations(self):
        self.reservation_list.clear()

    def clear_all(self):
        self.classrooms_by_id.clear()
        self.reservation_list.clear()

    def to_dict(self):
        return {
            "classrooms": [classroom.to_dict() for classroom in self.list_classrooms()],
            "reservations": [reservation.to_dict() for reservation in self.list_reservations()],
        }


def reservation_book_from_dict(book_data):
    reservation_book = ReservationBook()

    for classroom_data in book_data.get("classrooms", []):
        classroom = classroom_from_dict(classroom_data)
        reservation_book.classrooms_by_id[classroom.room_id] = classroom

    for reservation_data in book_data.get("reservations", []):
        reservation = reservation_from_dict(reservation_data)
        reservation_book.add_reservation(reservation)

    return reservation_book
