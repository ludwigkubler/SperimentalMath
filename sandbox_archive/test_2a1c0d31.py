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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_d_regular_graph(d: int, n: int) -> list:
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        
        while any(count != d for count in degree_count):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or graph[u][v] == 1:
                continue
            graph[u][v] = 1
            graph[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
        
        return graph
    
    def matrix_multiplication(A: list, B: list) -> list:
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A: list) -> int:
        n = len(A)
        rank = 0
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
            rank += 1
        return rank
    
    def symmetry_breaking_number(graph: list) -> int:
        n = len(graph)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        zero_matrix = [[0] * n for _ in range(n)]
        
        for k in range(1, n):
            powers_of_k = [identity]
            current_power = matrix_multiplication(identity, graph)
            while current_power != identity:
                powers_of_k.append(current_power)
                current_power = matrix_multiplication(current_power, graph)
            
            if len(powers_of_k) == 2:
                return k
        
        return n
    
    def communication_complexity_rank(graph: list) -> int:
        n = len(graph)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    rank += 1
        return rank
    
    def pearson_correlation_coefficient(x: list, y: list) -> float:
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    d_values = [3, 4, 5]
    results = []
    
    for d in d_values:
        for _ in range(10):
            graph = generate_d_regular_graph(d, 20)
            sbn = symmetry_breaking_number(graph)
            cc_rank = communication_complexity_rank(graph)
            results.append((sbn, cc_rank))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 20,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*results)
    correlation_coefficient = pearson_correlation_coefficient(x, y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 20,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")