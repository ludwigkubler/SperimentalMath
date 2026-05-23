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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(clause)
        return clauses

    def quadratic_form(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                for j in range(i, n):
                    Q[i][j] += clause[i] * clause[j]
                    if i != j:
                        Q[j][i] = Q[i][j]
        return Q

    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            rank += 1
            for j in range(i + 1, n):
                matrix[j][i] /= pivot
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank

    def communication_complexity(rank):
        return rank ** 2

    n = random.randint(5, 40)
    k = random.randint(1, 3)
    cnf = generate_k_cnf(n, k)
    Q = quadratic_form(cnf)
    rank = min_rank(Q)
    comm_complexity = communication_complexity(rank)

    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity <= n ** k and rank == n ** k,
        "counterexample": f"rank={rank}, expected=k={k}" if not (comm_complexity <= n ** k and rank == n ** k) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")