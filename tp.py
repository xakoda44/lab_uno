import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import csv
import os
import tempfile
from datetime import date, datetime
from tkcalendar import DateEntry
from typing import Tuple, List

# Константы
CSV_FILENAME = "persons.csv"
DATE_FORMAT = "%d.%m.%Y"
TREE_COLUMNS = ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Работает с")
COLUMN_WIDTHS = (50, 120, 120, 120, 60, 100, 100)


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("База данных сотрудников")
        self.geometry("1200x500")

        self.create_entries()
        self.create_buttons()
        self.create_treeview()
        self.load_data()

    def create_entries(self):
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        labels = ["Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Работает с"]
        for i, text in enumerate(labels):
            ttk.Label(self.entry_frame, text=text).grid(row=0, column=i, padx=5, pady=5)

        self.entry1 = ttk.Entry(self.entry_frame, width=15)
        self.entry2 = ttk.Entry(self.entry_frame, width=15)
        self.entry3 = ttk.Entry(self.entry_frame, width=15)

        self.gender_var = tk.StringVar()
        self.entry4 = ttk.Combobox(
            self.entry_frame, textvariable=self.gender_var,
            values=["М", "Ж"], width=13, state="readonly"
        )
        self.entry4.set("М")

        self.entry5 = DateEntry(self.entry_frame, width=13, date_pattern='dd.mm.yyyy')
        self.entry6 = DateEntry(self.entry_frame, width=13, date_pattern='dd.mm.yyyy')

        self.entry1.grid(row=1, column=0, padx=5, pady=5)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)
        self.entry3.grid(row=1, column=2, padx=5, pady=5)
        self.entry4.grid(row=1, column=3, padx=5, pady=5)
        self.entry5.grid(row=1, column=4, padx=5, pady=5)
        self.entry6.grid(row=1, column=5, padx=5, pady=5)

    def create_buttons(self):
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.btn_add = ttk.Button(self.button_frame, text="Добавить", command=self.add_person)
        self.btn_edit = ttk.Button(self.button_frame, text="Изменить", command=self.edit_person)
        self.btn_delete = ttk.Button(self.button_frame, text="Удалить", command=self.delete_person)
        self.btn_clear = ttk.Button(self.button_frame, text="Очистить", command=self.clear_entries)

        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        self.btn_edit.grid(row=0, column=1, padx=5, pady=5)
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

    def create_treeview(self):
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        columns = tuple(f"#{i}" for i in range(1, 8))
        self.tree = ttk.Treeview(self.tree_frame, show="headings", columns=columns, height=15)

        for i, (col, text) in enumerate(zip(columns, TREE_COLUMNS)):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=COLUMN_WIDTHS[i], anchor="center" if i in (0, 4, 5, 6) else "w")

        ysb = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")

        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.selection_stat)

    def load_data(self):
        try:
            if not os.path.exists(CSV_FILENAME):
                return
            with open(CSV_FILENAME, newline="", encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 7:
                        self.tree.insert("", tk.END, values=row)
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при загрузке данных: {e}")

    def get_form_data(self) -> Tuple[str, str, str, str, str, str]:
        last_name = self.entry1.get().strip()
        first_name = self.entry2.get().strip()
        middle_name = self.entry3.get().strip()
        gender = self.gender_var.get()
        birth_date = self.entry5.get_date().strftime(DATE_FORMAT)
        work_from = self.entry6.get_date().strftime(DATE_FORMAT)

        if not last_name or not first_name:
            raise ValueError("Заполните обязательные поля: Фамилия и Имя")

        try:
            birth_date_obj = datetime.strptime(birth_date, DATE_FORMAT).date()
            work_from_obj = datetime.strptime(work_from, DATE_FORMAT).date()
            if work_from_obj < birth_date_obj:
                raise ValueError("Дата начала работы не может быть раньше даты рождения")
        except ValueError as e:
            if "time data" in str(e) or "unconverted data" in str(e):
                raise ValueError("Некорректный формат даты")
            else:
                raise e

        return last_name, first_name, middle_name, gender, birth_date, work_from

    def get_next_id(self) -> int:
        children = self.tree.get_children()
        if not children:
            return 1
        last_item = self.tree.item(children[-1])
        try:
            return int(last_item['values'][0]) + 1
        except (ValueError, IndexError):
            return 1

    def add_person(self):
        try:
            data = self.get_form_data()
            new_id = self.get_next_id()
            row = [str(new_id), *data]
            self.tree.insert("", tk.END, values=row)
            with open(CSV_FILENAME, "a", newline="", encoding='utf-8') as f:
                csv.writer(f).writerow(row)
            mb.showinfo("Успех", "Сотрудник успешно добавлен")
            self.clear_entries()
        except ValueError as e:
            mb.showwarning("Предупреждение", str(e))
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при сохранении данных: {e}")

    def edit_person(self):
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для редактирования")
            return
        try:
            data = self.get_form_data()
            item = self.tree.item(selected[0])
            old_id = item['values'][0]
            new_row = [str(old_id), *data]
            self.tree.item(selected[0], values=new_row)
            self.save_all_data()
            mb.showinfo("Успех", "Данные сотрудника успешно обновлены")
        except ValueError as e:
            mb.showwarning("Предупреждение", str(e))
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при обновлении данных: {e}")

    def delete_person(self):
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для удаления")
            return
        if mb.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранного сотрудника?"):
            self.tree.delete(selected[0])
            self.save_all_data()
            mb.showinfo("Успех", "Сотрудник успешно удален")
            self.clear_entries()

    def save_all_data(self):
        temp_file = None
        try:
            all_data: List[List[str]] = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if len(values) == 7:
                    all_data.append(list(values))
            with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8', delete=False) as tmp:
                csv.writer(tmp).writerows(all_data)
                temp_file = tmp.name
            os.replace(temp_file, CSV_FILENAME)
        except Exception as e:
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
            raise e

    def clear_entries(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.gender_var.set("М")
        today = date.today()
        self.entry5.set_date(today)
        self.entry6.set_date(today)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        if len(values) < 7:
            return

        self.entry1.delete(0, tk.END);
        self.entry1.insert(0, values[1])
        self.entry2.delete(0, tk.END);
        self.entry2.insert(0, values[2])
        self.entry3.delete(0, tk.END);
        self.entry3.insert(0, values[3])
        self.gender_var.set(values[4])

        try:
            bd = datetime.strptime(values[5], DATE_FORMAT).date()
            wf = datetime.strptime(values[6], DATE_FORMAT).date()
            self.entry5.set_date(bd)
            self.entry6.set_date(wf)
        except (ValueError, TypeError):
            today = date.today()
            self.entry5.set_date(today)
            self.entry6.set_date(today)

    def calculate_age(self, birth_date: date) -> int:
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def selection_stat(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        if len(values) != 7:
            return

        try:
            _id, last_name, first_name, middle_name, gender, bdate_str, w_from_str = values
            bd = datetime.strptime(bdate_str, DATE_FORMAT).date()
            wf = datetime.strptime(w_from_str, DATE_FORMAT).date()

            age = self.calculate_age(bd)
            experience = self.calculate_age(wf)

            pension_age = 60 if gender == 'М' else 55
            min_experience = 25 if gender == 'М' else 20

            if age >= pension_age:
                years_to_pension = "Уже на пенсии"
                pension_status = "Да"
            else:
                years_to_pension = f"{pension_age - age} лет"
                pension_status = "Нет"

            if experience >= min_experience:
                experience_status = "Достаточный"
                experience_comment = ""
            else:
                experience_status = f"Недостаточный (еще {min_experience - experience} лет)"
                experience_comment = f"\nСтаж недостаточный (требуется {min_experience} лет)"

            report = (
                f"ОСНОВНАЯ ИНФОРМАЦИЯ\n"
                f"Возраст: {age} лет\n"
                f"Стаж: {experience} лет\n\n"
                f"ПЕНСИОННАЯ ИНФОРМАЦИЯ\n"
                f"Пенсионный возраст: {pension_age} лет\n"
                f"На пенсии: {pension_status}\n"
                f"До пенсии: {years_to_pension}\n\n"
                f"СТАЖ\n"
                f"Минимальный стаж: {min_experience} лет\n"
                f"Статус стажа: {experience_status}"
            )

            if age >= pension_age and experience >= min_experience:
                report += "\n\nСотрудник имеет право на пенсию"
            elif age >= pension_age:
                report += f"\n\nДостигнут пенсионный возраст, но стаж недостаточный{experience_comment}"
            elif experience >= min_experience:
                report += "\n\nСтаж достаточный, но пенсионный возраст ещё не наступил"
            else:
                report += experience_comment

            short_name = f"{last_name} {first_name[0]}."
            if middle_name:
                short_name += f"{middle_name[0]}."

            mb.showinfo(title=short_name, message=report)

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при расчёте статистики: {e}")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()