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
        cnf = []
        for _ in range(10):  # Generate 10 clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        literals = set()
        for clause in cnf:
            literals.update(clause)
        literal = random.choice(list(literals))
        positive = literal > 0
        
        new_cnf = []
        for clause in cnf:
            if positive and literal in clause:
                continue
            elif not positive and -literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != literal and l != -literal]
                if new_clause:
                    new_cnf.append(new_clause)
        return dpll(new_cnf, assignment + [(literal, True)]) or dpll(new_cnf, assignment + [(literal, False)])
    
    def algebraic_integers(cnf):
        integers = set()
        for clause in cnf:
            for literal in clause:
                if literal != 0:
                    integers.add(abs(literal))
        return integers
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        integers = algebraic_integers(cnf)
        min_abs_value = min(integers) if integers else 1
        width = dpll(cnf, [])
        
        results.append({
            "n": n,
            "min_abs_value": min_abs_value,
            "width": width
        })
    
    metric_value = sum(result["width"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["width"] <= 10 * result["n"] * math.log(result["min_abs_value"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")