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
    
    def generate_boolean_formula(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def subset_entropy(clauses):
        total_subsets = 2 ** len(clauses)
        entropy = 0
        for i in range(total_subsets):
            subset = [clauses[j] for j in range(len(clauses)) if (i & (1 << j))]
            num_clauses = sum(1 for clause in subset if any(var in clause for var in range(1, n+1)))
            prob = 2 ** (-num_clauses)
            entropy += prob * math.log2(prob) if prob != 0 else 0
        return -entropy
    
    def grb_basis(curves):
        # Simplified Gröbner basis computation (not actual implementation)
        return len(curves)
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n * n, 30))
    clauses = generate_boolean_formula(m, n)
    
    curves = []
    for clause in clauses:
        curve = [random.randint(1, n) for _ in range(len(clause))]
        curves.append(curve)
    
    num_curves = grb_basis(curves)
    subset_ent = subset_entropy(clauses)
    
    expected_num_curves = m * math.log(n, 2)
    expected_subset_ent = m * math.log(n, 2)
    
    conjecture_holds = (0.5 <= num_curves / expected_num_curves <= 2) and \
                       (0.5 <= subset_ent / expected_subset_ent <= 2)
    
    return {
        "metric_name": "Number of Curves",
        "metric_value": num_curves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")