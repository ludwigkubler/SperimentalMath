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
    
    def generate_cnf_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_quaternionic_matrix(cnf_formula):
        n = len(cnf_formula)
        Q = [[0] * (n + 2) for _ in range(n + 2)]
        for clause in cnf_formula:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0:
                Q[i][j + n + 1] = 1
            else:
                Q[j][i + n + 1] = 1
            Q[i][n] += 1
            Q[j][n] += 1
        return Q
    
    def determinant(matrix):
        n = len(matrix)
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def compute_min_order_K(cnf_formula):
        Q = construct_quaternionic_matrix(cnf_formula)
        det_Q = determinant(Q)
        min_order_K = abs(det_Q)
        return min_order_K
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        s = random.randint(5, 40)
        cnf_formula = generate_cnf_formula(s)
        min_order_K = compute_min_order_K(cnf_formula)
        
        if min_order_K > 2 * s**2:
            conjecture_holds = False
            counterexample = f"CNF size {s}, min_order(K) = {min_order_K}"
            break
        
        total_metric_value += min_order_K
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = (sum((x - mean_metric_value)**2 for x in [compute_min_order_K(generate_cnf_formula(random.randint(5, 40))) for _ in range(instances_tested)]) / instances_tested) ** 0.5
    
    return {
        "metric_name": "min_order(K)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")