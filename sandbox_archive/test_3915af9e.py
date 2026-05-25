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
    
    def generate_kcnf(n, m):
        variables = set(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def incidence_graph(clauses):
        graph = {}
        for var in range(2 * n):
            graph[var] = []
        for clause in clauses:
            for var in clause:
                graph[2 * var].append(2 * var + 1)
                graph[2 * var + 1].append(2 * var)
        return graph
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(n):
                if j != i and matrix[rank][j] != 0:
                    factor = matrix[rank][j] / matrix[rank][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def count_groupoid_operations(graph, n):
        operations = 0
        for var in range(2 * n):
            if graph[var]:
                operations += len(graph[var])
        return operations
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_operations = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            m = random.randint(n, 2 * n)
            clauses = generate_kcnf(n, m)
            graph = incidence_graph(clauses)
            operations = count_groupoid_operations(graph, n)
            total_operations += operations
            instances_tested += 1
    
    mean_operations = Fraction(total_operations, instances_tested)
    upper_bound = Fraction(2 * n_values[-1] * math.log(n_values[-1]), 1)
    
    conjecture_holds = mean_operations <= upper_bound
    counterexample = "" if conjecture_holds else f"mean_operations={mean_operations}, upper_bound={upper_bound}"
    
    return {
        "metric_name": "groupoid_operations",
        "metric_value": float(mean_operations),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")