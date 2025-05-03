import random
import math
from collections import defaultdict

# FT06 Problem
FT06_DATA = [
    [(1, 1), (2, 3), (3, 6), (4, 7), (5, 3), (0, 6)],
    [(3, 8), (2, 5), (1, 10), (0, 10), (5, 4), (4, 1)],
    [(2, 5), (3, 4), (4, 8), (1, 9), (0, 1), (5, 7)],
    [(1, 5), (0, 5), (2, 5), (3, 3), (4, 8), (5, 9)],
    [(2, 9), (1, 3), (4, 5), (5, 4), (0, 3), (3, 1)],
    [(1, 3), (3, 3), (5, 9), (0, 10), (2, 4), (4, 1)],
]

NUM_JOBS = len(FT06_DATA)
OPS_PER_JOB = len(FT06_DATA[0])

def generate_random_solution():
    sequence = []
    for job_id in range(NUM_JOBS):
        sequence += [job_id] * OPS_PER_JOB
    random.shuffle(sequence)
    return sequence

def cost(sequence):
    job_indices = [0] * NUM_JOBS
    machine_time = defaultdict(int)
    job_time = defaultdict(int)

    for job_id in sequence:
        op_idx = job_indices[job_id]
        machine, duration = FT06_DATA[job_id][op_idx]

        start_time = max(machine_time[machine], job_time[job_id])
        end_time = start_time + duration

        machine_time[machine] = end_time
        job_time[job_id] = end_time
        job_indices[job_id] += 1

    return max(job_time.values())

def generate_neighbor(solution):
    neighbor = solution[:]
    i, j = random.sample(range(len(neighbor)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing(T=1000.0, alpha=0.95, max_iter=1000):
    current = generate_random_solution()
    best = current
    best_cost = cost(current)

    for _ in range(max_iter):
        neighbor = generate_neighbor(current)
        delta = cost(neighbor) - cost(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = cost(current)
            if current_cost < best_cost:
                best = current
                best_cost = current_cost

        T *= alpha
        if best_cost == 55:  # known optimal
            break

    return best, best_cost

# Run SA
best_sequence, best_makespan = simulated_annealing()
print("Best sequence found:", best_sequence)
print("Best makespan:", best_makespan)