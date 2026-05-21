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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def resolve(cnf):
        n = len(cnf[0])
        dnf = []
        for clause in cnf:
            if not clause:
                return None  # Empty clause means unsatisfiable
            new_clause = [x for x in clause if x != -1]
            if not new_clause:
                continue
            dnf.append(new_clause)
        return dnf
    
    def fast_walsh_hadamard_transform(a):
        n = len(a)
        if n == 1:
            return a
        even = fast_walsh_hadamard_transform(a[::2])
        odd = fast_walsh_hadamard_transform(a[1::2])
        result = [0] * n
        for k in range(n // 2):
            result[k] = even[k] + odd[k]
            result[k + n // 2] = even[k] - odd[k]
        return result
    
    def fourier_coefficient(f, i):
        n = len(f)
        a = [0] * (1 << n)
        for j in range(1 << n):
            if f[j]:
                a[j ^ i] += 1
        return Fraction(a[0], 2 ** n) + Fraction(a[(1 << n) - 1], 2 ** n)
    
    def polymatroid_rank(f, S):
        return sum(abs(fourier_coefficient(f, i)) for i in S)
    
    n = 40
    k = 5
    
    cnf = []
    for _ in range(30):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        cnf.append(clause)
    
    dnf = resolve(cnf)
    if dnf is None:
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": 0,
            "instances_tested": 30,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable CNF"
        }
    
    S = set(range(n))
    rho_n = polymatroid_rank(dnf, S)
    rho_S = [polymatroid_rank(dnf, {i}) for i in range(1, min(101, n))]
    
    if rho_n < math.sqrt(n) * k ** (1/4):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rho_n,
            "instances_tested": 30,
            "conjecture_holds": False,
            "counterexample": f"rho([n]) = {rho_n} < {math.sqrt(n) * k ** (1/4)}"
        }
    
    if any(rho > 10 for rho in rho_S):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": max(rho_S),
            "instances_tested": 30,
            "conjecture_holds": False,
            "counterexample": f"rho(S) = {max(rho_S)} > 10"
        }
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rho_n,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support found")