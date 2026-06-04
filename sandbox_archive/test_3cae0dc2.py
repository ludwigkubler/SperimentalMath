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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def calculate_entropy(clauses):
        total_clauses = len(clauses)
        counts = {}
        for clause in clauses:
            key = tuple(sorted(clause))
            if key in counts:
                counts[key] += 1
            else:
                counts[key] = 1
        entropy = 0
        for count in counts.values():
            p = Fraction(count, total_clauses)
            entropy -= p * math.log2(p)
        return entropy
    
    def calculate_minimal_index(clauses):
        n = len(clauses[0])
        max_clause_length = max(len(clause) for clause in clauses)
        index = 2 ** (max_clause_length - 1)
        return index
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = calculate_entropy(cnf)
        minimal_index = calculate_minimal_index(cnf)
        results.append((n, entropy, minimal_index))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, entropies, minimal_indices = zip(*results)
    mean_entropy = sum(entropies) / len(entropies)
    mean_index = sum(minimal_indices) / len(minimal_indices)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((entropies[i] - mean_entropy) * (minimal_indices[i] - mean_index) for i in range(len(entropies)))
        denominator = math.sqrt(sum((entropies[i] - mean_entropy) ** 2 for i in range(len(entropies)))) * math.sqrt(sum((minimal_indices[i] - mean_index) ** 2 for i in range(len(minimal_indices))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
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
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")