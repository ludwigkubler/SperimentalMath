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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for _ in range(m):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause = f'~{clause}'
            clauses.append(clause)
        return variables, clauses
    
    def quasi_monogenic_sequence(variables, clauses):
        n = len(variables)
        m = len(clauses)
        Q = [[0] * (n + 1) for _ in range(m + 1)]
        Q[0][0] = 1
        for i in range(1, m + 1):
            clause = clauses[i-1]
            if '~' in clause:
                j = int(clause[2:]) - 1
                Q[i][j+1] = 1
            else:
                j = int(clause) - 1
                Q[i][j+1] = 1
        return Q
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, m)):
                rank += 1
                for j in range(m):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                matrix[pivot_row], matrix[rank-1] = matrix[rank-1], matrix[pivot_row]
                for j in range(m):
                    if j != rank-1 and matrix[j][i] != 0:
                        factor = matrix[j][i] / matrix[rank-1][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank-1][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_max = n // 2
        for _ in range(5):  # Ensure at least 5 instances per size
            variables, clauses = generate_tseitin_formula(n, m_max)
            Q = quasi_monogenic_sequence(variables, clauses)
            rank = matrix_rank(Q)
            results.append({
                "n": n,
                "m": len(clauses),
                "rank": rank
            })
    
    if not results:
        return {
            "metric_name": "rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(result["rank"] for result in results)
    instances_tested = len(results)
    mean_rank = total_rank / instances_tested
    
    C = 1.0  # Empirical constant
    expected_rank = C * math.log2(n + m_max)
    
    conjecture_holds = all(result["rank"] >= expected_rank for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if "metric_value" in r)
    instances_tested = sum(r["instances_tested"] for r in results if "instances_tested" in r)
    mean_rank = total_rank / instances_tested
    
    support_fraction = sum(1 for r in results if r.get("conjecture_holds", False)) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")