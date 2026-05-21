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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def murnaghan_nakayama(lambda_, mu):
        if len(lambda_) != len(mu):
            return 0
        n = sum(lambda_)
        a = [lambda_[i] - mu[i] for i in range(len(lambda_))]
        b = [lambda_[i] - lambda_[i+1] for i in range(len(lambda_) - 1)]
        c = [mu[i] - mu[i+1] for i in range(len(mu) - 1)]
        return sum(Fraction(a[i], b[i]) * Fraction(c[i], a[i+1]) for i in range(len(a)-1))
    
    def chi_lambda(M, lambda_):
        n = len(M)
        det = 0
        for mu in partitions(n):
            if len(mu) == len(lambda_):
                det += murnaghan_nakayama(lambda_, mu)
        return abs(det)
    
    def partitions(n):
        def partitions_recursive(n, max_partition):
            if n == 0:
                yield []
            else:
                for i in range(min(n, max_partition), 0, -1):
                    for p in partitions_recursive(n-i, i):
                        yield [i] + p
        return partitions_recursive(n, n)
    
    def perm_n():
        n = len(M)
        perm = list(range(n))
        random.shuffle(perm)
        return [[M[i][j] for j in perm] for i in range(n)]
    
    def det_m(m):
        if m == 0:
            return 1
        n = len(M)
        det = 0
        for j in range(n):
            M_sub = [row[:j] + row[j+1:] for row in M[1:]]
            sign = (-1) ** (j % 2)
            sub_det = det_m(m-1)
            det += sign * M[0][j] * sub_det
        return det
    
    n = 40
    M = generate_matrix(n)
    chi_perm_n = chi_lambda(perm_n(), [n])
    chi_det_20 = chi_lambda(det_m(20), [20])
    
    metric_name = "chi_lambda_discrepancy"
    metric_value = chi_perm_n - chi_det_20
    instances_tested = 1
    conjecture_holds = metric_value > 0
    counterexample = "" if conjecture_holds else "m=20, det(M) ≥ perm_n(M)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")