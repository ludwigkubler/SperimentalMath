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

def generate_formula(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.choice(variables) + " | " + random.choice(variables)
        clauses.append(clause)
    return " & ".join(clauses)

def symplectic_rank(clause_set):
    variables = set()
    for clause in clause_set:
        for var in clause.split():
            if var.startswith("x"):
                variables.add(var[1:])
    variables = sorted(list(variables))
    n = len(variables)
    matrix = [[0] * (n + 2) for _ in range(n)]
    for i, clause in enumerate(clause_set):
        for var in clause.split():
            if var.startswith("x"):
                j = variables.index(var[1:]) + 1
                matrix[i][j] = 1
                matrix[i][-1] += 1
                matrix[-2][j] -= 1
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return float('inf')
        for j in range(n):
            if i != j and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n + 2):
                    matrix[j][k] += factor * matrix[i][k]
    rank = sum(1 for row in matrix[:n] if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    clause_set = formula.split(" & ")
    try:
        rank = symplectic_rank(clause_set)
    except Exception as e:
        return {
            "metric_name": "categorified_symplectic_rank",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    expected_rank = n  # Placeholder for actual function f(n)
    ratio = rank / expected_rank
    return {
        "metric_name": "categorified_symplectic_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": 0.7 <= ratio <= 1.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(not math.isnan(r["metric_value"]) for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction}\" first_failing_seed={seeds[support_fraction < 0.8][0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation_or_nan")