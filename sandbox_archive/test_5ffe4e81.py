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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2 ** n)]
    
    def permutation_group_representation(f):
        n = int(math.log2(len(f)))
        G = []
        for i in range(2 ** n):
            row = [0] * (2 ** n)
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    row[i ^ (1 << j)] = 1
            G.append(row)
        return G
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if i == j:
                    continue
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_comm = 0
        for i in range(2 ** n):
            comm = sum(1 for j in range(n) if f[i ^ (1 << j)] != f[i])
            max_comm = max(max_comm, comm)
        return max_comm
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexities = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        G = permutation_group_representation(f)
        min_rank_value = min_rank(G)
        comm_complexity_value = communication_complexity(f)
        
        min_ranks.append(min_rank_value)
        comm_complexities.append(comm_complexity_value)
    
    correlation_coefficient = 0
    if len(min_ranks) > 1 and len(comm_complexities) > 1:
        mean_ranks = sum(min_ranks) / len(min_ranks)
        mean_comm = sum(comm_complexities) / len(comm_complexities)
        
        numerator = sum((min_ranks[i] - mean_ranks) * (comm_complexities[i] - mean_comm) for i in range(len(min_ranks)))
        denominator = math.sqrt(sum((min_ranks[i] - mean_ranks) ** 2 for i in range(len(min_ranks)))) * math.sqrt(sum((comm_complexities[i] - mean_comm) ** 2 for i in range(len(comm_complexities))))
        
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
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(res['counterexample'] for res in results if 'counterexample' in res)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no data")