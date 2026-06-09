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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} ∨ ¬{var}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'¬{variables[i-1]} ∨ ¬{variables[j-1]}')
        return f'( {" ∧ ".join(clauses)} )'

    def hamiltonian_system(n):
        # Simplified Hamiltonian system for demonstration
        H = [[0]*n for _ in range(n)]
        for i in range(n):
            H[i][i] = 1
        return H

    def geometric_entropy(H):
        n = len(H)
        det_H = determinant(H, n)
        if det_H == 0:
            return float('inf')
        return -math.log(abs(det_H))

    def determinant(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1)**j) * matrix[0][j] * determinant(submatrix, n-1)
        return det

    def frege_proof_width(formula):
        # Simplified estimation of Frege proof width
        return len(formula.split())

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        H = hamiltonian_system(n)
        mge_value = geometric_entropy(H)
        w_value = frege_proof_width(formula)
        
        if mge_value == float('inf'):
            continue
        
        results.append({
            "n": n,
            "mge": mge_value,
            "w": w_value
        })
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mge_values = [res["mge"] for res in results]
    w_values = [res["w"] for res in results]
    
    mean_mge = sum(mge_values) / len(mge_values)
    std_mge = math.sqrt(sum((x - mean_mge)**2 for x in mge_values) / len(mge_values))
    mean_w = sum(w_values) / len(w_values)
    std_w = math.sqrt(sum((x - mean_w)**2 for x in w_values) / len(w_values))
    
    correlation_coefficient = sum((mge_values[i] - mean_mge) * (w_values[i] - mean_w) for i in range(len(mge_values))) / (len(mge_values) * std_mge * std_w)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.1,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")