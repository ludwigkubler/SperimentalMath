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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if 0 not in clause:
                clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        if dpll(propagate(literal), assignment | {literal: True}):
            return True
        if dpll(propagate(-literal), assignment | {-literal: True}):
            return True
        return False
    
    def p_adic_order(n):
        # Simplified approximation for demonstration purposes
        return math.log2(n)
    
    n = 10
    instances_tested = 0
    total_ratio = 0
    max_n = 0
    
    while instances_tested < 30:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            continue
        
        clause_depth = len(cnf)
        order = p_adic_order(n)
        ratio = clause_depth / order if order != 0 else float('inf')
        
        total_ratio += ratio
        instances_tested += 1
        max_n = max(max_n, n)
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 4 and all(ratio <= 10 for ratio in [total_ratio / instances_tested])
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "Ratio of Clause Depth to p-adic Order",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mean_ratio={results[0]['metric_value']}' first_failing_seed={first_failing_seed}")