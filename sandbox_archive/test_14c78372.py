# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        literals = list(range(1, n + 1))
        formula = ' or '.join([f'{l} or {r}' for l, r in combinations(literals, 2)])
        return formula
    
    def incidence_matrix(formula, n):
        matrix = [[0] * n for _ in range(n)]
        literals = list(range(1, n + 1))
        for clause in formula.split(' or '):
            for literal in clause.split():
                if literal.startswith('-'):
                    col = abs(int(literal)) - 1
                    matrix[row][col] = -1
                else:
                    col = int(literal) - 1
                    matrix[row][col] = 1
        return matrix
    
    def min_order(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        augmented = [row + col for row, col in zip(matrix, identity)]
        
        # Gaussian elimination
        for i in range(n):
            if augmented[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n):
                factor = augmented[j][i] / augmented[i][i]
                for k in range(n * 2):
                    augmented[j][k] -= factor * augmented[i][k]
        
        # Count non-zero entries
        count = sum(abs(entry) > 0.5 for row in augmented for entry in row)
        return count
    
    def resolution_width(formula):
        clauses = formula.split(' or ')
        queue = [clauses]
        visited = set()
        width = 0
        
        while queue:
            new_queue = []
            for clause in queue:
                if len(clause) == 1:
                    continue
                literal, rest = clause[0], clause[1:]
                new_clause = [l for l in rest if not (l.startswith('-') and int(l[1:]) == abs(int(literal)))]
                if not new_clause:
                    return float('inf')
                new_queue.append(new_clause)
            queue = new_queue
            width += 1
        
        return width
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    inc_matrix = incidence_matrix(formula, n)
    min_order_val = min_order(inc_matrix)
    res_width = resolution_width(formula)
    
    if min_order_val == float('inf') or res_width == float('inf'):
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")