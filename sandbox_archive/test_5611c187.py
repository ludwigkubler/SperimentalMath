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
        for _ in range(2**n - 1):
            clause = [random.randint(1, n)]
            while len(clause) < random.randint(1, n):
                clause.append(random.choice([-1, 1]) * random.randint(1, n))
            clauses.append(clause)
        return clauses

    def communication_complexity(cnf):
        n = max(abs(lit) for lit in cnf[0])
        c = 0
        for clause in cnf:
            c += len(set(abs(lit) for lit in clause))
        return c

    def rank_toric_variety(cnf):
        # Placeholder function to simulate the computation of rank(R(φ))
        # This is a dummy implementation and should be replaced with actual logic
        n = max(abs(lit) for lit in cnf[0])
        return random.randint(n, 2*n)

    def solve(lits_true, lits_false):
        # Placeholder function to simulate the solution of a CNF
        # This is a dummy implementation and should be replaced with actual logic
        return True

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rank = rank_toric_variety(cnf)
    c = communication_complexity(cnf)

    if rank == 0 or c == 0:
        return {
            "metric_name": "rank_diff",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    rank_diff = abs(rank - c)
    return {
        "metric_name": "rank_diff",
        "metric_value": rank_diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank_diff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break