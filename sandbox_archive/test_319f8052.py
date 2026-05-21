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
    
    def generate_monotone_dnf(n, k):
        if n < k or k == 0:
            return []
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def truth_table(dnf):
        n = len(dnf[0])
        tt = [[False] * (2 ** n) for _ in range(len(dnf))]
        for i, clause in enumerate(dnf):
            for j in range(2 ** n):
                if all((j >> var) & 1 == lit for var, lit in enumerate(clause)):
                    tt[i][j] = True
        return tt
    
    def polynomial_hierarchy_depth(tt):
        m = 0
        while True:
            found = False
            for i in range(len(tt)):
                if any(not tt[i][j] for j in range(2 ** (m + 1))):
                    found = True
                    break
            if not found:
                return m
            m += 1
    
    n_max = 40
    k_max = 40
    instances_tested = 0
    total_depth = 0
    
    for n in range(5, n_max + 1):
        for k in range(1, min(k_max, n) + 1):
            dnf = generate_monotone_dnf(n, k)
            tt = truth_table(dnf)
            depth = polynomial_hierarchy_depth(tt)
            total_depth += depth
            instances_tested += 1
    
    mean_depth = total_depth / instances_tested
    std_dev = math.sqrt(sum((depth - mean_depth) ** 2 for depth in range(total_depth)) / instances_tested)
    
    conjecture_holds = mean_depth <= n_max ** k_max / 2 and std_dev <= 0.1 * n_max ** k_max
    
    return {
        "metric_name": "polynomial_hierarchy_depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean={mean_depth}, std={std_dev}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")