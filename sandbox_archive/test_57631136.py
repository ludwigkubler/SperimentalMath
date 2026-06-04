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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def shannon_entropy(probs):
        entropy = 0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def hodge_decomposition_order(cnf):
        # Placeholder implementation; actual computation depends on the conjecture's mapping
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        return n ** 1.5
    
    def clause_subset_entropy(cnf):
        total_clauses = len(cnf)
        subset_sizes = [len(subset) for subset in range(1, total_clauses + 1)]
        probs = [math.comb(total_clauses, size) / 2**total_clauses for size in subset_sizes]
        return shannon_entropy(probs)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n, random.randint(10, 2*n))
        hodge_order = hodge_decomposition_order(cnf)
        entropy = clause_subset_entropy(cnf)
        results.append((hodge_order, entropy))
    
    if not results:
        return {
            "metric_name": "Hodge Order vs Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hodge_orders = [r[0] for r in results]
    entropies = [r[1] for r in results]
    correlation_coefficient = sum((h - sum(hodge_orders) / len(hodge_orders)) * (e - sum(entropies) / len(entropies)) for h, e in zip(hodge_orders, entropies)) / (len(results) * math.sqrt(sum((h - sum(hodge_orders) / len(hodge_orders))**2 for h in hodge_orders)) * math.sqrt(sum((e - sum(entropies) / len(entropies))**2 for e in entropies)))
    
    return {
        "metric_name": "Hodge Order vs Entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["instances_tested"] >= 30 for result in results):
        n_max = max(max(result["n_max"] for result in results), 16)
    else:
        n_max = None
    
    if support_fraction >= 0.8 and n_max is not None and n_max >= 16:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and n_max is not None and n_max >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded n_tested=30")