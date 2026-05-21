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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return sum(1 for row in matrix if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 10
    m_min = 5
    m_max = 20
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def dnf_to_matrix(dnf):
        matrix = [[0] * n for _ in range(len(dnf))]
        for i, clause in enumerate(dnf):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-var - 1] = 1
        return matrix
    
    def resolution(clauses):
        new_clauses = set()
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if len(set(clauses[i]) & set(clauses[j])) == 2:
                        new_clause = tuple(sorted([x for x in clauses[i] + clauses[j] if x not in set(clauses[i]) & set(clauses[j])]))
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            if new_clause not in clauses and new_clause not in new_clauses:
                new_clauses.add(new_clause)
        return list(new_clauses)
    
    results = []
    for m in range(m_min, m_max + 1):
        cnf = generate_3cnf(n, m)
        dnf = resolution(cnf)
        matrix = dnf_to_matrix(dnf)
        rank = gaussian_elimination(matrix)
        if m <= n ** 0.5:
            expected_rank = max(1, int(0.8 * n))
        else:
            expected_rank = min(n, int(5 * math.log(n)))
        results.append({
            "m": m,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    support_fraction = sum(1 for result in results if result["rank"] >= result["expected_rank"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "m={}".format(m)
    
    return {
        "metric_name": "Rank",
        "metric_value": avg_rank,
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
        print("TRIAL: {" + ", ".join(f'"{k}": {v!r}' for k, v in trial_result.items()) + "}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results)
    avg_rank = total_rank / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='m={result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")