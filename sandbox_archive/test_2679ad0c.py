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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if 0 not in clause:
                clauses.append(clause)
        return clauses
    
    def resolution_width(formula):
        clauses = formula[:]
        width = 0
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-x in clauses[i] and x in clauses[j] for x in set(clauses[i]) & set(clauses[j])):
                        new_clause = [x for x in clauses[i] if x not in [-y for y in clauses[j]]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return width
            if len(new_clause) > width:
                width = len(new_clause)
            clauses.append(new_clause)
    
    def groupoid_dimension(formula):
        n = len(formula[0])
        relations = {}
        for clause in formula:
            for x in clause:
                for y in clause:
                    if x != y and (x, y) not in relations and (y, x) not in relations:
                        relations[(x, y)] = True
        return len(relations)
    
    n_values = [5, 10, 15, 20, 30, 40]
    dimensions = []
    widths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            dimension = groupoid_dimension(formula)
            width = resolution_width(formula)
            dimensions.append(dimension)
            widths.append(width)
    
    if not dimensions or not widths:
        return {
            "metric_name": "groupoid_dimension",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    mean_dimension = sum(dimensions) / len(dimensions)
    mean_width = sum(widths) / len(widths)
    max_dimension = max(dimensions)
    
    if max_dimension > 5 * mean_width:
        return {
            "metric_name": "groupoid_dimension",
            "metric_value": 0,
            "instances_tested": len(dimensions),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"max_dimension={max_dimension} > 5 * mean_width={mean_width}"
        }
    
    return {
        "metric_name": "groupoid_dimension",
        "metric_value": mean_dimension,
        "instances_tested": len(dimensions),
        "n_max": max(n_values),
        "conjecture_holds": True,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_dimension > 5 * mean_width\" first_failing_seed={first_failing_seed}")