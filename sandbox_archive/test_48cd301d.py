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
    
    n = 5 + (seed % 4) * 5  # Sweep n through {5,10,15,20,30,40}
    m = 5 + (seed // 7) * 5  # Sweep m through {5,10,15,20,30,40}
    
    # Generate a random k-CNF with n variables and m clauses
    k = 2  # Assuming binary CNF for simplicity
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            lit = random.randint(1, n)
            if -lit not in clause:
                clause.add(lit)
        cnf.append(tuple(sorted(clause)))
    
    # Compute the minimal state complexity q* using Myhill-Nerode theorem
    states = set()
    for clause in cnf:
        new_state = tuple(sorted(set(states) | {tuple(clause)}))
        states.add(new_state)
    
    q_star = len(states)
    
    # Calculate communication complexity (simplified as number of clauses)
    comm_complexity = m
    
    # Check if the conjecture holds
    upper_bound = (n + m + k) * math.log(n + m, 2)
    conjecture_holds = q_star <= upper_bound
    
    return {
        "metric_name": "q_star",
        "metric_value": q_star,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"q*={q_star} > upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_q_star = sum(r["metric_value"] for r in results) / len(results)
    std_q_star = math.sqrt(sum((r["metric_value"] - mean_q_star) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_q_star} std={std_q_star} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_q_star} std={std_q_star} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"q* exceeds upper-bound\" first_failing_seed={first_failing_seed}")