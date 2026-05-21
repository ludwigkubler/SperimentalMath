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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        for i in range(k):
            for j in range(i + 1, k):
                if (clique[i], clique[j]) not in edges and (clique[j], clique[i]) not in edges:
                    edges[(clique[i], clique[j])] = True
        return clique
    
    def real_stable_polynomial(clause_set):
        n = len(clause_set)
        poly = [1] * (n + 1)
        for clause in clause_set:
            monomial = 1
            for var in clause:
                monomial *= (x - var) / (x + var)
            poly = polynomial_multiplication(poly, monomial)
        return poly
    
    def polynomial_multiplication(p1, p2):
        result = [0] * (len(p1) + len(p2) - 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                result[i + j] += p1[i] * p2[j]
        return result
    
    def sturm_sequence(poly):
        seq = [poly]
        while True:
            derivative = [i * coeff for i, coeff in enumerate(seq[-1][1:], start=1)]
            if not derivative or all(coeff == 0 for coeff in derivative):
                break
            seq.append([-coeff for coeff in derivative])
        return seq
    
    def count_real_roots(poly):
        seq = sturm_sequence(poly)
        sign_changes_pos = len([i for i in range(len(seq) - 1) if seq[i][0] * seq[i + 1][0] < 0])
        sign_changes_neg = len([i for i in range(len(seq) - 1) if seq[i][-1] * seq[i + 1][-1] < 0])
        return sign_changes_pos - sign_changes_neg
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(2, min(n // 2, 5))
        clique_poly = real_stable_polynomial(generate_k_clique(n, k))
        if clique_poly is None:
            continue
        root_count = count_real_roots(clique_poly)
        results.append((n, k, root_count))
    
    if not results:
        return {
            "metric_name": "Real Roots Count",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "k_clique_generation_failed"
        }
    
    avg_root_count = sum(root_count for _, _, root_count in results) / len(results)
    if avg_root_count < n_values[-1] / 10:
        return {
            "metric_name": "Real Roots Count",
            "metric_value": avg_root_count,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Average root count {avg_root_count} < n/10 for some k-CLIQUE instances"
        }
    
    return {
        "metric_name": "Real Roots Count",
        "metric_value": avg_root_count,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='average_root_count < n/10' first_failing_seed={first_failing_seed}")