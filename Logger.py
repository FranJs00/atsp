class Logger:
    def __init__(self, filename, params):
        self.filename = filename
        self.params = params

    def save_results(self, fitness_history, best_solution, best_fitness, execution_time):
        with open(self.filename, 'a') as file:
            file.write("=== Resultados de Ejecución ===\n")
            file.write(f"Configuración del Algoritmo Evolutivo:\n")
            for key, value in self.params.items():
                file.write(f"  {key}: {value}\n")
            
            file.write("\nEvolución del Fitness:\n")
            for generation, fitness in enumerate(fitness_history):
                file.write(f"  Generación {generation + 1}: Mejor Fitness = {-fitness}\n")
            
            file.write("\nMejor Solución Encontrada:\n")
            file.write(f"  Ruta: {best_solution}\n")
            file.write(f"  Costo Total (Fitness): {-best_fitness}\n")
            
            file.write(f"\nTiempo de Ejecución: {execution_time:.2f} segundos\n")
            file.write("=================================\n\n")
        print (f"Resultados guardados en {self.filename}")