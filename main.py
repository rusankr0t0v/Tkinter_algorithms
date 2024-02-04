"""
Основной модуль программы, содержащий реализацию графического интерфейса, набор функций для реализации разных
способов сортировки и вспомогательные функции.
"""

import re
import time
import random
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror


def fill_random():
    """
    Функция принимает значение колл-ва элементов из поля fill_random_entry с помощью метода get().
    Проверяет введенные данные. В случае, если данные введены корректно, формирует рандомную последовательньость
    чисел, длинна которой равнf кол-ву указанных элементов. Подставляет сформированную последовательность
    в поле entry_field.
    В случае, если введено число меньше 2 или не числовое значение - выводит messagebox с ошибкой.
    :return:None
    """
    try:
        amount_elem = int(fill_random_entry.get())
        #проверка длинны списка
        if amount_elem >= 2:
            sort_select_btn.config(state='normal')
            items = list(range(amount_elem))
            random.shuffle(items)
            arr = items[:amount_elem]
            arr = (', '.join(map(str, arr)))
            #заполнение данными
            entry_field.replace("1.0", END, arr)
        else:
            raise ValueError
    except ValueError:
        showerror(title='Ошибка', message='В поле "Кол-во элементов" должно быть '
                                          'указано число больше или равно 2!')


def check_entry_field(event):
    """
    Функция сработывает каждый раз при вводе символа в текстовое поле entry_field с клавиатуры.
    Получает значение поля entry_field с помошью метода get().
    Проверяет полученное значение. Если данные валидны, кнопке sort_select_btn присваивается параметр
    state='normal' (кнопка активна), цвет теста в тексовом поле при этом - черный.
    Если данные не валидны, кнопке sort_select_btn присваивается параметр state='disabled' (не активна),
    цвет теста в тексовом поле при этом - красный.
    :param event: None
    :return: None
    """
    check_data = entry_field.get("1.0", END)
    check = re.match("^(?:\d+\, )+\d+$|^(?:\d+\,)+\d+$", check_data)
    if check:
        sort_select_btn.config(state='normal')
        entry_field.config(foreground='black')
    else:
        sort_select_btn.config(state='disabled')
        entry_field.config(foreground='red')


def execute_sort():
    """
    Функция запуска сотрировки.
    Получает значение выбранного варианта сортировки и неотсортированный список с помощью метода get().
    В зависимости от полученного метода сортировки, выполняет функцию нужной сортировки.
    Полученные данные (время сотрировки и отсортированный список) выводит в текстовом окне output_field.
    :return: None
    """
    # зачистить поле вывода отсортированной последовательности
    output_field.delete("1.0", END)
    sort_select = sort_select_cb.get()
    my_list = entry_field.get("1.0",'end-1c').split(',')
    my_list_int = [int(item) for item in my_list]

    sort = False
    if sort_select == '':
        showerror(title='Ошибка', message='Не выбран вариант сортировки!')
    elif sort_select == 'Сортировка пузырьком':
        sort = bubble_sort(my_list_int)
    elif sort_select == 'Сортировка подсчетом':
        max_val = max(my_list_int)
        sort = counting_sort(my_list_int, max_val)
    elif sort_select == 'Пирамидальная сортировка':
        sort = heap_sort(my_list_int)
    elif sort_select == 'Сортировка слиянием':
        sort = merge_sort(my_list_int)
    elif sort_select == 'Быстрая сортировка':
        sort = quicksort(my_list_int)
    elif sort_select == 'Поразрядная сортировка':
        sort = radix_sort(my_list_int)
    elif sort_select == 'Сравнить все (время)':
        compare_sort(my_list_int)
    else:
        showerror(title='Ошибка', message='Сортировка отсутствует!')

    if sort:
        output_field.config(state='normal')
        output_field.replace("1.0", END, f'Затраченное время на сортировку: {sort[0]} сек.\n'
                              f'{str(sort[1])}')


