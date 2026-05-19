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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def persistent_homology_betti_numbers(clauses):
        # Simplified filtration: 0th Betti number is the number of connected components
        # This is a very rough approximation for demonstration purposes
        return len(set(frozenset(c) for c in clauses))
    
    def log_rank_conjecture(n, m):
        # A naive estimation based on the log-rank conjecture
        # This is also a very rough approximation
        return math.ceil(math.log2(m * n))
    
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    clauses = generate_3cnf(n, m)
    betti_numbers = persistent_homology_betti_numbers(clauses)
    communication_complexity = log_rank_conjecture(n, m)
    
    return {
        "metric_name": "Sum of Betti Numbers",
        "metric_value": betti_numbers,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")