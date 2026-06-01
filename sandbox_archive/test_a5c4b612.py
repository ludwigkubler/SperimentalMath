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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, 2*m) for _ in range(random.randint(1, m))]
            cnf.append(clause)
        return cnf
    
    def frege_proof_depth(cnf):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        literals = set()
        for clause in cnf:
            if not any(lit in literals for lit in clause):
                literals.add(random.choice(clause))
                stack.append(clause)
        return len(stack)
    
    def tropical_variety(cnf):
        # Simplified computation of tropical variety index
        n = len(cnf)
        m = len(cnf[0])
        matrix = [[Fraction(1, 1) if i == j else Fraction(-1, 1) for j in range(n)] for i in range(n)]
        vector = [Fraction(-1, 1) * sum([Fraction(1, 1) if lit in clause else Fraction(-1, 1) for lit in clause]) for clause in cnf]
        
        # Gaussian elimination
        for i in range(n):
            if matrix[i][i] == 0:
                continue
            pivot = matrix[i][i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
                vector[j] -= factor * vector[i]
        
        # Count non-zero entries in the solution
        return sum(1 for v in vector if v != 0)
    
    mri_values = []
    frege_depths = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            mri_values.append(tropical_variety(cnf))
            frege_depths.append(frege_proof_depth(cnf))
            instances_tested += 1
    
    if not mri_values or not frege_depths:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, len(mri_values)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(mri_values)
    mean_mri = sum(mri_values) / n
    mean_depth = sum(frege_depths) / n
    
    covariance = sum((mri_values[i] - mean_mri) * (frege_depths[i] - mean_depth) for i in range(n)) / n
    variance_mri = sum((mri_values[i] - mean_mri) ** 2 for i in range(n)) / n
    variance_depth = sum((frege_depths[i] - mean_depth) ** 2 for i in range(n)) / n
    
    if variance_mri == 0 or variance_depth == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, len(mri_values)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_mri) * math.sqrt(variance_depth))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": max(5, len(mri_values)),
        "conjecture_holds": abs(pearson_corr) > 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")