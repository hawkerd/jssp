import random
import copy

# FT06 problem definition: [ (machine, duration), ... ]
FT06_DATA = [
    [(1, 1), (2, 3), (3, 6), (4, 7), (5, 3), (0, 6)],  # Job 0
    [(2, 8), (3, 5), (1, 10), (0, 10), (4, 4), (5, 8)],  # Job 1
    [(3, 5), (2, 4), (1, 8), (0, 9), (5, 1), (4, 7)],  # Job 2
    [(2, 9), (1, 6), (3, 9), (4, 8), (5, 7), (0, 5)],  # Job 3
    [(1, 3), (2, 7), (3, 8), (0, 9), (5, 5), (4, 10)],  # Job 4
    [(2, 9), (3, 10), (1, 4), (4, 6), (0, 10), (5, 9)],  # Job 5
]

NUM_JOBS = 6
NUM_MACHINES = 6
OPERATIONS_PER_JOB = 6
CHROMOSOME_LENGTH = NUM_JOBS * OPERATIONS_PER_JOB

def generate_random_chromosome():
    chrom = []
    for job_id in range(NUM_JOBS):
        chrom += [job_id] * OPERATIONS_PER_JOB
    random.shuffle(chrom)
    return chrom

def decode_and_evaluate(chromosome):
    job_progress = [0] * NUM_JOBS
    machine_available_time = [0] * NUM_MACHINES
    job_available_time = [0] * NUM_JOBS
    operation_end_times = []

    for job_id in chromosome:
        op_index = job_progress[job_id]
        machine_id, duration = FT06_DATA[job_id][op_index]

        # Start time = when both the job and the machine are free
        start_time = max(machine_available_time[machine_id], job_available_time[job_id])
        end_time = start_time + duration

        # Update availability
        machine_available_time[machine_id] = end_time
        job_available_time[job_id] = end_time
        job_progress[job_id] += 1

        operation_end_times.append(end_time)

    return max(operation_end_times)  # Makespan

def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    return min(selected, key=lambda x: x[1])[0]

def crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[a:b] = parent1[a:b]
    fill_pos = 0
    for gene in parent2:
        if child.count(gene) < parent1.count(gene):
            while child[fill_pos] != -1:
                fill_pos += 1
            child[fill_pos] = gene
    return child, child[:]

def mutate(chromosome, rate=0.2):
    if random.random() < rate:
        a, b = random.sample(range(len(chromosome)), 2)
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]

def get_best_individual(population, fitnesses):
    best_idx = fitnesses.index(min(fitnesses))
    return population[best_idx], fitnesses[best_idx]

def genetic_algorithm(pop_size=50, generations=200):
    population = [generate_random_chromosome() for _ in range(pop_size)]
    fitnesses = [decode_and_evaluate(ind) for ind in population]
    best_solution, best_fitness = get_best_individual(population, fitnesses)

    for _ in range(generations):
        new_population = []
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        new_fitnesses = [decode_and_evaluate(ind) for ind in new_population]
        combined = list(zip(population + new_population, fitnesses + new_fitnesses))
        combined.sort(key=lambda x: x[1])  # sort by fitness (lower is better)
        population = [x[0] for x in combined[:pop_size]]
        fitnesses = [x[1] for x in combined[:pop_size]]

        current_best, current_fitness = get_best_individual(population, fitnesses)
        if current_fitness < best_fitness:
            best_solution, best_fitness = current_best, current_fitness

    return best_solution, best_fitness

if __name__ == "__main__":
    best_solution, best_fitness = genetic_algorithm()
    print("Best solution:", best_solution)
    print("Best makespan:", best_fitness)