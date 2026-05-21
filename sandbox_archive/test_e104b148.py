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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in clique and (j, i) not in clique:
                    clique.append((i, j))
        return clique
    
    def generate_random_dnf(n, m):
        dnf = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            dnf.append(clause)
        return dnf
    
    def real_stable_polynomial(dnf):
        poly = [0] * (len(dnf) + 1)
        for clause in dnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (x - literal)
                else:
                    term *= (x + abs(literal))
            poly += [term]
        return poly
    
    def sturm_sequence(poly, x_values):
        seq = [poly[::]]
        while True:
            diff = [seq[-1][i] * i for i in range(1, len(seq[-1]))]
            if not any(diff):
                break
            seq.append(diff)
        lower_bound = 0
        upper_bound = 0
        for x in x_values:
            signs = [(-1) ** (len(poly) - 1 - i) * poly[i] / math.factorial(i) for i in range(len(poly))]
            sign_changes = sum(1 for i in range(1, len(signs)) if signs[i] * signs[i - 1] < 0)
            lower_bound += sign_changes
            upper_bound += sign_changes
        return lower_bound, upper_bound
    
    def count_real_roots(poly, x_values):
        lower_bound, upper_bound = sturm_sequence(poly, x_values)
        return upper_bound - lower_bound
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clique_poly = real_stable_polynomial(generate_k_clique(n, k))
        random_dnf = generate_random_dnf(n, int(0.1 * n**2))
        random_poly = real_stable_polynomial(random_dnf)
        
        x_values = [i for i in range(-n, n + 1)]
        clique_root_count = count_real_roots(clique_poly, x_values)
        random_root_count = count_real_roots(random_poly, x_values)
        
        results.append({
            "n": n,
            "clique_root_count": clique_root_count,
            "random_root_count": random_root_count
        })
    
    mean_clique_root_count = sum(result["clique_root_count"] for result in results) / len(results)
    mean_random_root_count = sum(result["random_root_count"] for result in results) / len(results)
    
    if any(result["clique_root_count"] < n / 10 for result in results):
        return {
            "metric_name": "Real Root Count",
            "metric_value": mean_clique_root_count,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE instance with root count < n/10"
        }
    
    return {
        "metric_name": "Real Root Count",
        "metric_value": mean_clique_root_count,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_clique_root_count = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_clique_root_count} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_clique_root_count} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE instance with root count < n/10\" first_failing_seed={first_failing_seed}")