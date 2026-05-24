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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def hodge_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def clause_indicator_polynomial(clauses, n):
        poly = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for clause in clauses:
                mask = 0
                for var in clause:
                    if var < 0:
                        mask |= 1 << (-var - 1)
                    else:
                        mask |= 1 << (var - 1)
                poly[i][mask] += 1
        return poly
    
    def sat_instance(n, max_clause_length):
        clauses = []
        for _ in range(random.randint(1, n * max_clause_length)):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, max_clause_length))]
            if all(var != 0 for var in clause):
                clauses.append(clause)
        return clauses
    
    def dpll_proof_complexity(clauses):
        # Placeholder function to simulate proof complexity
        return len(clauses) * 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    max_clause_length = 40
    clauses = sat_instance(n, max_clause_length)
    poly = clause_indicator_polynomial(clauses, n)
    rank = hodge_rank(poly)
    
    c = 2  # Example constant for the bound
    threshold = c * math.log(n)
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= threshold,
        "counterexample": "" if rank <= threshold else f"Hodge rank {rank} exceeds threshold {threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")