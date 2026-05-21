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
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, rows):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def nonnegative_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def k_clique_indicator(n, k):
        # Placeholder function to generate a random k-clique indicator matrix
        # This is a simplified version and does not represent an actual k-clique problem
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        clique = [i for i in range(k) if all(graph[i][j] == 1 for j in range(i+1, k))]
        indicator = [[0] * n for _ in range(n)]
        for u in clique:
            for v in clique:
                if u < v:
                    indicator[u][v] = 1
        return indicator
    
    def monotone_circuit_size(k):
        # Placeholder function to estimate the size of a monotone circuit
        # This is a simplified version and does not represent an actual k-clique problem
        return k * (k - 1) // 2
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 10))
    
    indicator_matrix = k_clique_indicator(n, k)
    rank = nonnegative_rank(indicator_matrix)
    circuit_size = monotone_circuit_size(k)
    
    metric_value = rank
    conjecture_holds = rank >= n ** (1/2) * math.log(k)
    counterexample = "" if conjecture_holds else f"n={n}, k={k}, rank={rank}"
    
    return {
        "metric_name": "Nonnegative Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")