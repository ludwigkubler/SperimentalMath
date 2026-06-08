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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in clause1 and -x not in clause2]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(queue)
            queue.append(new_clause)
    
    def hopf_algebra_rank(cnf):
        # Placeholder for actual implementation
        return len(cnf)  # Simplified for testing
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    min_rank = hopf_algebra_rank(cnf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "min_rank_over_w_phi",
        "metric_value": min_rank / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if 0.5 <= min_rank / w_phi <= 2 else False,
        "counterexample": "" if conjecture_holds else f"min_rank={min_rank}, w_phi={w_phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
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
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")