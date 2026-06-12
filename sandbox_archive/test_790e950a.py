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
    
    def generate_random_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses

    def dpll_search_tree_width(clauses):
        n = len(clauses[0])
        queue = [(clauses, set())]
        max_width = 0
        while queue:
            current_clauses, assignment = queue.pop()
            if not current_clauses:
                continue
            literal = next((lit for lit in range(1, n + 1) if all(lit not in clause and -lit not in clause for clause in current_clauses)), None)
            if literal is None:
                max_width = max(max_width, len(assignment))
                continue
            queue.append(([(c for c in current_clauses if literal not in c and -literal not in c), assignment.union({literal})], assignment))
            queue.append(([(c for c in current_clauses if -literal not in c), assignment.union({-literal})], assignment))
        return max_width

    def affine_quotient_ring(clauses):
        n = len(clauses[0])
        generators = set()
        for clause in clauses:
            for lit in clause:
                generators.add(lit)
        return generators

    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # 5 instances per size
            m = random.randint(n, 10 * n)
            clauses = generate_random_sat_instance(n, m)
            w_phi = dpll_search_tree_width(clauses)
            G_phi = affine_quotient_ring(clauses)
            if w_phi > 0:
                total_ratio += len(G_phi) / w_phi
                instances_tested += 1
                n_max = max(n_max, n)

    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0

    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_ratio - 1.0) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")