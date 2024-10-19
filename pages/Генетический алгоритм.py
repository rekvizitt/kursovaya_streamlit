import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

st.set_page_config(
    page_title="Генетический алгоритм",
    page_icon="🧬",
)

selections = ["EliteSelection", "RouletteWheel", "StochasticUniversalSampling", "Tournament"]
mutations = ["DisplacementMutation", "InsertionMutation", "ReverseSequenceMutation", "TworsMutation"]
crossovers = ["CycleCrossover", "OnePointCrossover", "OrderBasedCrossover", "OrderedCrossover", "PartiallyMappedCrossover",
              "PositionBasedCrossover", "ThreeParentCrossover", "TwoPointCrossover", "UniformCrossover"]
iterations = [10, 100, 1000, 10000]

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

def load_initial_data(selection, mutation, crossover):
    """Загрузка исходных данных из папки для выбранного кроссовера."""
    folder_path = f'data/initial/{selection}/{mutation}'
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and crossover in filename:
            file_path = os.path.join(folder_path, filename)
            data = load_data(file_path)
            if data:
                data_list.append(data)
    return data_list

def display_genetic_algorithm_data(selected_selection, selected_mutation, selected_crossover, selected_iterations, algorithm_data):
    """Отображение информации о генетическом алгоритме."""
    distance = algorithm_data['Distance']
    time_in_sec = algorithm_data['Data']['TimeInSec']
    fitness = algorithm_data['Data']['Fintess']
    
    st.subheader("Данные")
    st.write(f"Дистанция: {distance}")
    st.write(f"Время выполнения (сек): {time_in_sec}")
    st.write(f"Фитнес: {fitness}")

def display_initial_data(selected_selection, selected_mutation, selected_crossover, initial_data_list):
    """Отображение исходных данных в виде таблицы."""
    st.subheader("Исходные данные")
    st.write(f"Метод выбора: {selected_selection}")
    st.write(f"Мутация: {selected_mutation}")
    st.write(f"Кроссовер: {selected_crossover}")
    
    # Добавление слова 'Selection' к selected_selection, если его нет
    if not selected_selection.endswith('Selection'):
        selected_selection += 'Selection'
    
    # Преобразование данных в DataFrame
    df_list = []
    for data in initial_data_list:
        if data.get('Selection') == selected_selection and data.get('Mutation') == selected_mutation and data.get('Crossover') == selected_crossover:
            for indicator in data.get('NumericalIndicators', []):
                df_list.append({
                    'GenerationCount': indicator.get('GenerationCount', None),
                    'TimeInSec': indicator.get('TimeInSec', None),
                    'Fitness': indicator.get('Fintess', None),
                    'Distance': indicator.get('Distance', None)
                })
    
    if not df_list:
        st.write("Данные для выбранных метода выбора, мутации и кроссовера не найдены.")
    else:
        df = pd.DataFrame(df_list)
        st.dataframe(df, use_container_width=True)

def plot_best_results_comparison(best_results, selected_mutation, selected_crossover):
    """Построение графика сравнения лучших результатов для всех методов выбора."""
    data = {
        'Iterations': iterations,
    }

    for selection, selection_data in best_results.items():
        distances = []
        for iteration in iterations:
            distance = selection_data.get(selected_mutation, {}).get(selected_crossover, {}).get(str(iteration), {}).get('Distance', None)
            distances.append(distance)
        data[selection] = distances

    df = pd.DataFrame(data)

    st.subheader("График сравнения лучших результатов для всех методов выбора")
    
    # Установка стиля графика
    plt.style.use('ggplot')  # Используем стандартный стиль ggplot
    
    fig, ax = plt.subplots(figsize=(12, 5))  # Уменьшаем ширину графика
    
    for selection in selections:
        ax.plot(df['Iterations'], df[selection], marker='o', label=selection)
    
    # Настройка меток осей и заголовка
    ax.set_xlabel('Итерации', fontsize=14)
    ax.set_ylabel('Дистанция', fontsize=14)
    ax.set_title(f'График сравнения лучших результатов для всех методов выбора\n(Мутация: {selected_mutation}, Кроссовер: {selected_crossover})', fontsize=16)
    
    # Добавление сетки
    ax.grid(True, linestyle='--', alpha=0.7)
    
    ax.legend(fontsize=12)
    
    # Отображение графика
    st.pyplot(fig)

