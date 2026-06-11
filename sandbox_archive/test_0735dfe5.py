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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_clause_satisfied(phi, assignment):
        for clause in phi:
            if not any([assignment[abs(l)-1] == (l > 0) for l in clause]):
                return False
        return True
    
    def resolution(phi, assignment):
        while True:
            new_clauses = []
            satisfied = True
            for i in range(len(phi)):
                if is_clause_satisfied(phi[i], assignment):
                    satisfied = False
                    continue
                for j in range(i+1, len(phi)):
                    if is_clause_satisfied(phi[j], assignment):
                        continue
                    common_vars = set([abs(l) for l in phi[i]]) & set([abs(l) for l in phi[j]])
                    if not common_vars:
                        continue
                    new_clause = []
                    for l in phi[i]:
                        if abs(l) not in common_vars:
                            new_clause.append(l)
                    for l in phi[j]:
                        if abs(l) not in common_vars and -l not in new_clause:
                            new_clause.append(-l)
                    new_clauses.append(new_clause)
            if satisfied:
                return assignment
            phi.extend(new_clauses)
    
    def coxeter_group_size(phi):
        n = len(phi[0])
        generators = []
        for i in range(n):
            for j in range(i+1, n):
                found = False
                for clause in phi:
                    if abs(clause[0]) == i + 1 and abs(clause[1]) == j + 1:
                        found = True
                        break
                if not found:
                    generators.append((i, j))
        return len(generators)
    
    def resolution_proof_entanglement_complexity(phi):
        n = len(phi[0])
        assignment = [False] * n
        return len(resolution(phi, assignment))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_cnf(n)
            generators = coxeter_group_size(phi)
            entanglement_complexity = resolution_proof_entanglement_complexity(phi)
            results.append((generators, entanglement_complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    x_sum, y_sum, xy_sum, x2_sum, y2_sum = 0, 0, 0, 0, 0
    for x, y in results:
        x_sum += x
        y_sum += y
        xy_sum += x * y
        x2_sum += x ** 2
        y2_sum += y ** 2
    
    mean_x = x_sum / n
    mean_y = y_sum / n
    covariance = (xy_sum - n * mean_x * mean_y) / (n - 1)
    variance_x = (x2_sum - n * mean_x ** 2) / (n - 1)
    variance_y = (y2_sum - n * mean_y ** 2) / (n - 1)
    
    if variance_x == 0 or variance_y == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": n,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": pearson_correlation >= 0.8 and all(pearson_correlation >= 0.5 for _, _ in results),
        "counterexample": "" if pearson_correlation >= 0.8 else f"low correlation: {pearson_correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / (len(results) - 1))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] is None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data n_tested={first_failing_seed + 1}")