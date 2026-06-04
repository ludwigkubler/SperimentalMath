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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def vector_space_from_cnf(cnf):
        variables = set(abs(lit) for clause in cnf for lit in clause)
        n_vars = max(variables)
        V = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    V[lit][i + 1] += 1
                else:
                    V[-lit][i + 1] -= 1
        return V
    
    def minimal_index_of_adjointness(V):
        n = len(V)
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    I[i][j] = sum(V[i][k] * V[j][k] for k in range(1, n + 1))
        min_index = float('inf')
        for row in I:
            min_index = min(min_index, max(row) - min(row))
        return min_index
    
    def resolution_width(cnf):
        stack = []
        visited = set()
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                break
            lit = unit_clause[0]
            visited.add(abs(lit))
            cnf = [c for c in cnf if lit not in c and -lit not in c]
            stack.append(unit_clause)
        return max(len(stack), len(visited))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        V = vector_space_from_cnf(cnf)
        min_index = minimal_index_of_adjointness(V)
        width = resolution_width(cnf)
        metrics.append((min_index, width))
    
    if not metrics:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_indices, widths = zip(*metrics)
    correlation_coefficient = sum((mi - mean(min_indices)) * (w - mean(widths)) for mi, w in metrics) / (len(metrics) * std_dev(min_indices) * std_dev(widths))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std_dev([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criterion")