def plot_comparison(selected_methods, selected_mutations, selected_crossovers):
    """Построение графика сравнения результатов разных методов, мутаций и кроссоверов."""
    data = {
        'Iterations': iterations,
    }

    for method in selected_methods:
        for mutation in selected_mutations:
            for crossover in selected_crossovers:
                distances = []
                for iteration in iterations:
                    filename = f'data/best/best_results_{method}.json'
                    data_dict = load_data(filename)
                    if data_dict:
                        distance = data_dict.get(mutation, {}).get(crossover, {}).get(str(iteration), {}).get('Distance', None)
                        distances.append(distance)
                data[f'{method}_{mutation}_{crossover}'] = distances

    df = pd.DataFrame.from_dict(data, orient='index').transpose()

    st.subheader("График сравнения результатов разных методов, мутаций и кроссоверов")
    
    # Установка стиля графика
    plt.style.use('ggplot')  # Используем стандартный стиль ggplot
    
    fig, ax = plt.subplots(figsize=(12, 5))  # Уменьшаем ширину графика
    
    for column in df.columns:
        if column != 'Iterations':
            ax.plot(df['Iterations'], df[column], marker='o', label=column)
    
    # Настройка меток осей и заголовка
    ax.set_xlabel('Итерации', fontsize=14)
    ax.set_ylabel('Дистанция', fontsize=14)
    ax.set_title('График сравнения результатов разных методов, мутаций и кроссоверов', fontsize=16)
    
    # Добавление сетки
    ax.grid(True, linestyle='--', alpha=0.7)
    
    ax.legend(fontsize=12)
    
    # Отображение графика
    st.pyplot(fig)

def main():
    global selected_iterations
    st.title("Генетический алгоритм")
    
    selected_selection = st.selectbox("Выберите метод выбора:", selections)
    selected_mutation = st.selectbox("Выберите мутацию:", mutations)
    selected_crossover = st.selectbox("Выберите кроссовер:", crossovers)
    st.divider()
    st.header("Лучшие результаты")
    selected_iterations = st.selectbox("Выберите количество итераций:", iterations)
    filename = f'data/best/best_results_{selected_selection}.json'
    data = load_data(filename)

    if data:
        algorithm_data = data.get(selected_mutation, {}).get(selected_crossover, {}).get(str(selected_iterations))
        if algorithm_data:
            display_genetic_algorithm_data(selected_selection, selected_mutation, selected_crossover, selected_iterations, algorithm_data)
        else:
            st.write(f"Данные для {selected_selection}, {selected_mutation}, {selected_crossover} с {selected_iterations} итерациями не найдены.")

    st.divider()
    st.header("Исходные данные")
    
    initial_data_list = load_initial_data(selected_selection, selected_mutation, selected_crossover)
    if initial_data_list:
        display_initial_data(selected_selection, selected_mutation, selected_crossover, initial_data_list)
    else:
        st.write(f"Исходные данные для {selected_selection}, {selected_mutation} и {selected_crossover} не найдены.")

    st.divider()
    st.header("Сравнение лучших результатов")
    
    selected_mutation_for_comparison = st.selectbox("Выберите мутацию для сравнения:", mutations)
    selected_crossover_for_comparison = st.selectbox("Выберите кроссовер для сравнения:", crossovers)
    
    best_results = {}
    for selection in selections:
        filename = f'data/best/best_results_{selection}.json'
        data = load_data(filename)
        if data:
            best_results[selection] = data

    if best_results:
        plot_best_results_comparison(best_results, selected_mutation_for_comparison, selected_crossover_for_comparison)
    else:
        st.write("Данные для сравнения лучших результатов для всех методов выбора не найдены.")

    st.divider()
    st.header("Сравнение результатов разных методов, мутаций и кроссоверов")
    
    selected_methods = st.multiselect("Выберите методы выбора для сравнения:", selections)
    selected_mutations = st.multiselect("Выберите мутации для сравнения:", mutations)
    selected_crossovers = st.multiselect("Выберите кроссоверы для сравнения:", crossovers)
    
    if selected_methods and selected_mutations and selected_crossovers:
        plot_comparison(selected_methods, selected_mutations, selected_crossovers)
    else:
        st.write("Выберите хотя бы один метод выбора, одну мутацию и один кроссовер для сравнения.")

if __name__ == "__main__":
    main()