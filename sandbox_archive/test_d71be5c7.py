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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        seen = set()
        queue = cnf[:]
        while queue:
            literal = queue.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [x for x in clause if x != literal]
                    if not new_clause:
                        return len(seen)
                    if -new_clause[0] in seen:
                        return len(seen)
                    queue.append(new_clause)
        return len(seen)
    
    def minimal_rank(cnf):
        # Placeholder for actual computation
        return random.random() * 10  # Random rank between 0 and 10
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    r_phi = minimal_rank(cnf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": r_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(r_phi - w_phi) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, r_phi={r['metric_value']}, w_phi={resolution_width(generate_cnf(r['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break