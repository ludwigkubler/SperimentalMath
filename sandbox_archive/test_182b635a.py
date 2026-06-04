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
    
    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def entropy(clauses):
        total = len(clauses)
        counts = {}
        for clause in clauses:
            key = tuple(sorted(abs(x) for x in clause))
            if key not in counts:
                counts[key] = 0
            counts[key] += 1
        return -sum(count / total * math.log2(count / total) for count in counts.values())
    
    def self_dual_codes(clauses):
        n = len(clauses[0])
        codes = []
        for i in range(1 << n):
            code = [(-1 if (i & (1 << j)) else 1) * (j + 1) for j in range(n)]
            if all(all(code[i] == -code[j] for i in range(n) for j in range(i + 1, n))):
                codes.append(code)
        return codes
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    N = []
    H = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            m = int(2 ** entropy(generate_sat_instance(n, 1)))
            clauses = generate_sat_instance(n, m)
            codes = self_dual_codes(clauses)
            N.append(len(codes))
            H.append(entropy(clauses))
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_N = sum(N) / len(N)
    std_N = math.sqrt(sum((x - mean_N) ** 2 for x in N) / len(N))
    corr = correlation(N, H)
    
    conjecture_holds = corr >= 0.8 and all(abs(n - mean_N) <= 3 * std_N for n in N)
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"
    
    return {
        "metric_name": "Correlation",
        "metric_value": corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")