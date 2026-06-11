# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(n):
            if j != i:
                factor = Fraction(matrix[j][i], pivot)
                for k in range(n+1):
                    matrix[j][k] -= factor * matrix[i][k]

    return matrix

def row_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[i]):
            rank += 1
    return rank

def quandle_order(cnf):
    n = len(cnf[0])
    elements = set()
    for clause in cnf:
        for literal in clause:
            elements.add(literal)
    
    n_elements = len(elements)
    identity_matrix = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n_elements)] for i in range(n_elements)]
    
    for clause in cnf:
        row = [Fraction(0, 1)] * n_elements
        for literal in clause:
            if literal > 0:
                row[elements.index(literal)] += Fraction(1, 1)
            else:
                row[elements.index(-literal)] -= Fraction(1, 1)
        
        identity_matrix.append(row)
    
    augmented_matrix = identity_matrix + [[Fraction(0, 1)] * (n_elements + n) for _ in range(n)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    
    return row_rank(reduced_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = [[random.randint(-n, n) for _ in range(random.randint(2, 4))] for _ in range(n)]
            min_order = quandle_order(cnf)
            entanglement_width = len(max(set(abs(lit) for lit in clause for clause in cnf), key=abs))
            
            if min_order == 0 or entanglement_width == 0:
                continue
            
            results.append((min_order, entanglement_width))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "MinOrder vs EntanglementWidth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [r[0] for r in results]
    entanglement_widths = [r[1] for r in results]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_entanglement_width = sum(entanglement_widths) / len(entanglement_widths)
    
    # Simple linear correlation coefficient
    covariance = sum((min_orders[i] - mean_min_order) * (entanglement_widths[i] - mean_entanglement_width) for i in range(len(min_orders)))
    variance_min_order = sum((min_orders[i] - mean_min_order) ** 2 for i in range(len(min_orders)))
    variance_entanglement_width = sum((entanglement_widths[i] - mean_entanglement_width) ** 2 for i in range(len(entanglement_widths)))
    
    correlation_coefficient = covariance / (variance_min_order * variance_entanglement_width) ** 0.5
    
    return {
        "metric_name": "MinOrder vs EntanglementWidth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    min_orders = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean_min_order = sum(min_orders) / len(min_orders)
    std_min_order = (sum((x - mean_min_order) ** 2 for x in min_orders) / len(min_orders)) ** 0.5
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_min_order} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_min_order} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")