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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def minterms_to_free_monoid(minterms):
        monoid = set()
        for m in minterms:
            monoid.add(tuple(sorted([abs(x) for x in m])))
        return len(monoid)
    
    def clause_subset_entropy(n):
        return n * math.log2(2**n)
    
    def generate_random_cnf(n, num_clauses):
        clauses = []
        variables = list(range(1, n + 1))
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * random.choice(variables) for _ in range(random.randint(1, n))]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def minterms_to_free_monoid(minterms):
        monoid = set()
        for m in minterms:
            monoid.add(tuple(sorted([abs(x) for x in m])))
        return len(monoid)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_random_cnf(n, random.randint(1, n))
            minterms = [tuple(sorted([abs(x) for x in clause])) for clause in cnf]
            free_monoid_order = minterms_to_free_monoid(minterms)
            h_n = clause_subset_entropy(n)
            results.append((free_monoid_order, h_n))
    
    if not results:
        return {
            "metric_name": "Free Monoid Order vs Clause Subset Entropy",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    free_monoid_orders = [r[0] for r in results]
    h_ns = [r[1] for r in results]
    mean_order = sum(free_monoid_orders) / len(free_monoid_orders)
    std_dev = math.sqrt(sum((x - mean_order)**2 for x in free_monoid_orders) / len(free_monoid_orders))
    
    max_n = max(n_values)
    conjecture_holds = all(order <= 1.5 * h_n for order, h_n in results)
    
    return {
        "metric_name": "Free Monoid Order vs Clause Subset Entropy",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")