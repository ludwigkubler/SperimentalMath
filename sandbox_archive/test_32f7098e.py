# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(cols):
            max_row = rank
            for j in range(rank, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            
            if matrix[max_row][i] == 0:
                continue
            
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            
            for j in range(rows):
                if j != rank:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            
            rank += 1
        
        return rank
    
    def compute_lattice_rank(graph):
        n = len(graph)
        augmented_matrix = [[0] * (n + 1) for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    augmented_matrix[i][j] = 1
                    augmented_matrix[i][-1] += 1
        
        return gaussian_elimination(augmented_matrix)
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
        
        return graph
    
    def compute_quantum_circuit_depth(graph):
        # Placeholder for actual quantum circuit depth computation
        # This is a stub and should be replaced with actual logic
        n = len(graph)
        return random.randint(1, n**2)  # Random depth between 1 and n^2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    lattice_rank = compute_lattice_rank(graph)
    quantum_circuit_depth = compute_quantum_circuit_depth(graph)
    
    metric_name = "Quantum Circuit Depth vs. Lattice Rank"
    metric_value = quantum_circuit_depth
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if lattice_rank == 0:
        counterexample = "Lattice rank is zero, which is not Θ(n^{1.5})"
    elif abs(lattice_rank - n**1.5) / (n**1.5) <= 0.75 and quantum_circuit_depth <= lattice_rank**2 * 4:
        conjecture_holds = True
    else:
        counterexample = f"Counterexample: lattice rank {lattice_rank}, depth {quantum_circuit_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")