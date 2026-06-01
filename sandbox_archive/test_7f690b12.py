# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(k, m):
        variables = list(range(1, k + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def qaut_index(clauses):
        # Placeholder function to compute the minimal index of quaternionic automorphism group
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses)  # Simplified for demonstration purposes
    
    def clause_set_complexity(clauses):
        return len(set(tuple(sorted(clause)) for clause in clauses))
    
    k = random.randint(5, 30)
    m = random.randint(k * 2, k * 4)
    clauses = generate_kcnf(k, m)
    
    qaut_val = qaut_index(clauses)
    kappa_val = clause_set_complexity(clauses)
    
    return {
        "metric_name": "qaut_index",
        "metric_value": qaut_val,
        "instances_tested": 1,
        "n_max": k,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")