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

def generate_phi(n):
    phi = []
    for _ in range(n):
        clause = set()
        while len(clause) < 3:
            var = random.choice(range(1, n + 1))
            if var not in clause:
                clause.add(var)
        phi.append(list(clause))
    return phi

def polynomial(phi):
    p = [0] * (2 ** len(phi))
    for i in range(len(phi)):
        for assignment in range(2 ** len(phi[i])):
            product = 1
            for var in phi[i]:
                if (assignment >> (var - 1)) & 1:
                    product *= -1
            p[assignment] += product
    return p

def minimal_quadratic_residue_symbol(p):
    n = len(p)
    qrs = 0
    for i in range(n):
        if p[i] != 0:
            qrs = (qrs + p[i]) % 2
    return qrs

def dpll_search_tree(phi, assignment=0, path=[]):
    if len(path) == len(phi):
        return 1 if all(p >= 0 for p in polynomial(phi)) else 0
    
    var = phi[len(path)][0]
    count = 0
    count += dpll_search_tree(phi, assignment | (1 << (var - 1)), path + [True])
    count += dpll_search_tree(phi, assignment & ~(1 << (var - 1)), path + [False])
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_phi(n)
        p = polynomial(phi)
        qrs = minimal_quadratic_residue_symbol(p)
        d = dpll_search_tree(phi)
        results.append((qrs, d))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_total = len(results)
    qrs_values = [qrs for qrs, _ in results]
    d_values = [d for _, d in results]
    
    mean_qrs = sum(qrs_values) / n_total
    mean_d = sum(d_values) / n_total
    
    correlation = 0.0
    for qrs, d in results:
        correlation += (qrs - mean_qrs) * (d - mean_d)
    correlation /= (n_total * math.sqrt(sum((qrs - mean_qrs) ** 2 for qrs in qrs_values)) * math.sqrt(sum((d - mean_d) ** 2 for d in d_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n_total,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.5) / len(results)
    
    if all(abs(result["metric_value"]) >= 0.5 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")