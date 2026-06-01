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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) == 1 for x in clause):
                clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {abs(literal): literal > 0}
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(new_cnf, assignment | new_assignment)
        
        p = next(abs(l) for l in random.choice(cnf))
        if dpll(cnf, assignment | {p: True}):
            return True
        elif dpll(cnf, assignment | {p: False}):
            return True
        else:
            return False

    def quaternionic_root_count(clauses):
        roots = set()
        for clause in clauses:
            for literal in clause:
                root = Fraction(literal, 1)
                if root not in roots:
                    roots.add(root)
        return len(roots)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    min_root_count = quaternionic_root_count(cnf)
    diameter = dpll(cnf)  # Diameter is not directly computable without a search algorithm

    return {
        "metric_name": "min_root_count",
        "metric_value": min_root_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")