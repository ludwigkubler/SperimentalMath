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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2 ** n)]
    
    def permutation_group_representation(f):
        n = len(f)
        G = []
        for i in range(2 ** n):
            row = [0] * (2 ** n)
            for j in range(2 ** n):
                if f[(i ^ j) % (2 ** n)] == 1:
                    row[j] = 1
            G.append(row)
        return G
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(2 ** n):
            comm = sum(f[(i ^ j) % (2 ** n)] for j in range(2 ** n))
            if comm > max_comm:
                max_comm = comm
        return max_comm
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if matrix[i][i] != 1:
                for j in range(i + 1, m):
                    if matrix[j][i] == 1:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
            for j in range(n):
                if i != j and matrix[i][j] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(m):
                        matrix[k][j] += factor * matrix[k][i]
        rank = sum(1 for row in matrix if any(row))
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
    
    correlation_coefficient = 0
    if len(min_ranks) > 1 and len(comm_complexities) > 1:
        mean_r_f = sum(min_ranks) / len(min_ranks)
        mean_c_f = sum(comm_complexities) / len(comm_complexities)
        numerator = sum((min_ranks[i] - mean_r_f) * (comm_complexities[i] - mean_c_f) for i in range(len(min_ranks)))
        denominator = math.sqrt(sum((min_r_f - mean_r_f) ** 2 for r_f in min_ranks)) * math.sqrt(sum((c_f - mean_c_f) ** 2 for c_f in comm_complexities))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")