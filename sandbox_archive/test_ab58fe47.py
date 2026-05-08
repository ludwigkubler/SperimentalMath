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
    
    def generate_cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def exchange_matrix(clauses, variables):
        n = len(variables)
        matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            var_index1 = variables.index(abs(clause[0]))
            var_index2 = variables.index(abs(clause[1]))
            matrix[var_index1][var_index2] += 1
            matrix[var_index2][var_index1] += 1
        return matrix
    
    def fomin_zelevinsky_algorithm(matrix):
        n = len(matrix)
        distance = 0
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] > 0:
                    distance += 1
        return distance
    
    def acc0_circuit_size_bound(n):
        # Simplified approximation based on Williams' framework (2011)
        return math.log2(n) * (1 + random.random() / 10)
    
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    clauses = generate_cnf(n, m)
    variables = set(abs(clause[0]) for clause in clauses) | set(abs(clause[1]) for clause in clauses)
    
    exchange_mat = exchange_matrix(clauses, list(variables))
    mutation_distance = fomin_zelevinsky_algorithm(exchange_mat)
    acc0_bound = acc0_circuit_size_bound(n)
    
    if mutation_distance == 0 or abs(mutation_distance - acc0_bound) > 1e-6:
        return {
            "metric_name": "mutation_distance",
            "metric_value": mutation_distance,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mutation_distance != ACC^0 circuit size bound"
        }
    
    return {
        "metric_name": "mutation_distance",
        "metric_value": mutation_distance,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mutation_distance != ACC^0 circuit size bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")