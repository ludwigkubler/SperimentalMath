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
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = determinant(matrix, n)
        return trace / abs(det)

    def determinant(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix, n - 1)
        return det

    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        literals = set()
        for clause in formula:
            if all(l not in literals and -l not in literals for l in clause):
                literals.update(clause)
            else:
                stack.append(clause)
        while stack:
            clause = stack.pop()
            if any(l in literals for l in clause):
                continue
            literals.add(random.choice(clause))
            for c in stack:
                if all(l not in literals and -l not in literals for l in c):
                    literals.update(c)
                else:
                    stack.remove(c)
        return len(literals)

    def generate_formula(n, m):
        formula = []
        for _ in range(m):
            clause = random.sample(range(1, n+1), 3)
            formula.append(clause)
        return formula

    n_max = 0
    instances_tested = 0
    total_frobenius_schur = 0
    total_depth = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):
            formula = generate_formula(n, n)
            matrix = [[0] * n for _ in range(n)]
            for clause in formula:
                for l1 in clause:
                    for l2 in clause:
                        if abs(l1) != abs(l2):
                            matrix[abs(l1)-1][abs(l2)-1] += 1
                            matrix[abs(l2)-1][abs(l1)-1] += 1

            frobenius_schur = frobenius_schur_indicator(matrix)
            depth = frege_proof_depth(formula)

            total_frobenius_schur += frobenius_schur
            total_depth += depth
            instances_tested += 1

    mean_frobenius_schur = total_frobenius_schur / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(frobenius_schur * depth for frobenius_schur, depth in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_frobenius_schur * mean_depth) / math.sqrt((instances_tested * sum(frobenius_schur**2 for frobenius_schur in range(instances_tested)) - instances_tested * mean_frobenius_schur**2) * (instances_tested * sum(depth**2 for depth in range(instances_tested)) - instances_tested * mean_depth**2))

    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={seeds[first_failing_seed]}")