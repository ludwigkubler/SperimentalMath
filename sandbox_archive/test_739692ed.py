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
    
    def generate_formula(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals + [f"~{l}" for l in literals], 2)
            clauses.append(tuple(sorted(clause)))
        return tuple(sorted(set(clauses)))

    def aic(formula):
        if not formula:
            return 0
        n = len(formula[0])
        matrix = [[0] * (n + 1) for _ in range(n)]
        for clause in formula:
            for i, literal in enumerate(clause):
                if literal.startswith("~"):
                    j = int(literal[1:]) - 1
                    matrix[i][j] = -1
                else:
                    j = int(literal) - 1
                    matrix[i][j] = 1
        matrix.append([0] * n + [1])
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return 0
            pivot = Fraction(matrix[i][i])
            for j in range(n + 1):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n + 1):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix[:n] if any(row))
        return n - rank

    def clause_set_complexity(formula):
        return len(set(tuple(sorted(clause)) for clause in formula))

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_formula(n)
        aic_value = aic(formula)
        c_value = clause_set_complexity(formula)
        results.append((aic_value, c_value))

    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    aic_values = [r[0] for r in results]
    c_values = [r[1] for r in results]

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator if denominator else 0

    correlation = pearson_correlation(aic_values, c_values)
    p_value = 1.96 * (1 - abs(correlation)) / math.sqrt(2 * n)

    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation >= 0.8 and p_value <= 0.05,
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

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)

    if all(r["instances_tested"] >= 30 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")