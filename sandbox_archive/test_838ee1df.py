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
    
    n = 40
    M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def murnaghan_nakayama(lam, mu):
        if len(lam) != len(mu):
            return 0
        sign = 1
        for i in range(len(lam)):
            if lam[i] < mu[i]:
                sign *= -1
        return sign
    
    def chi_lambda(M, lam):
        n = len(M)
        det = [1]
        for i in range(n):
            det.append(det[-1] * (i + 1))
        det_inv = [1 / d for d in det]
        
        result = 0
        for mu in partitions(n):
            if len(mu) != len(lam):
                continue
            term = murnaghan_nakayama(lam, mu)
            for i in range(len(mu)):
                term *= math.factorial(mu[i])
                term //= math.prod(math.factorial(mu[j]) for j in range(i + 1))
            result += abs(term * det_inv[len(det) - len(mu)])
        return result
    
    def partitions(n):
        if n == 0:
            yield []
            return
        for p in partitions(n - 1):
            yield [p[0] + 1] + p[1:]
            if not p or p[0] != p[1]:
                yield [1] + p
    
    chi_perm_n = chi_lambda(M, [n])
    chi_det_20 = chi_lambda(M, [20])
    
    return {
        "metric_name": "chi_lambda",
        "metric_value": chi_perm_n,
        "instances_tested": 1,
        "conjecture_holds": chi_det_20 < chi_perm_n,
        "counterexample": "" if chi_det_20 < chi_perm_n else "det(20) >= perm(n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"det(20) >= perm(n)\" first_failing_seed={first_failing_seed}")