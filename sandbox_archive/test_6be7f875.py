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
            max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
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

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref = gaussian_elimination([row[:] for row in matrix])
        rank = 0
        for row in rref:
            if any(row[j] != 0 for j in range(cols)):
                rank += 1
        return rank

    def dpll(formula):
        variables = set()
        clauses = []
        for clause in formula.split(' '):
            if clause.startswith('-'):
                literals = [-int(clause[1:])]
            else:
                literals = [int(clause)]
            variables.update(literals)
            clauses.append(literals)

        def solve(assignment):
            unassigned = variables - set(assignment.keys())
            if not unassigned:
                return all(all(lit in assignment and (lit > 0) == assignment[lit] for lit in clause) for clause in clauses)
            var = next(iter(unassigned))
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                if solve(new_assignment):
                    return True
            return False

        return solve({})

    def mrd(formula):
        n = len(formula.split(' '))
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i, clause in enumerate(formula.split(' ')):
            if clause.startswith('-'):
                literals = [-int(clause[1:])]
            else:
                literals = [int(clause)]
            for lit in literals:
                matrix[i][abs(lit)] += 1
        return rank(matrix)

    def dpll_height(formula):
        n = len(formula.split(' '))
        stack = [(formula, {})]
        max_depth = 0
        while stack:
            formula, assignment = stack.pop()
            if solve(assignment):
                continue
            unassigned = variables - set(assignment.keys())
            if not unassigned:
                break
            var = next(iter(unassigned))
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                stack.append((formula, new_assignment))
            max_depth += 1
        return max_depth

    n = random.randint(5, 40)
    formula = ' '.join(str(random.randint(-n, n)) for _ in range(n * (n + 1) // 2))
    
    mrd_value = mrd(formula)
    dpll_height_value = dpll_height(formula)
    
    return {
        "metric_name": "mrd_dpll_ratio",
        "metric_value": mrd_value / dpll_height_value**2,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mrd_value - dpll_height_value**2) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mrd_dpll_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")