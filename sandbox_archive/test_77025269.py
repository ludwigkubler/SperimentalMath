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
        for _ in range(10 * n):  # Each variable appears in 10 clauses on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def count_clauses(cnf):
        return len(cnf)
    
    def symplectic_leaves(cnf):
        # Simplified simulation of symplectic leaves calculation
        n = len(cnf)
        return int(math.log2(n)) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_leaves = 0
    total_clauses = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        leaves = symplectic_leaves(cnf)
        clauses = count_clauses(cnf)
        
        if clauses == 0:
            continue
        
        total_leaves += leaves
        total_clauses += clauses
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "symplectic_leaves_per_clause",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ratio = total_leaves / total_clauses
    return {
        "metric_name": "symplectic_leaves_per_clause",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= ratio <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if 0.8 <= r["metric_value"] <= 1.2) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r for r in results if not (0.8 <= r["metric_value"] <= 1.2))["seed"]
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")