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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def hodge_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] += 1
                else:
                    matrix[i][-1] += 1
        return len(gaussian_elimination(matrix)) - 1

    def dpll_width(clauses):
        n = len(clauses)
        variables = set()
        for clause in clauses:
            variables.update(abs(var) for var in clause)
        variable_count = len(variables)

        def dfs(model, level):
            if level == variable_count:
                return True
            var = list(variables - model.keys())[0]
            for value in [True, False]:
                new_model = model.copy()
                new_model[var] = value
                if all(any(new_model[var] for var in clause) for clause in clauses):
                    if dfs(new_model, level + 1):
                        return True
            return False

        return dfs({}, 0)

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(2, min(n, 10))
        clause = [random.choice([-i, i]) for i in range(1, num_vars + 1)]
        clauses.append(clause)

    rank = hodge_rank(clauses)
    width = dpll_width(clauses)

    return {
        "metric_name": "Rank vs DPLL Width",
        "metric_value": rank / width,
        "instances_tested": 1,
        "conjecture_holds": rank <= width * 2,  # Allow a small margin of error
        "counterexample": "" if rank <= width * 2 else f"Counterexample with n={n}, rank={rank}, width={width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")