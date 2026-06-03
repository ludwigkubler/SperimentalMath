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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(1 << n):
            comm = 0
            for j in range(i + 1, 1 << n):
                if f[i] != f[j]:
                    comm += 1
            max_comm = max(max_comm, comm)
        return max_comm
    
    def permutation_group_representation(f):
        n = len(f)
        G = []
        for i in range(1 << n):
            row = [0] * (1 << n)
            for j in range(1 << n):
                if f[i] == f[j]:
                    row[j] = 1
            G.append(row)
        return G
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            max_row = -1
            for j in range(i, m):
                if sum(abs(matrix[j][k]) for k in range(n)) > sum(abs(matrix[max_row][k]) for k in range(n)):
                    max_row = j
            if matrix[max_row][i] != 0:
                rank += 1
                for j in range(n):
                    matrix[i][j], matrix[max_row][j] = matrix[max_row][j], matrix[i][j]
                for j in range(m):
                    if i != j:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        G = permutation_group_representation(f)
        r_f = min_rank(G)
        c_f = communication_complexity(f)
        min_ranks.append(r_f)
        comm_complexities.append(c_f)
    
    correlation_coefficient = sum((min_ranks[i] - mean(min_ranks)) * (comm_complexities[i] - mean(comm_complexities)) for i in range(len(n_values))) / len(n_values) / math.sqrt(sum((min_ranks[i] - mean(min_ranks))**2 for i in range(len(n_values)))) / math.sqrt(sum((comm_complexities[i] - mean(comm_complexities))**2 for i in range(len(n_values))))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds are provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")