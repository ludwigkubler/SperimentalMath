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
    
    def tseitin_formula(n, num_clauses):
        literals = list(range(1, n + 1))
        clauses = []
        
        # Create unit clauses for each literal
        for lit in literals:
            clauses.append([lit])
        
        # Create binary clauses
        for i in range(num_clauses - len(literals)):
            lit1 = random.choice(literals)
            lit2 = random.choice(literals)
            while lit1 == lit2:
                lit2 = random.choice(literals)
            clauses.append([-lit1, -lit2])
        
        # Create a final clause that is the OR of all literals
        final_clause = [lit for lit in literals]
        clauses.append(final_clause)
        
        return clauses
    
    def lie_algebra_lattice(clauses):
        n = len(clauses)
        lattice = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if any(lit in clauses[i - 1] and -lit in clauses[j - 1] for lit in literals):
                    lattice[i][j] = 1
                    lattice[j][i] = 1
        
        return lattice
    
    def min_index_of_automorphism_groups(lattice):
        n = len(lattice)
        rank = 0
        
        for i in range(n):
            if any(lattice[i][j] == 1 for j in range(i + 1, n)):
                row = [lattice[i][j] for j in range(n)]
                for j in range(n):
                    if lattice[j][i] == 1:
                        col = [lattice[k][j] for k in range(n)]
                        if all(row[k] == col[k] for k in range(n)):
                            rank += 1
                            break
        
        return n - rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    def mean_absolute_difference(x, y):
        return sum(abs(a - b) for a, b in zip(x, y)) / len(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    clause_counts = []
    
    for n in n_values:
        num_clauses = random.randint(n // 2, 2 * n)
        clauses = tseitin_formula(n, num_clauses)
        lattice = lie_algebra_lattice(clauses)
        min_index = min_index_of_automorphism_groups(lattice)
        
        min_indices.append(min_index)
        clause_counts.append(num_clauses)
    
    correlation = correlation_coefficient(min_indices, clause_counts)
    mean_diff = mean_absolute_difference(min_indices, [n for n in n_values])
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 3 else "Correlation too low or mean absolute difference too high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low or mean absolute difference too high\" first_failing_seed={first_failing_seed}")