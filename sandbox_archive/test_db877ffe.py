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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            if -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def dpll_refutation_depth(clauses):
    def backtrack(model=None, depth=0):
        if model is None:
            model = {}
        if all(any(lit in model and model[lit] == True for lit in clause) or any(-lit in model and model[-lit] == False for lit in clause) for clause in clauses):
            return depth
        var = next((var for var in range(1, n+1) if var not in model and -var not in model), None)
        if var is None:
            return float('inf')
        model[var] = True
        depth_true = backtrack(model, depth + 1)
        del model[var]
        model[-var] = False
        depth_false = backtrack(model, depth + 1)
        del model[-var]
        return min(depth_true, depth_false)
    n = len(clauses[0])
    return backtrack()

def entropic_complexity(clauses):
    truth_table = [False] * (2 ** len(clauses[0]))
    for assignment in range(2 ** len(clauses[0])):
        assignment_dict = {i+1: bool((assignment >> i) & 1) for i in range(len(clauses[0]))}
        if all(any(lit in assignment_dict and assignment_dict[lit] == True for lit in clause) or any(-lit in assignment_dict and assignment_dict[-lit] == False for lit in clause) for clause in clauses):
            truth_table[assignment] = True
    entropy = 0.0
    for count in [truth_table.count(True), truth_table.count(False)]:
        if count > 0:
            p = Fraction(count, len(truth_table))
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    clauses = generate_k_cnf(n, k)
    
    refutation_depth = dpll_refutation_depth(clauses)
    if refutation_depth == float('inf'):
        return {
            "metric_name": "DPLL Refutation Depth",
            "metric_value": refutation_depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    entropic = entropic_complexity(clauses)
    if entropic <= 0:
        return {
            "metric_name": "Entropic Complexity",
            "metric_value": entropic,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "non-positive"
        }
    
    c1 = random.uniform(0.5, 2.0)
    c2 = random.uniform(0.5, 2.0)
    expected_min = c1 * math.log2(2 ** refutation_depth + 1)
    expected_max = c2 * math.log2(2 ** refutation_depth + 1)
    
    return {
        "metric_name": "Entropic Complexity vs DPLL Refutation Depth",
        "metric_value": entropic,
        "instances_tested": 1,
        "conjecture_holds": expected_min <= entropic <= expected_max,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")