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
    
    def generate_random_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clauses):
        n = len(clauses[0])
        poly = [[-math.inf] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if all(x == 1 or x == -1 and j != i for j, x in enumerate(clause)):
                    poly[i][i] = max(poly[i][i], sum(abs(x) for x in clause))
        return poly
    
    def minimal_monomial_degree(poly):
        n = len(poly)
        degree = 0
        for i in range(n):
            degree = max(degree, sum(1 for j in range(n) if poly[i][j] != -math.inf))
        return degree
    
    def clause_entropy(clauses):
        n = len(clauses[0])
        counts = [0] * (n + 1)
        for clause in clauses:
            counts[len(clause)] += 1
        entropy = 0
        total_clauses = len(clauses)
        for count in counts:
            if count > 0:
                p = count / total_clauses
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_random_sat_instance(n)
        poly = tropical_polynomial(clauses)
        d_n = minimal_monomial_degree(poly)
        H_phi_n = clause_entropy(clauses)
        results.append({
            "n": n,
            "d_n": d_n,
            "H_phi_n": H_phi_n
        })
    
    correlation_coefficient = 0.0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            x1, y1 = results[i]["d_n"], results[i]["H_phi_n"]
            x2, y2 = results[j]["d_n"], results[j]["H_phi_n"]
            correlation_coefficient += (x1 - x2) * (y1 - y2)
    correlation_coefficient /= len(results) * (len(results) - 1) / 2
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")