def compare_sort(lst):
    """
    Функция сравнения времени выполнения сортировки всеми вариатами сотритовки.
    Запускается в случае, если пользователь выбрал вариант сортировки "Сравнить все (время)"
    Функция последовательно запускает каждую функцию сотртировки и выводит время выполнения в
    текстовом окне output_field.
    :param lst: неотсортированный список
    :return: None
    """
    try:
        compare_qs = quicksort(lst)
        output_field.insert("1.0", f'Быстрая сортировка...........{compare_qs[0]} сек.\n')

        compare_bs = bubble_sort(lst)
        output_field.insert(END,f'Сортировка пузырьком.........{compare_bs[0]} сек.\n')

        max_val = max(lst)
        compare_cs = counting_sort(lst, max_val)
        output_field.insert(END, f'Сортировка подсчетом.........{compare_cs[0]} сек.\n')

        compare_hs = heap_sort(lst)
        output_field.insert(END, f'Пирамидальная сортировка.....{compare_hs[0]} сек.\n')

        compare_ms = merge_sort(lst)
        output_field.insert(END, f'Сортировка слиянием..........{compare_ms[0]} сек.\n')

        compare_rs = radix_sort(lst)
        output_field.insert(END, f'Поразрядная сортировка.......{compare_rs[0]} сек.\n')
    except Exception:
        output_field.replace("1.0", 'Непредвиденная ошибка!')

def bubble_sort(my_list):
    """
    Функция сортировки пузырьком.
    :param my_list: неотсортированный список
    :return: list. end - время выполнения сортировки, my_list - отсортированный список
    """
    start = time.time()
    last_elem_index = len(my_list) - 1
    for passNo in range(last_elem_index, 0, -1):
        for idx in range(passNo):
            if my_list[idx] > my_list[idx + 1]:
                my_list[idx], my_list[idx + 1] = my_list[idx + 1], my_list[idx]
    end = time.time() - start
    return [end, my_list]


def counting_sort(my_list, largest):
    """
    Функция сортировки подсчетом.
    :param my_list: неотсортированный список
    :param largest: наибольшее значение элемента my_list
    :return: list. end - время выполнения сортировки, result - отсортированный список
    """
    #сотрировка подсчетом
    start = time.time()
    c = [0] * (largest + 1)
    for i in range(len(my_list)):
        c[my_list[i]] = c[my_list[i]] + 1
    c[0] = c[0] - 1
    for i in range(1, largest + 1):
        c[i] = c[i] + c[i - 1]
    result = [None] * len(my_list)
    for x in reversed(my_list):
        result[c[x]] = x
        c[x] = c[x] - 1
    end = time.time() - start
    return [end, result]


def heap_sort(lst):
    """
    Функция пирамидальной сортировки
    :param lst: неотсортированный список
    :return: list. end - время выполнения сортировки, lst - отсортированный список
    """
    start = time.time()
    n = len(lst)
    for i in range(n, -1, -1):
        heapify(lst, n, i)
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        heapify(lst, i, 0)
    end = time.time() - start
    return [end, lst]


