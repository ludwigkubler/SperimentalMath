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
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll_tree_width(cnf):
        if not cnf:
            return 0
        if any(len(clause) == 1 for clause in cnf):
            return 1
        for literal in cnf[0]:
            new_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
            width = dpll_tree_width(new_cnf)
            if width > 1:
                return width + 1
        return 2
    
    def tropicalized_k_group(cnf):
        rank = len(cnf)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = dpll_tree_width(cnf)
        rank = tropicalized_k_group(cnf)
        
        if width == 0 or rank == 0:
            continue
        
        ratio = rank / width
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_ratio = total_ratio / instances_tested
    std_ratio = math.sqrt(sum((ratio - mean_ratio) ** 2 for ratio in range(instances_tested)) / instances_tested)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_ratio <= 10 and std_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")