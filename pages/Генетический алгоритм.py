import streamlit as st
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

def load_initial_data(selection, mutation):
    """Загрузка исходных данных из папки."""
    folder_path = f'data/initial/{selection}/{mutation}'
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
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

def display_initial_data(selected_selection, selected_mutation, selected_crossover, selected_file, initial_data):
    """Отображение исходных данных."""
    st.subheader("Данные")
    st.write(f"Файл: {selected_file}")
    st.write(f"Метод выбора: {selected_selection}")
    st.write(f"Мутация: {selected_mutation}")
    st.write(f"Кроссовер: {selected_crossover}")
    st.write(f"Данные:")
    st.write(initial_data)

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
    
    initial_data_list = load_initial_data(selected_selection, selected_mutation)
    if initial_data_list:
        selected_file = st.selectbox("Выберите файл с исходными данными:", [f"{i+1}" for i in range(len(initial_data_list))])
        selected_data = initial_data_list[int(selected_file) - 1]
        display_initial_data(selected_selection, selected_mutation, selected_crossover, selected_file, selected_data)
    else:
        st.write(f"Исходные данные для {selected_selection} и {selected_mutation} не найдены.")

if __name__ == "__main__":
    main()