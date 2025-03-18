import random
import time
from Logger import Logger

class Algorithm:
    def __init__(self, cost_matrix, population_size, crossover_prob, mutation_prob, k_value_tournament, max_generations, replacement_count, filename="results.txt"):
        self.Logger = Logger(filename=filename, params={
            "population_size": population_size,
            "crossover_prob": crossover_prob,
            "mutation_prob": mutation_prob,
            "k_value_tournament": k_value_tournament,
            "max_generations": max_generations,
            "replacement_count": replacement_count
            })
        self.cost_matrix = cost_matrix
        self.population_size = population_size
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.k_value_tournament = k_value_tournament
        self.max_generations = max_generations
        self.replacement_count = int(population_size * replacement_count)
    
    def generate_initial_population(self, size, n_cities):
        population = []
        for _ in range(size):
            individual = list(range(n_cities))
            random.shuffle(individual)
            population.append(individual)
        return population

    def calculate_fitness(self, individual, cost_matrix):
        total_cost = 0
        for i in range(len(individual)):
            from_city = individual[i]
            to_city = individual[(i + 1) % len(individual)]  # Regreso al inicio
            total_cost += cost_matrix[from_city][to_city]
        return -total_cost  # Fitness negativo porque queremos minimizar

    def tournament_selection(self, population, fitness, k):
        selected = random.choices(list(range(len(population))), k=k)
        best = min(selected, key=lambda idx: fitness[idx])  # Seleccionar el mejor
        return population[best]

    def pmx_crossover(self, parent1, parent2):
        size = len(parent1)
        child = [-1] * size
        start, end = sorted(random.sample(range(size), 2))
        
        # Copiar segmento
        child[start:end + 1] = parent1[start:end + 1]
        
        # Map genes de parent2
        for i in range(start, end + 1):
            if parent2[i] not in child:
                pos = i
                while child[pos] != -1:
                    pos = parent2.index(parent1[pos])
                child[pos] = parent2[i]
        
        # Llenar los genes restantes
        for i in range(size):
            if child[i] == -1:
                child[i] = parent2[i]
        return child

    def inversion_mutation(self, individual):
        start, end = sorted(random.sample(range(len(individual)), 2))
        individual[start:end + 1] = reversed(individual[start:end + 1])
        return individual

    def steady_state_selection(self, population, offspring, fitness, offspring_fitness):
        N = len(population)
        
        if self.replacement_count > len(offspring):
            raise ValueError("El número de reemplazos no puede ser mayor que la cantidad de descendientes generados.")
        
        # Ordenar la población actual de mayor a menor fitness
        pop_sorted = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
        # Seleccionar los mejores (N - replacement_count) individuos de la población actual
        survivors = [ind for ind, fit in pop_sorted[:N - self.replacement_count]]
        
        # Ordenar los descendientes de mayor a menor fitness
        offspring_sorted = sorted(zip(offspring, offspring_fitness), key=lambda x: x[1], reverse=True)
        # Seleccionar los mejores 'replacement_count' descendientes
        replacements = [ind for ind, fit in offspring_sorted[:self.replacement_count]]
        
        # Combinar los sobrevivientes y los reemplazos para formar la nueva población
        new_population = survivors + replacements
        return new_population

    def run(self, save_results=False):
        n_cities = len(self.cost_matrix)
        population = self.generate_initial_population(self.population_size, n_cities)
        fitness = [self.calculate_fitness(ind, self.cost_matrix) for ind in population]
        fitness_history = []  # Para registrar la evolución del fitness
        
        start_time = time.time()  # Iniciar el temporizador
        
        for generation in range(self.max_generations):
            new_population = []
            
            while len(new_population) < self.population_size:
                # Selección de padres
                parent1 = self.tournament_selection(population, fitness, self.k_value_tournament)
                parent2 = self.tournament_selection(population, fitness, self.k_value_tournament)
                
                # Cruce
                if random.random() < self.crossover_prob:
                    child = self.pmx_crossover(parent1, parent2)
                else:
                    child = parent1[:]
                
                # Mutación
                if random.random() < self.mutation_prob:
                    child = self.inversion_mutation(child)
                
                new_population.append(child)
            
            # Fitness de la nueva población
            offspring_fitness = [self.calculate_fitness(ind, self.cost_matrix) for ind in new_population]
            
            # Selección de sobrevivientes
            population = self.steady_state_selection(population, new_population, fitness, offspring_fitness)
            fitness = [self.calculate_fitness(ind, self.cost_matrix) for ind in population]
            
            # Mejor individuo de esta generación
            best_fitness = max(fitness)
            fitness_history.append(best_fitness)
            print(f"Generación {generation + 1}: Mejor fitness = {-best_fitness}")
        
        # Mejor solución final
        best_index = fitness.index(max(fitness))
        best_solution = population[best_index]
        execution_time = time.time() - start_time  # Calcular el tiempo total

        if save_results:
            self.Logger.save_results(fitness_history, best_solution, best_fitness, execution_time)
        
        return population[best_index], -fitness[best_index]
