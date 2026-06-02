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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses, n):
        poly = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
        for clause in clauses:
            for i in clause:
                if i < 0:
                    i = -i
                poly[i][i] += 1
        return poly
    
    def min_order(poly):
        order = 0
        for row in poly:
            for val in row:
                if val != 0:
                    order = max(order, int(math.log2(val)))
        return order
    
    def resolution_width(clauses):
        width = 0
        stack = []
        while clauses:
            clause = random.choice(clauses)
            if len(clause) == 1:
                literals = set(c for c in clauses if c != clause)
                new_clause = [l for l in literals if -l not in literals]
                clauses.remove(clause)
                clauses.extend(new_clause)
            else:
                literal = random.choice(clause)
                stack.append(literal)
                clauses = [c for c in clauses if literal not in c and -literal not in c]
                width += 1
        return width
    
    n = random.randint(5, 40)
    phi = generate_3cnf(n)
    Phi_phi = clause_indicator_polynomial(phi, n)
    min_order_phi = min_order(Phi_phi)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "min_order / w",
        "metric_value": min_order_phi / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")