def heapify(lst, n, i):
    """
    Функция преобразования в двоичную кучу (пирамидальная сортировка).
    Вызывается функцией heap_sort()
    :param lst: список
    :param n: размер кучи
    :param i: корневой индекс
    :return: None
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and lst[i] < lst[left]:
        largest = left
    if right < n and lst[largest] < lst[right]:
        largest = right
    if largest != i:
        lst[i], lst[largest] = lst[largest], lst[i]
        heapify(lst, n, largest)


def merge_sort(lst):
    """
    Функция сортировки слиянием.
    :param lst: неотсортированный список
    :return: list. end - время выполнения сортировки, lst - отсортированный список
    """
    #Сортировка слиянием
    start = time.time()
    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort(left)
        merge_sort(right)

        a = 0
        b = 0
        c = 0
        while a < len(left) and b < len(right):
            if left[a] < right[b]:
                lst[c] = left[a]
                a = a + 1
            else:
                lst[c] = right[b]
                b = b + 1
            c = c + 1
        while a < len(left):
            lst[c] = left[a]
            a = a + 1
            c = c + 1
        while b < len(right):
            lst[c] = right[b]
            b = b + 1
            c = c + 1
    end = time.time() - start
    return [end, lst]


def quicksort(lst):
    """
    Вспомогательная функция быстрой сортировки.
    Вызывает функцию сортировки и считывает время выполнения.
    :param lst: неотсортированный список
    :return: list. end - время выполнения сортировки, result - отсортированный список
    """
    def func_quicksort(lst):
        """
        Функция быстрой сортировки.
        :param lst: неотсортированный список
        :return: рекурсивыный вызов функции func_quicksort(), pivot или lst
        """
        if len(lst) < 2:
            return lst
        else:
            pivot = lst[0]
            less = [i for i in lst[1:] if i < pivot]
            greater = [i for i in lst[1:] if i > pivot]
            return func_quicksort(less) + [pivot] + func_quicksort(greater)
    start = time.time()
    result = func_quicksort(lst)
    end = time.time() - start
    return [end, result]


def radix_sort(lst):
    """
    Функция поразрядной сортировки.
    :param lst: неотсортированный список
    :return: list. end - время выполнения сортировки, lst - отсортированный список
    """
    start = time.time()
    max_digit = max([len(str(num)) for num in lst])
    radix = 10
    lists = [[] for i in range(radix)]
    for i in range(0, max_digit):
        for elem in lst:
            digit = (elem // radix ** i) % radix
            lists[digit].append(elem)
        lst = [x for queue in lists for x in queue]
        lists = [[] for i in range(radix)]
    end = time.time() - start
    return [end, lst]



if __name__ == '__main__':

    """
    if __name__ == '__main__' - запуск программы. 
    Создание графического интерфейса.
    """
    root = Tk()
    root.title("Tkinter & Сортировки")
    root.geometry("800x600")

    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(15): root.rowconfigure(index=r, weight=1)

    #блок отображения поля для ввода последовательности
    entry_field_lable = Label(text="Введите последовательность чисел (через запятую) "
                                   "или сформируйте ее кнопкой ниже")
    entry_field_lable.grid(column=0, columnspan=15, row=0)
    entry_field = Text(wrap="word", height=12)
    entry_field.grid(column=0, columnspan=14, row=1, rowspan=4, sticky=NSEW)
    entry_field.bind("<KeyRelease>", check_entry_field)
    entry_field_ys = ttk.Scrollbar(orient="vertical", command=entry_field.yview)
    entry_field_ys.grid(column=14, row=1, rowspan=4, sticky=NS)
    entry_field["yscrollcommand"] = entry_field_ys.set

    #блок рандомоного заполнения поля для ввода
    fill_random_lable = Label(text="Кол-во элементов:")
    fill_random_lable.grid(column=0, row=6, sticky=E)
    fill_random_entry = ttk.Entry(width=8)
    fill_random_entry.grid(column=1, row=6, sticky=EW)
    fill_random_btn = ttk.Button(text="Заполнить рандомно", command=fill_random)
    fill_random_btn.grid(column=2, columnspan=5, row=6, sticky=EW)

    #блок выбора варианта сотрировки
    sort_select_lable = Label(text="Сортировка:")
    sort_select_lable.grid(column=10, row=6, sticky=E)
    sort_select = ['Сортировка пузырьком', 'Сортировка подсчетом', 'Пирамидальная сортировка', 'Сортировка слиянием',
                   'Быстрая сортировка', 'Поразрядная сортировка', 'Сравнить все (время)']
    sort_select_cb = ttk.Combobox(values=sort_select)
    sort_select_cb.grid(column=11, row=6, sticky=EW)
    sort_select_btn = ttk.Button(text="Start", command=execute_sort, state=["disabled"])
    sort_select_btn.grid(column=12, columnspan=2, row=6)

    #блок отображения поля для вывода отсортированной последовательности
    output_field_lable = Label(text="Вывод информации:")
    output_field_lable.grid(column=0, columnspan=15, row=7)
    output_field = Text(wrap="word", height=13, state=["disabled"])
    output_field.grid(column=0, columnspan=14, row=8, rowspan=4, sticky=NSEW)
    output_field_ys = ttk.Scrollbar(orient="vertical", command=output_field.yview)
    output_field_ys.grid(column=14, row=9, rowspan=4, sticky=NS)
    output_field["yscrollcommand"] = output_field_ys.set

    root.mainloop()