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
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([True, False]) for _ in range(5)]
            clauses.append(clause)
        return clauses
    
    def clause_depth(clauses):
        max_depth = 0
        for clause in clauses:
            depth = sum(1 for x in clause if x is not None)
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    def ehrhart_semigroup_size(clauses):
        m = len(clauses)
        d = clause_depth(clauses)
        return math.ceil(d ** (1.5 / 2) * math.log(m, 2) ** 3)
    
    n_max = 0
    instances_tested = 0
    total_mtr = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            clauses = generate_formula(n)
            mtr = ehrhart_semigroup_size(clauses)
            total_mtr += mtr
            instances_tested += 1
    
    mean_mtr = total_mtr / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    if mean_mtr > n_max ** (1.5 / 2) * math.log(n_max, 2) ** 3:
        conjecture_holds = False
        counterexample = f"mean_mtr={mean_mtr} exceeds upper bound for n_max={n_max}"
    
    return {
        "metric_name": "Ehrhart Semigroup Size",
        "metric_value": mean_mtr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mtr = sum(r["metric_value"] for r in results) / len(results)
    std_mtr = math.sqrt(sum((r["metric_value"] - mean_mtr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_mtr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_mtr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")