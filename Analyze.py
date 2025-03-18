import pandas as pd

class Analyze:
    def __init__(self, problem, filename = "experiment_results.csv"):
        self.problem = problem
        self.path = f'./problems/{problem}/results/{filename}'

    def get_best_solution(self):
        """
        Lee un archivo CSV con las columnas:
        population_size, crossover_prob, mutation_prob, max_generations,
        best_solution, best_cost, execution_time,
        y retorna la(s) fila(s) con el menor valor de best_cost.
        """
        # Leer el archivo CSV
        df = pd.read_csv(self.path)
        
        # Encontrar el valor mínimo de 'best_cost'
        min_cost = df['best_cost'].min()
        
        # Seleccionar las filas con el menor best_cost
        best_rows = df[df['best_cost'] == min_cost]

        save = input("¿Desea guardar los resultados en un archivo CSV? (s/n): ")

        if save == "s":
            best_rows.to_csv(f"best_solutions_{self.problem}.csv", index=False)
            print("Resultados guardados en best_solutions.csv")
        
        return best_rows
    