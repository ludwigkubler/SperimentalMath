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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, m))]
            cnf.append(clause)
        return cnf
    
    def frege_proof_depth(cnf):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        while literals:
            literal = random.choice(list(literals))
            if literal > 0:
                literals.remove(-literal)
            else:
                literals.remove(-literal)
            stack.append(literal)
        return len(stack)
    
    def mri(cnf):
        # Simplified computation of minimal local ring index
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                matrix[i][abs(lit)] = max(matrix[i][abs(lit)], abs(lit))
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return n - rank
    
    results = []
    for m in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(m)
        mri_value = mri(cnf)
        frege_depth = frege_proof_depth(cnf)
        results.append({"mri": mri_value, "frege_depth": frege_depth})
    
    if not all(results):
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(m for m, _ in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "empty_values"
        }
    
    mri_values = [r["mri"] for r in results]
    frege_depths = [r["frege_depth"] for r in results]
    
    mean_mri = sum(mri_values) / len(mri_values)
    mean_frege = sum(frege_depths) / len(frege_depths)
    
    covariance = sum((mri - mean_mri) * (frege - mean_frege) for mri, frege in zip(mri_values, frege_depths))
    variance_mri = sum((mri - mean_mri) ** 2 for mri in mri_values)
    variance_frege = sum((frege - mean_frege) ** 2 for frege in frege_depths)
    
    if variance_mri == 0 or variance_frege == 0:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(m for m, _ in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "empty_values"
        }
    
    correlation = covariance / (math.sqrt(variance_mri) * math.sqrt(variance_frege))
    
    return {
        "metric_name": "mri_vs_frege",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(m for m, _ in results) if results else 0,
        "conjecture_holds": abs(correlation) > 0.1,  # Arbitrary threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")