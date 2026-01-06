class Classroom:
    def __init__(self, room_id, building_name, capacity, equipment_list=None):
        self.room_id = room_id
        self.building_name = building_name
        self.capacity = capacity
        self.equipment_list = equipment_list if equipment_list is not None else []

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "building": self.building_name,
            "capacity": self.capacity,
            "equipment": list(self.equipment_list),
        }

    def __eq__(self, other):
        return (
            isinstance(other, Classroom)
            and self.room_id == other.room_id
            and self.building_name == other.building_name
            and self.capacity == other.capacity
            and self.equipment_list == other.equipment_list
        )


def classroom_from_dict(classroom_data):
    return Classroom(
        room_id=str(classroom_data["room_id"]),
        building_name=str(classroom_data["building"]),
        capacity=int(classroom_data["capacity"]),
        equipment_list=[str(item) for item in classroom_data.get("equipment", [])],
    )
