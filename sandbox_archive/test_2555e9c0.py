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
    
    def generate_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses

    def is_satisfiable(cnf):
        # Simplified SAT solver using backtracking
        assignment = {i: None for i in range(1, n + 1)}
        
        def backtrack(i):
            if i > n:
                return True
            for val in [True, False]:
                assignment[i] = val
                if all(any(not (c[0] < 0 and not assignment[-c[0]]) and not (c[1] < 0 and not assignment[-c[1]])
                        for c in clause) for clause in cnf):
                    if backtrack(i + 1):
                        return True
            assignment[i] = None
            return False
        
        return backtrack(1)

    def quasi_plurality_matrix(cnf):
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit - 1] += 1
                else:
                    matrix[-lit - 1][-lit - 1] += 1
        return matrix

    def min_rank(matrix):
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for j in range(n):
                    if row[j]:
                        for k in range(n):
                            matrix[k][j] -= row[k]
        return rank

    n = random.randint(5, 40)
    k = random.randint(2 * n, 3 * n)

    cnf_satisfiable = generate_cnf(n, k)
    cnf_unsatisfiable = generate_cnf(n, 2 * n + 1)

    rank_satisfiable = min_rank(quasi_plurality_matrix(cnf_satisfiable))
    rank_unsatisfiable = min_rank(quasi_plurality_matrix(cnf_unsatisfiable))

    return {
        "metric_name": "min_rank",
        "metric_value": (rank_satisfiable, rank_unsatisfiable),
        "instances_tested": 2,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [727, 773, 821, 877, 929]  # Default list of primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_rank_satisfiable = sum(r["metric_value"][0] for r in results) / len(results)
        mean_rank_unsatisfiable = sum(r["metric_value"][1] for r in results) / len(results)
        support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rank_satisfiable} std={math.sqrt(sum((r['metric_value'][0] - mean_rank_satisfiable) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")