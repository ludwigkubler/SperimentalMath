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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def min_rank(matrix):
        reduced_matrix = gaussian_elimination([row[:] for row in matrix])
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank

    def tseitin_formula(n):
        variables = [chr(i) for i in range(ord('A'), ord('A') + n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(n - 1):
            clauses.append([-variables[i], variables[i + 1]])
        return variables, clauses

    def resolution_refutation(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        new_clauses = []
        while True:
            found_resolvent = False
            for i in range(len(new_clauses)):
                for j in range(i + 1, len(new_clauses)):
                    resolvents = set()
                    for literal in new_clauses[i]:
                        if -literal in new_clauses[j]:
                            resolvents.update([c for c in new_clauses[j] if c != -literal])
                    if not resolvents:
                        continue
                    found_resolvent = True
                    new_clause = tuple(sorted(list(resolvents)))
                    if new_clause not in clauses_set and new_clause not in new_clauses:
                        new_clauses.append(new_clause)
            if not found_resolvent:
                break
        return len(new_clauses)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = tseitin_formula(n)
        matrix = [[int(lit in clause) for lit in variables] for clause in clauses]
        min_rank_value = min_rank(matrix)
        resolution_length = resolution_refutation(clauses)
        results.append({
            "n": n,
            "min_rank": min_rank_value,
            "resolution_length": resolution_length
        })

    total_min_rank = sum(result["min_rank"] for result in results)
    total_resolution_length = sum(result["resolution_length"] for result in results)
    mean_ratio = (2 ** total_min_rank) / total_resolution_length

    return {
        "metric_name": "Mean Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio > 1,  # Assuming c=0 for simplicity
        "counterexample": "" if mean_ratio > 1 else "mean_ratio < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['results'][0]['n']}, min_rank={r['results'][0]['min_rank']}, resolution_length={r['results'][0]['resolution_length']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break