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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if 0 not in clause:
                clauses.append(clause)
        return clauses

    def is_satisfiable(clauses):
        variables = set(abs(x) for clause in clauses for x in clause)
        assignment = {var: random.choice([-1, 1]) for var in variables}
        for clause in clauses:
            if all(assignment[var] * x <= 0 for x in clause):
                return True
        return False

    def sos_moment_matrix(clauses):
        n = max(abs(x) for clause in clauses for x in clause)
        matrix = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        for assignment in itertools.product([-1, 1], repeat=n):
            count = sum(assignment[i] * x for i, x in enumerate(clauses))
            if count >= 0:
                matrix[count][len([x for x in assignment if x != 0])] += Fraction(1, 1)
        return matrix

    def schur_coefficients(matrix):
        n = len(matrix) - 1
        coefficients = [matrix[i][i] for i in range(n + 1)]
        return coefficients

    def dominates(coefficients):
        max_index = coefficients.index(max(coefficients))
        for i in range(max_index):
            if coefficients[i] > coefficients[max_index]:
                return False
        return True

    n = random.randint(5, 40)
    clauses = generate_3sat_instance(n)
    satisfiable = is_satisfiable(clauses)
    matrix = sos_moment_matrix(clauses)
    coefficients = schur_coefficients(matrix)

    if satisfiable:
        conjecture_holds = dominates(coefficients)
    else:
        conjecture_holds = not dominates(coefficients)

    return {
        "metric_name": "Schur Coefficient Dominance",
        "metric_value": max(coefficients) if coefficients else 0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "unsatisfiable instance"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"unsatisfiable instance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")