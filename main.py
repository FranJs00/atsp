from tsplib95 import load
import random
import time
import os
import pandas as pd
import itertools
from Algorithm import Algorithm
from Analyze import Analyze

valid_files = ['br17', 'p43']

# Solicitar problema al usuario
print("Seleccione uno de los problemas Disponibles:")
print("1. br17")
print("2. p43")
user_file = input("Ingrese el nombre del problema: ")

if user_file not in valid_files:
    print("El problema seleccionado no es válido")
    exit()

PROBLEM = user_file
PATH = f'./problems/{PROBLEM}'
RESULTS_PATH = f'{PATH}/results/'

# Obtener cantidad de archivos dentro de la carpeta results
EXECUTION_NUMBER = len([name for name in os.listdir(RESULTS_PATH) if os.path.isfile(os.path.join(RESULTS_PATH, name))])

file = load(f'{PATH}/{PROBLEM}.atsp')

def save_results(filename, params, fitness_history, best_solution, best_fitness, execution_time):
    with open(filename, 'a') as file:
        file.write("=== Resultados de Ejecución ===\n")
        file.write(f"Configuración del Algoritmo Evolutivo:\n")
        for key, value in params.items():
            file.write(f"  {key}: {value}\n")
        
        file.write("\nEvolución del Fitness:\n")
        for generation, fitness in enumerate(fitness_history):
            file.write(f"  Generación {generation + 1}: Mejor Fitness = {-fitness}\n")
        
        file.write("\nMejor Solución Encontrada:\n")
        file.write(f"  Ruta: {best_solution}\n")
        file.write(f"  Costo Total (Fitness): {-best_fitness}\n")
        
        file.write(f"\nTiempo de Ejecución: {execution_time:.2f} segundos\n")
        file.write("=================================\n\n")
   


def run_experiments(cost_matrix, configs, repetitions=5, output_file="experiment_results.csv"):
    results = []
    total_experiments = len(configs) * repetitions
    experiment_counter = 0
    
    for config in configs:
        for rep in range(repetitions):
            start_time = time.time()
            algorithm = Algorithm(cost_matrix, **config)
            best_solution, best_cost = algorithm.run()
            execution_time = time.time() - start_time
            
            results.append({
                "population_size": config["population_size"],
                "crossover_prob": config["crossover_prob"],
                "mutation_prob": config["mutation_prob"],
                "max_generations": config["max_generations"],
                "k_value_tournament": config["k_value_tournament"],
                "replacement_count": config["replacement_count"],
                "best_solution": best_solution,
                "best_cost": best_cost,
                "execution_time": execution_time
            })
            
            experiment_counter += 1
            print(f"Experimento {experiment_counter}/{total_experiments} completado")
    
    # Guardar resultados en un archivo CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Resultados guardados en {output_file}")

def generate_configurations():
    # Definir los valores a probar para cada parámetro
    population_sizes = [100, 150, 200]
    crossover_probs = [0.7, 0.8, 0.9]
    mutation_probs = [0.05, 0.1, 0.2]
    max_generations = [500, 1000, 1500]
    k_values = [3, 5, 7]
    replacement_counts = [0.2, 0.3, 0.4]
    
    configurations = []
    for population_size, crossover_prob, mutation_prob, max_gen, k_value, replacement_count  in itertools.product(
        population_sizes, crossover_probs, mutation_probs, max_generations, k_values, replacement_counts):
        configurations.append({
            "population_size": population_size,
            "crossover_prob": crossover_prob,
            "mutation_prob": mutation_prob,
            "max_generations": max_gen,
            "k_value_tournament": k_value,
            "replacement_count": replacement_count
        })
    return configurations

def run_single_experiment(params=None):
    if params is not None:
        config = params
    else:
        # Solicitar los parámetros al usuario
        population_size = int(input("Tamaño de la población: "))
        crossover_prob = float(input("Probabilidad de cruce: "))
        mutation_prob = float(input("Probabilidad de mutación: "))
        max_generations = int(input("Máximo número de generaciones: "))
        k_value_tournament = int(input("Valor de K para torneo: "))
        replacement_count = float(input("Porcentaje de reemplazo (en base al tamaño de la poblacion): "))

        # Crear el diccionario con los parámetros
        config = {
            "population_size": population_size,
            "crossover_prob": crossover_prob,
            "mutation_prob": mutation_prob,
            "max_generations": max_generations,
            "k_value_tournament": k_value_tournament,
            "replacement_count": replacement_count
        }

    # Correr el experimento
    algorithm = Algorithm(file.edge_weights, **config, filename=f"{RESULTS_PATH}/experiment_{EXECUTION_NUMBER}.txt")

    save = input("¿Desea guardar los resultados? (s/n): ")
    save_file = False
    if save.lower() == "s":
        save_file = True

    best_solution, best_cost = algorithm.run(save_file)
    print(f"Mejor Solución Encontrada:\n")
    print(f"  Ruta: {best_solution}\n")
    print(f"  Costo Total (Fitness): {best_cost}\n")

    
while True:
    try:
        print("1. Ejecutar experimento personalizado")
        print("2. Ejecutar experimentos con múltiples configuraciones predefinidas (puede tardar has horas)")
        print("3. Ejecutar experimento usando aleatoriamente una de las mejores soluciones obtenidas de los experimentos")
        print("4. Mostrar los mejores resultados obtenidos en los experimentos")
        print("5. Salir")
        option = input("Seleccione una opción: ")

        if option == "1":
            run_single_experiment()
        elif option == "2":
            configurations = generate_configurations()
            print(f"Ejecutando {len(configurations)} configuraciones con 5 repeticiones cada una")
            run_experiments(file.edge_weights, configurations, repetitions=5, output_file=f"{RESULTS_PATH}/experiment_results.csv")
        elif option == "3":
            # Usar una configuracion aleatoria de el paso anterior
            analyze = Analyze(PROBLEM)
        
            # Obtener una fila random
            random_row = analyze.get_best_solution().sample()
            
            if random_row.empty:
                print("No hay resultados para mostrar")
                continue

            paramsDict = random_row.to_dict()
            # Dar formato para que sea key => valor
            params = {key: list(value.values())[0] for key, value in paramsDict.items()}
            # Eliminar la columna de best_solution, best_cost y execution_time
            del params['best_solution']
            del params['best_cost']
            del params['execution_time']

            run_single_experiment(params)
        elif option == "4":
            print("Análisis de resultados")
            analyze = Analyze(PROBLEM)
            print(analyze.get_best_solution().to_string(index=False))
        elif option == "5":
            break
        else:
            print("Opción no válida")
            continue
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        continue

