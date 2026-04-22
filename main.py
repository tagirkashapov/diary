import pathlib
import json
import datetime


class Diary:
    def __init__(self, filename):
        self.filename = filename
        pathlib.Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
        self.entries = self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Oшибка при загрузке: {e}")
            return []

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    def add(self, text):
        current_id = 0
        if self.entries:
            current_id = self.entries[-1]['id']
        entry = {
            'id': current_id+1,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': text
        }
        self.entries.append(entry)
        self.save()
        print("Запись добавлена\n")

    def delete(self, id):
        for entry in self.entries:
            if entry['id'] == id:
                self.entries.remove(entry)
                self.save()
                print("Запись удалена\n")
                return True
        print("Запись не найдена\n")
        return False

    def print_entries(self):
        if self.entries:
            print("Ваши записи:")
            for entry in self.entries:
                print(f'[{entry['id']}] {entry['date']} - {entry['text']}')
        else:
            print("Записи не найдены")
        print()


if __name__ == '__main__':
    diary = Diary('entries/diary.json')

    while True:
        print("=== Личный дневник ===\n1. Добавить запись\n2. Показать все записи\n3. Удалить запись\n4. Выйти")
        choice = input("Выберите действие: ")
        print()

        match choice:
            case '1':
                text = input("Введите текст записи: ")
                diary.add(text)
            case '2':
                diary.print_entries()
            case '3':
                id = int(input("Введите id записи, которую хотите удалить: "))
                diary.delete(id)
            case '4':
                break
