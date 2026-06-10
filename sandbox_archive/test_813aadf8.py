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
    
    def generate_circuit(n):
        circuit = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    circuit[i][j] = 1
                    circuit[j][i] = 1
        return circuit
    
    def rank_variance(matrix):
        n = len(matrix)
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        
        def gaussian_elimination(A, B=None):
            A = [row[:] for row in A]
            if B is not None:
                B = [b[:] for b in B]
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                if B is not None:
                    B[i], B[max_row] = B[max_row], B[i]
                for j in range(i + 1, n):
                    factor = A[j][i] / A[i][i]
                    A[j][i] = Fraction(0)
                    for k in range(i + 1, n):
                        A[j][k] -= factor * A[i][k]
                    if B is not None:
                        B[j] -= factor * B[i]
            return A, B
        
        _, U = gaussian_elimination(matrix)
        rank = sum(1 for row in U if any(x != Fraction(0) for x in row))
        det = 1
        for i in range(rank):
            det *= U[i][i]
        return (n - rank) / n
    
    def graphical_regularity(circuit):
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j] == 1:
                    G[i][j] = 1
                    G[j][i] = 1
        
        def dfs(v, visited):
            stack = [v]
            while stack:
                v = stack.pop()
                if not visited[v]:
                    visited[v] = True
                    for u in range(n):
                        if G[v][u] == 1 and not visited[u]:
                            stack.append(u)
        
        visited = [False] * n
        dfs(0, visited)
        return sum(not v for v in visited) / (n - 1)
    
    def simulate_protocol(circuit, protocol):
        n = len(circuit)
        results = []
        for _ in range(n):
            inputs = random.sample(range(n), n)
            output = circuit[inputs.index(0)][inputs.index(1)]
            if protocol == 'OR':
                result = any(circuit[i][j] == 1 for i, j in zip(inputs, inputs[1:]))
            elif protocol == 'AND':
                result = all(circuit[i][j] == 1 for i, j in zip(inputs, inputs[1:]))
            else:
                raise ValueError("Invalid protocol")
            results.append(result)
        return results
    
    n_values = [5, 10, 15, 20, 30, 40]
    gamma_sum = 0
    rho_n_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        circuit = generate_circuit(n)
        gamma = graphical_regularity(circuit)
        rho_n = rank_variance(circuit)
        
        if gamma is None or rho_n is None:
            return {
                "metric_name": "graphical_regularity vs rank_variance",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        gamma_sum += gamma
        rho_n_sum += rho_n
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_gamma = gamma_sum / instances_tested
    mean_rho_n = rho_n_sum / instances_tested
    support_fraction = sum(1 for _ in range(instances_tested) if abs(mean_gamma - mean_rho_n) <= 1) / instances_tested
    
    return {
        "metric_name": "graphical_regularity vs rank_variance",
        "metric_value": (mean_gamma, mean_rho_n),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and abs(mean_gamma - mean_rho_n) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gamma = sum(res["metric_value"][0] for res in results) / len(results)
    mean_rho_n = sum(res["metric_value"][1] for res in results) / len(results)
    support_fraction = sum(1 for res in results if abs(res["metric_value"][0] - res["metric_value"][1]) <= 1) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean_gamma={mean_gamma} mean_rho_n={mean_rho_n} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gamma not within 1 of rho_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")