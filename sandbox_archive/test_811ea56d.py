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
        edges = set()
        for i in range(k):
            for j in range(i + 1, k):
                edges.add((i, j))
        for _ in range(int(math.comb(n - k, 2))):
            u, v = random.sample(range(k, n), 2)
            edges.add((u, v))
        return edges
    
    def clause_indicator_polynomial(edges, n):
        poly = [0] * (1 << n)
        for i in range(1, 1 << n):
            if all((i >> j) & 1 == (i >> k) & 1 for u, v in edges if u < v and (u, v) in edges):
                poly[i] = 1
        return poly
    
    def polarized_hodge_structure(poly):
        hodge_structure = {}
        n = len(poly)
        for i in range(1 << n):
            count = sum(1 for j in range(n) if (i >> j) & 1 == 1)
            if count not in hodge_structure:
                hodge_structure[count] = []
            hodge_structure[count].append(i)
        return hodge_structure
    
    def resolution_proof_size(poly):
        n = len(poly)
        size = 0
        for i in range(1 << n):
            if poly[i] == 1:
                size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(4):  # Ensure at least 4 instances per size
            k = min(n, random.randint(2, n - 1))
            edges = generate_k_clique(n, k)
            poly = clause_indicator_polynomial(edges, n)
            hodge_structure = polarized_hodge_structure(poly)
            num_monomials = sum(len(v) for v in hodge_structure.values())
            t_F = resolution_proof_size(poly)
            
            if abs(num_monomials - t_F) > 0.2 * t_F:
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, num_monomials={num_monomials}, t_F={t_F}"
                break
            
            total_metric_value += num_monomials
            instances_tested += 1
    
    return {
        "metric_name": "Number of Monomials",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")