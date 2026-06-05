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
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(1, n)] if random.choice([True, False]) else [-random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def geometric_entropy(cnf, n):
        max_level = 0
        for clause in cnf:
            level = max(abs(lit) for lit in clause)
            if level > max_level:
                max_level = level
        boxes = [[False] * (max_level + 1) for _ in range(max_level + 1)]
        for clause in cnf:
            for lit in clause:
                index = abs(lit)
                boxes[index][index] = True
        count = sum(sum(row) for row in boxes)
        total_boxes = len(boxes) ** 2
        entropy = -count / total_boxes * math.log(count / total_boxes, 2) if count > 0 else 0
        return entropy
    
    def dpll_width(cnf):
        def dpll(clause_set, assignment):
            if not clause_set:
                return 1
            if not any(lit in assignment for lit in clause_set[0]):
                return 0
            new_assignment = {**assignment}
            new_assignment[list(clause_set[0])[0]] = True
            width_true = dpll([c for c in clause_set if all(lit not in c or (lit in assignment and assignment[lit])) for lit in new_assignment], new_assignment)
            if width_true > 0:
                return width_true
            new_assignment[list(clause_set[0])[0]] = False
            width_false = dpll([c for c in clause_set if all(lit not in c or (lit in assignment and not assignment[lit])) for lit in new_assignment], new_assignment)
            return width_false
        
        return dpll(cnf, {})
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropy_sum = 0
    width_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random CNF formulas
            cnf = generate_cnf(n)
            entropy = geometric_entropy(cnf, n)
            width = dpll_width(cnf)
            entropy_sum += entropy
            width_sum += width
            instances_tested += 1
    
    mean_entropy = entropy_sum / instances_tested
    mean_width = width_sum / instances_tested
    
    correlation_coefficient = (instances_tested * entropy_sum * width_sum - entropy_sum**2 - width_sum**2) / \
                              math.sqrt((instances_tested * entropy_sum**2 - entropy_sum**4) * (instances_tested * width_sum**2 - width_sum**4))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.2f} < 0.8"
    
    return {
        "metric_name": "Geometric Entropy vs DPLL Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")