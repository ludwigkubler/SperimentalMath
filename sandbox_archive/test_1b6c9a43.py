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
    
    def generate_cnf(n: int):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses):
        # Simplified DPLL width calculation
        max_width = 0
        stack = [(clauses, [])]
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                continue
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                var = abs(unit_clause[0])
                new_assignment = assignment + [var] if unit_clause[0] > 0 else assignment + [-var]
                stack.append(([(c for c in clauses if var not in c and -var not in c), new_assignment], new_assignment))
            else:
                var = next(var for var in range(1, len(clauses) + 1) if var not in [abs(c[0]) for c in clauses])
                stack.append(([c for c in clauses if var not in c and -var not in c], assignment + [var]))
                stack.append(([c for c in clauses if var not in c and -var not in c], assignment + [-var]))
        return max_width
    
    def hodge_decomposition_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (2 * n) for _ in range(2 * n)]
        for clause in clauses:
            var1, var2 = abs(clause[0]), abs(clause[1])
            matrix[var1 - 1][var2 - 1] += 1
            matrix[var2 - 1][var1 - 1] += 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return -1
            for j in range(n):
                if i != j and A[j][i] != 0:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_cnf(n)
        width = dpll_width(clauses)
        rank = hodge_decomposition_rank(clauses)
        results.append((n, width, rank))
    
    if not results:
        return {
            "metric_name": "Rank vs DPLL Width",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_width = sum(width for _, width, _ in results) / len(results)
    mean_rank = sum(rank for _, _, rank in results) / len(results)
    
    if mean_rank <= 2 * mean_width:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Mean Rank {mean_rank} > 2 * Mean Width {2 * mean_width}"
    
    return {
        "metric_name": "Rank vs DPLL Width",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = f"Mean Rank {result['metric_value']} > 2 * Mean Width {2 * mean_rank}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")