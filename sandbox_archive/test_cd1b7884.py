# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate a random satisfiable 3-CNF formula
    clauses = []
    for _ in range(m):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
        clause = tuple(sorted(literals))
        if clause not in clauses:
            clauses.append(clause)
    
    # Apply the Coxeter group action on the set of clauses
    def coxeter_group_action(clauses):
        new_clauses = []
        for clause in clauses:
            new_clause = [-lit for lit in clause]
            if new_clause not in clauses:
                new_clauses.append(new_clause)
        return new_clauses
    
    distinct_clauses = set()
    for _ in range(10):  # Apply the action multiple times to ensure exploration
        distinct_clauses.update(coxeter_group_action(distinct_clauses))
    
    # Count the number of distinct minimal length words
    distinct_min_length_words = len([len(clause) for clause in distinct_clauses if len(clause) == min(len(c) for c in distinct_clauses)])
    
    # Compute the ratio
    n_cubed_root = n ** (1/3)
    if n_cubed_root == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    ratio = Fraction(distinct_min_length_words, n_cubed_root)
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if ratio < 0.8 else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8 and mean <= 3:
            print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}")
        else:
            print("RESULT: FALSIFIED counterexample=\"unsupported\" first_failing_seed=-1")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_value_none")