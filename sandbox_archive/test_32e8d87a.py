# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, 5))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment[literal] = abs(literal) not in assignment or (assignment[abs(literal)] and literal > 0)
            return dpll([c for c in cnf if literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, max(abs(c) for c in sum(cnf, [])) + 1) if (all(l not in c or (assignment.get(abs(l), False) and l > 0) for c in cnf) and all(-l not in c or (not assignment.get(abs(l), False) and l < 0) for c in cnf))), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            return dpll(cnf, new_assignment)
        literal = random.choice([l for c in cnf for l in c])
        new_assignment[literal] = True
        if dpll(cnf, new_assignment):
            return True
        new_assignment[literal] = False
        return dpll(cnf, new_assignment)
    
    def tropical_cyclotomic_polynomial_size(cnf):
        n = len(cnf)
        degree = 0
        coefficients = set()
        for clause in cnf:
            for literal in clause:
                degree += abs(literal)
                coefficients.add(abs(literal))
        return degree, len(coefficients)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            continue
        
        degree, num_coefficients = tropical_cyclotomic_polynomial_size(cnf)
        metric_values.append(degree * math.log(n))
        
        n_max = max(n_max, n)
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Tropical Cyclotomic Polynomial Complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = pearson_correlation(metric_values, [n for n in [5, 10, 15, 20, 30, 40] * instances_tested])
    
    if correlation < 0.7:
        conjecture_holds = False
        counterexample = f"low_correlation={correlation}"
    
    return {
        "metric_name": "Tropical Cyclotomic Polynomial Complexity",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")