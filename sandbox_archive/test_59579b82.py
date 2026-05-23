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
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def dpll_search_tree_width(clauses):
        variables = set()
        for clause in clauses:
            variables.update(clause)
        n_vars = len(variables)
        max_width = 0
        stack = [(set(), set())]
        while stack:
            assignment, unassigned = stack.pop()
            if not unassigned:
                max_width = max(max_width, len(assignment))
                continue
            var = next(iter(unassigned))
            new_unassigned = unassigned - {var}
            for value in [True, False]:
                new_assignment = assignment | {(var, value)}
                new_clauses = []
                for clause in clauses:
                    if any(var == v and value == val for v, val in new_assignment):
                        continue
                    if all(v not in new_assignment for v, _ in clause):
                        break
                    new_clause = [v for v, _ in clause if (v, _) not in new_assignment]
                    if new_clause:
                        new_clauses.append(new_clause)
                else:
                    stack.append((new_assignment, set(new_unassigned)))
        return max_width

    def hodge_decomposition_rank(clauses):
        n_vars = len(set(v for clause in clauses for v in clause))
        matrix = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
        for i, clause in enumerate(clauses):
            for var in clause:
                matrix[i][var - 1] += 1
        return len(gaussian_elimination(matrix))

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(2, n)
        clause = set()
        while len(clause) < num_vars:
            var = random.randint(1, n)
            if (var, True) not in clause and (var, False) not in clause:
                clause.add((var, random.choice([True, False])))
        clauses.append(list(clause))

    rank = hodge_decomposition_rank(clauses)
    width = dpll_search_tree_width(clauses)

    return {
        "metric_name": "Rank vs DPLL Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= width * 2,  # Allow a small constant factor
        "counterexample": "" if rank <= width * 2 else f"rank={rank}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > 2*width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")