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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def minimal_rank_of_quadratic_form(clauses):
        n = len(clauses)
        Q = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i, x1 in enumerate(clause):
                for j, x2 in enumerate(clause):
                    if i <= j:
                        Q[i][j] += x1 * x2
        Q = gaussian_elimination(Q)
        rank = sum(1 for row in Q if any(row))
        return rank
    
    def resolution_refutation_size(clauses):
        # Simplified version of resolution refutation size calculation
        return len(clauses) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    refutations = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        rank = minimal_rank_of_quadratic_form(clauses)
        refutation_size = resolution_refutation_size(clauses)
        ranks.append(rank)
        refutations.append(refutation_size)
    
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (refutations[i] - mean(refutations)) for i in range(len(n_values))) / len(n_values) / stdev(ranks) / stdev(refutations)
    
    result = {
        "metric_name": "CorrelationCoefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": abs(correlation_coefficient) <= 0.7 and all(abs(corr) > 0.3 for corr in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient <= -0.7 else f"Correlation coefficient: {correlation_coefficient}"
    }
    
    return result

def mean(lst):
    return sum(lst) / len(lst)

def stdev(lst):
    avg = mean(lst)
    variance = sum((x - avg) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = stdev([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] and "Correlation coefficient" in r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")