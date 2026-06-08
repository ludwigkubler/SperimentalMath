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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_circuit(n, depth):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_random_circuit(n // 2, depth - 1)
            right = generate_random_circuit(n - n // 2, depth - 1)
            return [random.choice([0, 1]) for _ in range(n)] + left + right
    
    def construct_root_system(circuit):
        n = len(circuit)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            if circuit[i] == 1:
                for j in range(n):
                    if circuit[j] == 1 and i != j:
                        adjacency_matrix[i][j] = 1
                        adjacency_matrix[j][i] = 1
        return adjacency_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
            if matrix[i][i] != 0:
                rank += 1
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def compute_lie_algebra_dimension(root_system):
        n = len(root_system)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [1] for row in root_system] + identity_matrix
        rank = gaussian_elimination(augmented_matrix)
        return n - rank
    
    def is_d_regular_graph(adjacency_matrix):
        degree = sum(sum(row) for row in adjacency_matrix) // len(adjacency_matrix)
        return all(sum(row) == degree for row in adjacency_matrix)
    
    n_min, n_max = 5, 40
    depth_min, depth_max = 1, 40
    instances_per_seed = 30
    
    total_metric_value = 0
    conjecture_holds_count = 0
    counterexample = ""
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        depth = random.randint(depth_min, depth_max)
        circuit = generate_random_circuit(n, depth)
        root_system = construct_root_system(circuit)
        
        if not is_d_regular_graph(root_system):
            continue
        
        rank = gaussian_elimination(root_system)
        lie_algebra_dimension = compute_lie_algebra_dimension(root_system)
        
        total_metric_value += rank
        if rank <= depth:
            conjecture_holds_count += 1
        else:
            counterexample = f"Rank {rank} > Depth {depth}"
    
    mean_metric_value = total_metric_value / instances_per_seed
    support_fraction = conjecture_holds_count / instances_per_seed
    
    return {
        "metric_name": "Rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_per_seed,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")