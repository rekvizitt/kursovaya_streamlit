import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import datetime

st.set_page_config(
    page_title="TwoOpt и LKH",
    page_icon="🟥",
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
    
    fig, ax = plt.subplots(figsize=(15, 6))  # Увеличиваем ширину графика
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

if __name__ == "__main__":
    main()