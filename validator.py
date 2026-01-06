from datetime import date, time


class Validator:
    def require_non_empty_text(self, raw_value, field_name):
        text_value = str(raw_value).strip()
        if not text_value:
            raise ValueError("{} must be non-empty.".format(field_name))
        return text_value

    def require_positive_integer(self, raw_value, field_name):
        text_value = str(raw_value).strip()
        if not text_value.isdigit():
            raise ValueError("{} must be a positive integer.".format(field_name))

        integer_value = int(text_value)
        if integer_value <= 0:
            raise ValueError("{} must be > 0.".format(field_name))

        return integer_value

    def parse_iso_date(self, raw_value):
        date_text = str(raw_value).strip()
        parts = date_text.split("-")
        if len(parts) != 3:
            raise ValueError("Date must be in format YYYY-MM-DD.")

        try:
            year, month, day = (int(part) for part in parts)
            return date(year, month, day)
        except Exception:
            raise ValueError("Invalid date.")

    def parse_hhmm_time(self, raw_value):
        time_text = str(raw_value).strip()
        parts = time_text.split(":")
        if len(parts) != 2:
            raise ValueError("Time must be in format HH:MM.")

        try:
            hours, minutes = (int(part) for part in parts)
        except Exception:
            raise ValueError("Invalid time.")

        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError("Invalid time.")

        return time(hours, minutes)

    def parse_equipment_list(self, raw_value):
        equipment_text = str(raw_value).strip()
        if not equipment_text:
            return []

        raw_items = [item.strip() for item in equipment_text.split(",") if item.strip()]

        seen_lowercase = set()
        result_items = []
        for item in raw_items:
            item_key = item.lower()
            if item_key not in seen_lowercase:
                seen_lowercase.add(item_key)
                result_items.append(item)

        return result_items
