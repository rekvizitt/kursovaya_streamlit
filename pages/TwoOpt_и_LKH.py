import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import datetime

st.set_page_config(
    page_title="TwoOpt и LKH",
    page_icon="🦧",
)

algorithms = ["TwoOpt", "Lkh"]
iterations = [10, 100, 1000]

def load_data(filename):
    """Загрузка данных из JSON файла."""
    try:
        with open(filename) as f:
            data = json.load(f)
        if not data:
            st.write("Нет данных для отображения.")
            return None
        return data
    except FileNotFoundError:
        st.write("Файл не найден.")
        return None

def load_initial_data(algorithm, iterations):
    """Загрузка исходных данных из папки."""
    folder_path = f'data/initial/{algorithm}/{iterations}'
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            data = load_data(file_path)
            if data:
                data_list.append(data)
    return data_list

def display_algorithm_data(selected_algorithm, algorithm_data):
    """Отображение информации об алгоритме."""
    total_sum = algorithm_data['TotalSum']
    elapsed_milliseconds = algorithm_data['ElapsedMilliseconds']
    
    # Преобразование миллисекунд в удобочитаемую строку
    elapsed_time = str(datetime.timedelta(milliseconds=elapsed_milliseconds))
    
    st.subheader("Данные")
    st.write(f"Сумма: {total_sum}")
    st.write(f"Затраченное время: {elapsed_time}")

