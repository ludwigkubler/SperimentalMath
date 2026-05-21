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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = Fraction(1, matrix[i][i])
        for j in range(i+1, n):
            matrix[j][i] *= factor
        
        # Eliminate above
        for j in range(i):
            factor = matrix[j][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def hodge_index(kernel_matrix):
    n = len(kernel_matrix)
    if n == 0:
        return 0
    kernel_matrix = gaussian_elimination(kernel_matrix)
    rank = sum(1 for row in kernel_matrix if any(x != 0 for x in row))
    return rank

def circuit_complexity(formula, seed):
    random.seed(seed)
    complexity = 0
    for _ in range(100):  # Sample 100 instances
        assignment = [random.choice([0, 1]) for _ in range(len(formula))]
        if all(eval(clause, {}, dict(zip('x' + ''.join(str(i) for i in range(len(formula))), assignment))) for clause in formula):
            complexity += 1
    return Fraction(complexity, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = [random.choice(['x' + str(i), 'not x' + str(i)]) for i in range(n)]
    kernel_matrix = [[int(eval(clause1, {}, {'x' + str(i): assignment[i] for i in range(n)})) * int(eval(clause2, {}, {'x' + str(i): assignment[i] for i in range(n)})) for clause2 in formula] for clause1 in formula]
    h_index = hodge_index(kernel_matrix)
    avg_complexity = circuit_complexity(formula, seed)
    
    return {
        "metric_name": "Hodge Index and Circuit Complexity",
        "metric_value": h_index,
        "instances_tested": 100,
        "conjecture_holds": h_index <= n**3 and avg_complexity >= 2**(1/3) * n**(3/3),
        "counterexample": "" if h_index <= n**3 and avg_complexity >= 2**(1/3) * n**(3/3) else f"Formula: {formula}, Hodge Index: {h_index}, Avg Circuit Complexity: {avg_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")