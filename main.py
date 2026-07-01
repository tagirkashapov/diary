from pathlib import Path
import json
from datetime import datetime


class Diary:
    def __init__(self):
        self.filename = Path(__file__).parent / 'diary.json'
        self.entries = self.load_entries()

    def load_entries(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Oшибка при загрузке: {e}")
            return []

    def save_entries(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    def add_entry(self, text):
        current_id = 0
        if self.entries:
            current_id = self.entries[-1]['id']
        entry = {
            'id': current_id+1,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': text
        }
        self.entries.append(entry)
        self.save_entries()

    def delete_entry(self, id):
        for entry in self.entries:
            if entry['id'] == id:
                self.entries.remove(entry)
                self.save_entries()
                return True
        return False

    def display_entries(self):
        for entry in self.entries:
            print(f"[{entry['id']}] {entry['date']} - {entry['text']}")

    def run(self):
        while True:
            print("=== Личный дневник ===")
            print("1. Добавить запись")
            print("2. Показать все записи")
            print("3. Удалить запись")
            print("4. Выйти")
            choice = input("Выберите действие: ")
            print()

            match choice:
                case '1':
                    text = input("Введите текст записи: ")
                    if not text.strip():
                        print("Ошибка: текст не должен быть пустым\n")
                        continue
                    self.add_entry(text)
                    print("Запись добавлена\n")
                case '2':
                    if not self.entries:
                        print("Записи не найдены\n")
                        continue
                    print("Ваши записи:")
                    self.display_entries()
                    print()
                case '3':
                    try:
                        id = int(input("Введите id записи, которую хотите удалить: "))
                        if id <= 0:
                            print("Ошибка: число должно быть положительным\n")
                            continue
                        if not self.delete_entry(id):
                            print("Запись не найдена\n")
                            continue
                        print("Запись удалена\n")
                    except ValueError:
                        print("Ошибка: введите число\n")
                case '4':
                    print("Завершение работы")
                    break


if __name__ == '__main__':
    diary = Diary()
    diary.run()
