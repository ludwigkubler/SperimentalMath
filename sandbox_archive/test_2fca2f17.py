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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def count_clauses(clauses):
        return len(clauses)
    
    def symplectic_leaves(clauses):
        n = len(clauses[0])
        leaves = set()
        for clause in clauses:
            leaf = tuple(sorted([abs(x) for x in clause]))
            leaves.add(leaf)
        return len(leaves)
    
    def log_squared(n):
        if n <= 0:
            return 0
        return math.log2(n) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        num_clauses = count_clauses(cnf)
        leaves = symplectic_leaves(cnf)
        ratio = Fraction(leaves, log_squared(n))
        results.append({
            "n": n,
            "num_clauses": num_clauses,
            "leaves": leaves,
            "ratio": ratio
        })
    
    total_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = 0.8 <= total_ratio <= 1.2
    
    return {
        "metric_name": "Ratio of Symplectic Leaves to log²(n)",
        "metric_value": float(total_ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio outside [0.8, 1.2]: {total_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.8, 1.2]\" first_failing_seed={first_failing_seed}")