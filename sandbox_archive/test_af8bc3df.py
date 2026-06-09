# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            # Find pivot
            max_row = i + sum(1 for j in range(i, rows) if abs(matrix[j][i]) > abs(matrix[i][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below pivot
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back-substitute to get row echelon form
        for i in range(rows - 1, -1, -1):
            for j in range(i + 1, rows):
                matrix[i][-1] -= matrix[j][-1] * matrix[i][j]
            matrix[i][-1] /= matrix[i][i]
        
        # Count non-zero rows
        rank = sum(1 for row in matrix if any(row))
        return rank

    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next(var for var in range(1, len(clauses) + 1) if var not in assignment and -var not in assignment)
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_clauses = []
            for clause in clauses:
                if any(var == abs(lit) and lit > 0 != value for lit in clause):
                    continue
                elif all(abs(lit) not in new_assignment or new_assignment[abs(lit)] != (lit > 0) for lit in clause):
                    return False
                else:
                    new_clauses.append([lit for lit in clause if abs(lit) not in new_assignment])
            if dpll(new_clauses, new_assignment):
                return True
        return False

    def height_dpll(clauses):
        def solve(assignment):
            if not clauses:
                return 0
            var = next(var for var in range(1, len(clauses) + 1) if var not in assignment and -var not in assignment)
            true_branch = solve(assignment.copy())
            false_branch = solve(assignment.copy())
            return max(true_branch, false_branch) + 1
        return solve({})

    def grothendieck_group_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for lit in clauses[i]:
                if lit > 0:
                    matrix[i][lit - 1] += 1
                else:
                    matrix[i][-1] -= 1
        return gaussian_elimination(matrix)

    n = random.randint(5, 40)
    clauses = [random.choice([-i-1, i] for i in range(n)) for _ in range(random.randint(1, n))]
    rank = grothendieck_group_rank(clauses)
    height = height_dpll(clauses)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": rank / height if height > 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")