def plot_costs(selected_algorithm, costs, repeat=None):
    """Построение графика для Costs."""
    df = pd.DataFrame({
        'Index': range(len(costs)),
        'Costs': costs
    })

    st.subheader("График Costs по индексам")
    
    # Установка стиля графика
    plt.style.use('ggplot')  # Используем стандартный стиль ggplot
    
    fig, ax = plt.subplots(figsize=(12, 5))  # Уменьшаем ширину графика
    ax.plot(df['Index'], df['Costs'], marker='o', color='royalblue', label='Costs', markersize=6, linewidth=2)
    
    # Настройка меток осей и заголовка
    ax.set_xlabel('Индекс', fontsize=14)
    ax.set_ylabel('Costs', fontsize=14)
    if repeat:
        ax.set_title(f'График Costs для {selected_algorithm}, {selected_iterations} итераций, {repeat} повторение', fontsize=16)
    else:
        ax.set_title(f'График Costs для {selected_algorithm}, {selected_iterations} итераций', fontsize=16)
    
    # Добавление сетки
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Добавление аннотаций для ключевых точек
    for i, cost in enumerate(costs):
        ax.annotate(f'{cost}', xy=(i, cost), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

    ax.legend(fontsize=12)
    
    # Отображение графика
    st.pyplot(fig)

def plot_iterations_comparison(selected_algorithm, data_10, data_100, data_1000):
    """Построение графика сравнения результатов для разных итераций."""
    iterations_list = [10, 100, 1000]
    total_sum_list = [data_10['TotalSum'], data_100['TotalSum'], data_1000['TotalSum']]
    elapsed_time_list = [data_10['ElapsedMilliseconds'], data_100['ElapsedMilliseconds'], data_1000['ElapsedMilliseconds']]

    df = pd.DataFrame({
        'Iterations': iterations_list,
        'TotalSum': total_sum_list,
        'ElapsedTime': elapsed_time_list
    })

    st.subheader("График сравнения результатов для разных итераций")
    
    # Установка стиля графика
    plt.style.use('ggplot')  # Используем стандартный стиль ggplot
    
    fig, ax1 = plt.subplots(figsize=(12, 5))  # Уменьшаем ширину графика
    
    color = 'tab:blue'
    ax1.set_xlabel('Итерации', fontsize=14)
    ax1.set_ylabel('Сумма', color=color, fontsize=14)
    ax1.plot(df['Iterations'], df['TotalSum'], marker='o', color=color, label='Сумма')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Установка максимума для оси sum
    max_sum = max(total_sum_list) * 1.2  # Увеличиваем максимум на 20%
    min_sum = min(total_sum_list) * 0.8
    ax1.set_ylim(min_sum, max_sum)

    ax2 = ax1.twinx()  # Второй y-ось
    color = 'tab:red'
    ax2.set_ylabel('Затраченное время (мс)', color=color, fontsize=14)
    ax2.plot(df['Iterations'], df['ElapsedTime'], marker='o', color=color, label='Затраченное время')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Установка максимума для оси elapsed_milliseconds
    max_elapsed_time = max(elapsed_time_list) * 1.2  # Увеличиваем максимум на 20%
    ax2.set_ylim(0, max_elapsed_time)
    
    # Настройка меток осей и заголовка
    ax1.set_title(f'График сравнения результатов для {selected_algorithm}', fontsize=16)
    
    # Добавление сетки
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Добавление аннотаций для ключевых точек
    for i, (total_sum, elapsed_time) in enumerate(zip(total_sum_list, elapsed_time_list)):
        ax1.annotate(f'{total_sum}', xy=(iterations_list[i], total_sum), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
        ax2.annotate(f'{elapsed_time}', xy=(iterations_list[i], elapsed_time), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

    ax1.legend(loc='upper left', fontsize=12)
    ax2.legend(loc='upper right', fontsize=12)
    
    # Отображение графика
    st.pyplot(fig)

def plot_algorithm_comparison(selected_algorithms):
    """Построение графика сравнения результатов разных алгоритмов."""
    iterations_list = [10, 100, 1000]
    data = {
        'Iterations': iterations_list,
    }

    for algorithm in selected_algorithms:
        total_sum_list = []
        elapsed_time_list = []
        for iteration in iterations_list:
            if algorithm == "TwoOpt":
                filename = 'data/best/best_solutions_2opt.json'
            elif algorithm == "Lkh":
                filename = 'data/best/best_solutions_LKH.json'
            data_dict = load_data(filename)
            if data_dict:
                algorithm_data = data_dict['BestSolutions'].get(str(iteration))
                if algorithm_data:
                    total_sum_list.append(algorithm_data['TotalSum'])
                    elapsed_time_list.append(algorithm_data['ElapsedMilliseconds'])
                else:
                    total_sum_list.append(None)
                    elapsed_time_list.append(None)
            else:
                total_sum_list.append(None)
                elapsed_time_list.append(None)
        data[f'{algorithm}_TotalSum'] = total_sum_list
        data[f'{algorithm}_ElapsedTime'] = elapsed_time_list

    df = pd.DataFrame.from_dict(data, orient='index').transpose()

    st.subheader("График сравнения результатов разных алгоритмов")
    
    # Установка стиля графика
    plt.style.use('ggplot')  # Используем стандартный стиль ggplot
    
    fig, ax1 = plt.subplots(figsize=(12, 5))  # Уменьшаем ширину графика
    
    color = 'tab:blue'
    ax1.set_xlabel('Итерации', fontsize=14)
    ax1.set_ylabel('Сумма', color=color, fontsize=14)
    for algorithm in selected_algorithms:
        ax1.plot(df['Iterations'], df[f'{algorithm}_TotalSum'], marker='o', label=f'{algorithm} Сумма')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # Второй y-ось
    color = 'tab:red'
    ax2.set_ylabel('Затраченное время (мс)', color=color, fontsize=14)
    for algorithm in selected_algorithms:
        ax2.plot(df['Iterations'], df[f'{algorithm}_ElapsedTime'], marker='o', label=f'{algorithm} Затраченное время')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Настройка меток осей и заголовка
    ax1.set_title('График сравнения результатов разных алгоритмов', fontsize=16)
    
    # Добавление сетки
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax1.legend(loc='upper left', fontsize=12)
    ax2.legend(loc='upper right', fontsize=12)
    
    # Отображение графика
    st.pyplot(fig)

def display_initial_data_table(initial_data_list):
    """Отображение исходных данных в виде таблицы."""
    st.subheader("Исходные данные")
    
    # Преобразование данных в DataFrame
    df_list = []
    for data in initial_data_list:
        df_list.append({
            'TotalSum': data.get('TotalSum', None),
            'ElapsedMilliseconds': data.get('ElapsedMilliseconds', None),
            'Iterations': data.get('Iterations', None)
        })
    
    df = pd.DataFrame(df_list)
    
    # Отображение таблицы с возможностью сортировки и фильтрации
    st.dataframe(df, use_container_width=True)

def main():
    global selected_iterations
    st.title("Алгоритмы TwoOpt и LKH")
    
    selected_algorithm = st.selectbox("Выберите алгоритм:", algorithms)
    st.divider()
    st.header("Лучшие результаты")
    selected_iterations = st.selectbox("Выберите количество итераций:", iterations)

    if selected_algorithm == "TwoOpt":
        filename = 'data/best/best_solutions_2opt.json'
    elif selected_algorithm == "Lkh":
        filename = 'data/best/best_solutions_LKH.json'

    data = load_data(filename)

    if data:
        algorithm_data = data['BestSolutions'].get(str(selected_iterations))
        if algorithm_data:
            display_algorithm_data(selected_algorithm, algorithm_data)
            plot_costs(selected_algorithm, algorithm_data['Costs'])
        else:
            st.write(f"Данные для {selected_algorithm} с {selected_iterations} итерациями не найдены.")
    st.divider()
    st.header("Исходные данные")
    
    initial_data = load_initial_data(selected_algorithm.lower(), selected_iterations)
    if initial_data:
        selected_file = st.selectbox("Выберите файл с исходными данными (номер повтора):", [f"{i+1}" for i in range(len(initial_data))])
        repeat = int(selected_file)
        selected_data = initial_data[repeat - 1]
        display_algorithm_data(selected_algorithm, selected_data)
        plot_costs(selected_algorithm, selected_data['Costs'], repeat)
    else:
        st.write(f"Исходные данные для {selected_algorithm} с {selected_iterations} итерациями не найдены.")

    st.divider()
    st.header("Исходные данные в виде таблицы")
    
    initial_data_table = load_initial_data(selected_algorithm.lower(), selected_iterations)
    if initial_data_table:
        display_initial_data_table(initial_data_table)
    else:
        st.write(f"Исходные данные для {selected_algorithm} с {selected_iterations} итерациями не найдены.")

    st.divider()
    st.header("Сравнение лучших результатов для разного количества итераций")
    
    data_10 = load_data(filename)['BestSolutions'].get('10')
    data_100 = load_data(filename)['BestSolutions'].get('100')
    data_1000 = load_data(filename)['BestSolutions'].get('1000')

    if data_10 and data_100 and data_1000:
        plot_iterations_comparison(selected_algorithm, data_10, data_100, data_1000)
    else:
        st.write("Данные для сравнения результатов для разных итераций не найдены.")

    st.divider()
    st.header("Сравнение результатов разных алгоритмов")
    
    selected_algorithms = st.multiselect("Выберите алгоритмы для сравнения:", algorithms)
    
    if selected_algorithms:
        plot_algorithm_comparison(selected_algorithms)
    else:
        st.write("Выберите хотя бы один алгоритм для сравнения.")

if __name__ == "__main__":
    main()