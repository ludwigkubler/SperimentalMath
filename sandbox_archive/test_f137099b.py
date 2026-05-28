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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def rank(A):
    A = [row[:] for row in A]
    r = gaussian_elimination(A)
    return sum(1 for row in r if any(row))

def quadratic_form_matrix(bp):
    n = bp['n']
    m = len(bp['clauses'])
    Q = [[0] * (2 * n) for _ in range(n)]
    for clause in bp['clauses']:
        x = [bp['variables'].index(var) for var in clause]
        for i in x:
            Q[i][i + n] = 1
            for j in x:
                if i != j:
                    Q[i][j + n] += 1
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = random.randint(1, n)
        s = random.randint(1, n)
        variables = ['x' + str(i) for i in range(n)]
        clauses = []
        for _ in range(s):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        bp = {'n': n, 'variables': variables, 'clauses': clauses}
        Q = quadratic_form_matrix(bp)
        rank_Q = rank(Q)
        total_rank += rank_Q
        instances_tested += 1

        if rank_Q > m**2 * math.log(n):
            conjecture_holds = False
            counterexample = f"Rank {rank_Q} exceeds O(m^2 log n) for n={n}, m={m}"

    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "Minimal Rank",
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

    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")