import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import csv
from datetime import date, datetime
from tkcalendar import DateEntry

class Person:
    def __init__(self, id, last_name, first_name, middle_name, gender, birth_date, work_from):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.gender = gender
        self.birth_date = birth_date
        self.work_from = work_from

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Настройка главного окна
        self.title("База данных сотрудников")
        self.geometry("1200x500")
        
        # Создание и размещение полей ввода
        self.create_entries()
        
        # Создание кнопок управления
        self.create_buttons()
        
        # Создание и настройка TreeView
        self.create_treeview()
        
        # Загрузка данных
        self.load_data()
        
    def create_entries(self):
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Создаем поля ввода
        ttk.Label(self.entry_frame, text="Фамилия").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.entry_frame, text="Имя").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.entry_frame, text="Отчество").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(self.entry_frame, text="Пол").grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(self.entry_frame, text="Дата рождения").grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(self.entry_frame, text="Работает с").grid(row=0, column=5, padx=5, pady=5)
        
        self.entry1 = ttk.Entry(self.entry_frame, width=15)
        self.entry2 = ttk.Entry(self.entry_frame, width=15)
        self.entry3 = ttk.Entry(self.entry_frame, width=15)
        
        # Пол - комбобокс
        self.gender_var = tk.StringVar()
        self.entry4 = ttk.Combobox(self.entry_frame, textvariable=self.gender_var, 
                                  values=["М", "Ж"], width=13, state="readonly")
        self.entry4.set("М")
        
        # Дата рождения - календарь
        self.entry5 = DateEntry(self.entry_frame, width=13, date_pattern='dd.mm.yyyy')
        
        # Дата начала работы - календарь
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
        # Создаем фрейм для таблицы
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Определяем колонки
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        
        # Создаем TreeView
        self.tree = ttk.Treeview(self.tree_frame, show="headings", columns=columns, height=15)
        
        # Настраиваем заголовки
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Фамилия")
        self.tree.heading("#3", text="Имя")
        self.tree.heading("#4", text="Отчество")
        self.tree.heading("#5", text="Пол")
        self.tree.heading("#6", text="Дата рождения")
        self.tree.heading("#7", text="Работает с")
        
        # Настраиваем ширину колонок
        self.tree.column("#1", width=50, anchor="center")
        self.tree.column("#2", width=120)
        self.tree.column("#3", width=120)
        self.tree.column("#4", width=120)
        self.tree.column("#5", width=60, anchor="center")
        self.tree.column("#6", width=100, anchor="center")
        self.tree.column("#7", width=100, anchor="center")
        
        # Создаем скроллбары
        ysb = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        
        # Размещаем элементы
        self.tree.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        
        # Настройка весов для растягивания
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Связываем события
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.selection_stat)
        
    def load_data(self):
        """Загрузка данных из CSV файла"""
        try:
            with open("persons.csv", newline="", encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            # Если файл не найден, создаем пустой
            with open("persons.csv", "w", newline="", encoding='utf-8') as f:
                pass
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при загрузке данных: {str(e)}")
            
    def validate_date(self, date_str):
        """Проверка корректности формата даты"""
        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False
            
    def get_next_id(self):
        """Получение следующего ID"""
        children = self.tree.get_children()
        if not children:
            return 1
        last_item = self.tree.item(children[-1])
        last_id = int(last_item['values'][0])
        return last_id + 1
        
    def add_person(self):
        """Добавление нового сотрудника"""
        # Получаем значения из полей ввода
        last_name = self.entry1.get().strip()
        first_name = self.entry2.get().strip()
        middle_name = self.entry3.get().strip()
        gender = self.gender_var.get()
        birth_date = self.entry5.get_date().strftime('%d.%m.%Y')
        work_from = self.entry6.get_date().strftime('%d.%m.%Y')
        
        # Проверка заполненности обязательных полей
        if not last_name or not first_name:
            mb.showwarning("Предупреждение", "Заполните обязательные поля: Фамилия и Имя")
            return
            
        # Проверка корректности дат
        try:
            birth_date_obj = datetime.strptime(birth_date, '%d.%m.%Y')
            work_from_obj = datetime.strptime(work_from, '%d.%m.%Y')
            
            # Проверка, что дата начала работы не раньше даты рождения
            if work_from_obj < birth_date_obj:
                mb.showwarning("Предупреждение", "Дата начала работы не может быть раньше даты рождения")
                return
        except ValueError:
            mb.showwarning("Предупреждение", "Некорректный формат даты")
            return
            
        # Генерируем ID
        new_id = self.get_next_id()
        
        # Создаем данные для добавления
        data = [str(new_id), last_name, first_name, middle_name, gender, birth_date, work_from]
        
        # Добавляем в TreeView
        self.tree.insert("", tk.END, values=data)
        
        # Сохраняем в файл
        try:
            with open("persons.csv", "a", newline="", encoding='utf-8') as f:
                csv.writer(f).writerow(data)
            mb.showinfo("Успех", "Сотрудник успешно добавлен")
            self.clear_entries()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
            
    def edit_person(self):
        """Редактирование выбранного сотрудника"""
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для редактирования")
            return
            
        # Получаем значения из полей ввода
        last_name = self.entry1.get().strip()
        first_name = self.entry2.get().strip()
        middle_name = self.entry3.get().strip()
        gender = self.gender_var.get()
        birth_date = self.entry5.get_date().strftime('%d.%m.%Y')
        work_from = self.entry6.get_date().strftime('%d.%m.%Y')
        
        # Проверка заполненности обязательных полей
        if not last_name or not first_name:
            mb.showwarning("Предупреждение", "Заполните обязательные поля: Фамилия и Имя")
            return
            
        # Проверка корректности дат
        try:
            birth_date_obj = datetime.strptime(birth_date, '%d.%m.%Y')
            work_from_obj = datetime.strptime(work_from, '%d.%m.%Y')
            
            # Проверка, что дата начала работы не раньше даты рождения
            if work_from_obj < birth_date_obj:
                mb.showwarning("Предупреждение", "Дата начала работы не может быть раньше даты рождения")
                return
        except ValueError:
            mb.showwarning("Предупреждение", "Некорректный формат даты")
            return
            
        # Получаем ID выбранного элемента
        item = self.tree.item(selected[0])
        old_id = item['values'][0]
        
        # Создаем новые данные
        data = [str(old_id), last_name, first_name, middle_name, gender, birth_date, work_from]
        
        # Обновляем в TreeView
        self.tree.item(selected[0], values=data)
        
        # Перезаписываем весь файл
        self.save_all_data()
        
        mb.showinfo("Успех", "Данные сотрудника успешно обновлены")
        
    def delete_person(self):
        """Удаление выбранного сотрудника"""
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для удаления")
            return
            
        # Подтверждение удаления
        result = mb.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранного сотрудника?")
        if result:
            # Удаляем из TreeView
            self.tree.delete(selected[0])
            
            # Перезаписываем весь файл
            self.save_all_data()
            
            mb.showinfo("Успех", "Сотрудник успешно удален")
            self.clear_entries()
            
    def save_all_data(self):
        """Сохранение всех данных в файл"""
        try:
            # Получаем все данные из TreeView
            all_data = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                all_data.append(values)
                
            # Перезаписываем файл
            with open("persons.csv", "w", newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(all_data)
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
            
    def clear_entries(self):
        """Очистка полей ввода"""
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.gender_var.set("М")
        # Сбрасываем календари на текущую дату
        self.entry5.set_date(date.today())
        self.entry6.set_date(date.today())
        
    def on_select(self, event):
        """Обработка выбора строки в таблице"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            
            # Заполняем поля ввода данными из выбранной строки
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, values[1])
            
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, values[2])
            
            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, values[3])
            
            self.gender_var.set(values[4])
            
            # Устанавливаем даты в календарях
            try:
                birth_date = datetime.strptime(values[5], '%d.%m.%Y').date()
                self.entry5.set_date(birth_date)
                
                work_from_date = datetime.strptime(values[6], '%d.%m.%Y').date()
                self.entry6.set_date(work_from_date)
            except ValueError:
                pass  # Игнорируем ошибки парсинга дат
                
    def selection_stat(self, event):
        """Отображение статистики по выбранному сотруднику"""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = self.tree.item(selected[0])
        values = item["values"]
        
        try:
            _id, last_name, first_name, middle_name, gender, bdate, w_from = values
            
            # Парсим даты
            bd = datetime.strptime(bdate, '%d.%m.%Y').date()
            wf = datetime.strptime(w_from, '%d.%m.%Y').date()
            
            # Рассчитываем возраст и стаж
            today = date.today()
            
            # Точный расчет возраста
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            
            # Точный расчет стажа
            experience = today.year - wf.year - ((today.month, today.day) < (wf.month, wf.day))
            
            # Определяем пенсионный возраст
            pension_age = 60 if gender == 'М' else 55
            
            # Расчет до пенсии
            if age >= pension_age:
                years_to_pension = "Уже на пенсии"
                pension_status = "Да"
            else:
                years_to_pension = f"{pension_age - age} лет"
                pension_status = "Нет"
            
            # Минимальный стаж для пенсии (в зависимости от пола)
            min_experience = 25 if gender == 'М' else 20
            
            # Проверка достаточности стажа
            if experience >= min_experience:
                experience_status = "Достаточный"
            else:
                experience_status = f"Недостаточный (еще {min_experience - experience} лет)"
            
            # Формируем подробный отчет
            report = f"ОСНОВНАЯ ИНФОРМАЦИЯ\n"
            report += f"Возраст: {age} лет\n"
            report += f"Стаж: {experience} лет\n\n"
            
            report += f"ПЕНСИОННАЯ ИНФОРМАЦИЯ\n"
            report += f"Пенсионный возраст: {pension_age} лет\n"
            report += f"На пенсии: {pension_status}\n"
            report += f"До пенсии: {years_to_pension}\n\n"
            
            report += f"СТАЖ\n"
            report += f"Минимальный стаж: {min_experience} лет\n"
            report += f"Статус стажа: {experience_status}\n"
            
            # Добавляем рекомендации
            if age >= pension_age and experience >= min_experience:
                report += f"\nСотрудник имеет право на пенсию"
            elif age >= pension_age:
                report += f"\nДостигнут пенсионный возраст, но стаж недостаточный"
            elif experience >= min_experience:
                report += f"\nСтаж достаточный, но пенсионный возраст еще не наступил"
            
            # Формируем заголовок
            if middle_name:
                title = f"{last_name} {first_name[0]}.{middle_name[0]}."
            else:
                title = f"{last_name} {first_name[0]}."
            
            mb.showinfo(title=title, message=report)
            
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при расчете статистики: {str(e)}")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()