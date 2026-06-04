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
        formula = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            formula.append(clause)
        return formula
    
    def count_integral_points(formula):
        n = len(formula[0])
        points = set()
        for x in range(2**n):
            valid = True
            for clause in formula:
                if all(x & (1 << abs(lit) - 1) == lit for lit in clause):
                    continue
                else:
                    valid = False
                    break
            if valid:
                points.add(tuple((x >> i) & 1 for i in range(n)))
        return len(points)
    
    def resolution_width(formula):
        n = len(formula[0])
        clauses = formula[:]
        while True:
            new_clauses = []
            added_clause = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(lit) == abs(lit2) and lit != lit2 for lit in clauses[i] for lit2 in clauses[j]):
                        new_lit = -clauses[i][0]
                        new_clause = [lit for lit in clauses[i] if lit != new_lit] + [lit for lit in clauses[j] if lit != -new_lit]
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            added_clause = True
            if not added_clause:
                break
            clauses.extend(new_clauses)
        return max(len(clause) for clause in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_points = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            points = count_integral_points(formula)
            width = resolution_width(formula)
            total_width += width
            total_points += points
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    mean_points = total_points / instances_tested
    conjecture_holds = mean_width <= 3 * mean_points
    counterexample = "" if conjecture_holds else f"mean_width={mean_width}, mean_points={mean_points}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_width > 3 * mean_points\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")