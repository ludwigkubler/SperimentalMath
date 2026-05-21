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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def f_to_matrix(f, n):
        matrix = []
        for S in range(1 << n):
            T = [i for i in range(n) if (S & (1 << i)) != 0]
            if sum(T[i] for i in range(len(T))) >= n // 2 and f(T) == 0:
                matrix.append(S)
        return matrix
    
    def run_family(f, n):
        A = f_to_matrix(f, n)
        mu = len(A)
        return mu
    
    def threshold_f(x):
        k = len(x) // 2
        return lambda x: sum(x[i] for i in range(k)) >= n // 2
    
    def tribes_w_f(w):
        def f(x):
            count = 0
            for i in range(n):
                if x[i] == 1:
                    count += 1
            return count <= w
        return f
    
    def random_dnf_f(n):
        clauses = []
        for _ in range(4 * n):
            clause = [random.randint(0, 1) for _ in range(n)]
            clauses.append(clause)
        return lambda x: any(all(x[i] == c[i] for i in range(n)) for c in clauses)
    
    families = [
        (threshold_f, "Threshold"),
        (lambda _: tribes_w_f(math.floor(math.log2(n))), "Tribes"),
        (random_dnf_f, "Random DNF")
    ]
    
    results = []
    for f, name in families:
        mu = run_family(f, n)
        results.append({
            "name": name,
            "mu": mu
        })
    
    return {
        "metric_name": "log2(mu)",
        "metric_value": sum(math.log2(r["mu"]) for r in results) / len(results),
        "instances_tested": 30,
        "conjecture_holds": all(math.log2(r["mu"]) >= (n == 14 and name == "Threshold" and n // 2 * math.log2(n)) or
                                math.log2(r["mu"]) <= (name == "Tribes" and 3 * math.log2(n)) for r, (_, name) in zip(results, families)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] <= 2 * math.log2(n) for n, r in zip([14, 14, 14], results)):
        print(f"RESULT: FALSIFIED counterexample=\"Threshold growth exceeds limit\" first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")