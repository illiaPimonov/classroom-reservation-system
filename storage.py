import json
from pathlib import Path
from reservation_book import reservation_book_from_dict


class Storage:
    def save_to_file(self, reservation_book, filename):
        file_path = Path(filename)
        book_data = reservation_book.to_dict()

        try:
            file_path.write_text(
                json.dumps(book_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as error:
            raise OSError("Failed to save file: {}".format(error))

    def load_from_file(self, filename):
        file_path = Path(filename)

        try:
            raw_text = file_path.read_text(encoding="utf-8")
            book_data = json.loads(raw_text)

            if not isinstance(book_data, dict):
                raise ValueError("Invalid file format (root must be a JSON object).")

            return reservation_book_from_dict(book_data)

        except FileNotFoundError:
            raise FileNotFoundError("File not found: {}".format(filename))
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON: {}".format(error))
        except OSError as error:
            raise OSError("Failed to read file: {}".format(error))
