import csv


class CSVReader:
    """
    Читает данные из CSV файла
    """

    @classmethod
    def read_file(cls, file_name) -> list:
        with open(file_name, 'r', newline='', encoding='utf-8') as f:
            csv_data = []
            csv_in = csv.reader(f)
            for line in csv_in:
                for l in line:
                    csv_data.append(l)
            return csv_data
