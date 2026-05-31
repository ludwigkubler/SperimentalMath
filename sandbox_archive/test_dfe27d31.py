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
    
    def tseitin_formula(n, k):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Clause for each literal
        for var in variables:
            clauses.append([var])
        
        # Clause for each clause of the formula
        for i in range(n, n + k):
            literals = random.sample(variables, 2)
            clauses.append(literals)
            clauses.append([-l for l in literals])
        
        return clauses
    
    def lie_algebra_lattice(clauses):
        n = len(clauses)
        lattice = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                if any(lit in clauses[i - 1] and -lit in clauses[j - 1] for lit in variables):
                    lattice[i][j] = 1
                    lattice[j][i] = 1
        
        return lattice
    
    def min_index_of_automorphism_groups(lattice):
        n = len(lattice)
        rank = 0
        
        for i in range(n):
            if any(lattice[i][j] == 1 for j in range(i + 1, n)):
                for j in range(i + 1, n):
                    if lattice[j][i] == 1:
                        for k in range(n):
                            if lattice[k][j] == 1 and lattice[k][i] == 0:
                                lattice[k][i] = 1
                                rank += 1
        
        return rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        
        return numerator / denominator
    
    def mean_absolute_difference(x, y):
        n = len(x)
        return sum(abs(x[i] - y[i]) for i in range(n)) / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    clause_sizes = []
    
    for n in n_values:
        k = random.randint(n // 2, 2 * n)
        clauses = tseitin_formula(n, k)
        lattice = lie_algebra_lattice(clauses)
        min_index = min_index_of_automorphism_groups(lattice)
        
        min_indices.append(min_index)
        clause_sizes.append(k)
    
    correlation = correlation_coefficient(min_indices, clause_sizes)
    mean_diff = mean_absolute_difference(min_indices, [k for k in clause_sizes])
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 3 else f"Correlation: {correlation}, Mean Absolute Difference: {mean_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation or Mean Absolute Difference does not meet criteria\" first_failing_seed={first_failing_seed}")