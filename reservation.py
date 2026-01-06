from datetime import date, time


class Reservation:
    def __init__(self, room_id, person_name, reservation_purpose, reservation_date, start_time, end_time):
        self.room_id = room_id
        self.person_name = person_name
        self.reservation_purpose = reservation_purpose
        self.reservation_date = reservation_date
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "person": self.person_name,
            "purpose": self.reservation_purpose,
            "date": self.reservation_date.isoformat(),
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M"),
        }

    def __eq__(self, other):
        return (
            isinstance(other, Reservation)
            and self.room_id == other.room_id
            and self.person_name == other.person_name
            and self.reservation_purpose == other.reservation_purpose
            and self.reservation_date == other.reservation_date
            and self.start_time == other.start_time
            and self.end_time == other.end_time
        )


def reservation_from_dict(reservation_data):
    year, month, day = [int(part) for part in str(reservation_data["date"]).split("-")]
    start_hour, start_minute = [int(part) for part in str(reservation_data["start_time"]).split(":")]
    end_hour, end_minute = [int(part) for part in str(reservation_data["end_time"]).split(":")]

    return Reservation(
        room_id=str(reservation_data["room_id"]),
        person_name=str(reservation_data["person"]),
        reservation_purpose=str(reservation_data["purpose"]),
        reservation_date=date(year, month, day),
        start_time=time(start_hour, start_minute),
        end_time=time(end_hour, end_minute),
    )
