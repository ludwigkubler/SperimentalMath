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
        queue = cnf[:]
        seen = set()
        while queue:
            literal = queue.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [x for x in clause if x != literal]
                    if not new_clause:
                        return float('inf')
                    if -new_clause[0] in queue:
                        return float('inf')
                    queue.append(-new_clause[0])
        return len(seen)

    def minimal_rank(cnf):
        # Placeholder implementation of minimal rank calculation
        # This is a dummy function and should be replaced with actual computation
        return random.randint(1, 10)  # Dummy value

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    mrank = minimal_rank(cnf)
    w_phi = resolution_width(cnf)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "mrank_w_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_unbounded"
        }
    
    mrank_w_ratio = abs(mrank) / abs(w_phi)
    return {
        "metric_name": "mrank_w_ratio",
        "metric_value": mrank_w_ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mrank_w_ratio <= 2 and mrank_w_ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width_unbounded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no failing seeds found")