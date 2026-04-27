# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def perm(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        sign = 1
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if matrix[j][i] < matrix[min_idx][i]:
                    min_idx = j
            if min_idx != i:
                matrix[i], matrix[min_idx] = matrix[min_idx], matrix[i]
                sign *= -1
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        det = sign * matrix[0][0]
        for i in range(1, n):
            det *= matrix[i][i]
        return abs(det)

    def Q_dt(f, memo={}):
        if f not in memo:
            k = len(f)
            if k == 1:
                memo[f] = 1
            else:
                memo[f] = max(Q_dt(f[:k-1], memo), Q_dt(f[1:], memo))
        return memo[f]

    def sensitive_boundary_matrix(f):
        n = 2 ** (len(f) - 1)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            x = bin(i)[2:].zfill(len(f) - 1)
            for j in range(n):
                y = bin(j)[2:].zfill(len(f) - 1)
                if sum(int(a) != int(b) for a, b in zip(x, y)) == 1 and f[x] != f[y]:
                    B[i][j] = 1
        return B

    k = 4
    n = 2 ** (k - 1)
    total_slack = 0
    num_violators = 0
    worst_case_slack = float('-inf')

    for i in range(2**k):
        f = {bin(i)[2:].zfill(k): random.choice([0, 1]) for i in range(2**(k-1))}
        B = sensitive_boundary_matrix(f)
        perm_B = perm(B)
        Q_dt_f = Q_dt(tuple(f.values()))
        slack = 4 * Q_dt_f - math.log2(perm_B + 1)
        total_slack += slack
        if slack < 0:
            num_violators += 1
            worst_case_slack = max(worst_case_slack, slack)

    mean_slack = total_slack / (2**k)
    support_fraction = 1.0 - num_violators / (2**k)

    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": 2**k,
        "conjecture_holds": support_fraction == 1.0 and worst_case_slack >= 0,
        "counterexample": "" if support_fraction == 1.0 else f"violator found with slack {worst_case_slack}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"violator found\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")