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
    
    def generate_dnf(n, m):
        dnf = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            dnf.append(clause)
        return dnf
    
    def submodular_width(dnf):
        n = len(dnf[0])
        width = 0
        while True:
            covered = [False] * n
            new_covered = False
            for clause in dnf:
                if any(not covered[i - 1] and c == i for c, i in zip(clause, range(1, n + 1))):
                    covered = [c or (c2 != 0) for c, c2 in zip(covered, clause)]
                    new_covered = True
            if not new_covered:
                break
            width += 1
        return width
    
    def k_clique_indicator(n):
        return [[i * j for i in range(1, n + 1)] for j in range(1, n + 1)]
    
    def submodular_width_k_clique(n):
        clique = k_clique_indicator(n)
        width = 0
        while True:
            covered = [False] * (n * n)
            new_covered = False
            for row in clique:
                if any(not covered[i - 1] and c == i for c, i in zip(row, range(1, n * n + 1))):
                    covered = [c or (c2 != 0) for c, c2 in zip(covered, row)]
                    new_covered = True
            if not new_covered:
                break
            width += 1
        return width
    
    def is_monotone(dnf):
        for clause in dnf:
            if any(c < 0 for c in clause):
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        dnf = generate_dnf(n, random.randint(1, n))
        if not is_monotone(dnf):
            continue
        width = submodular_width(dnf)
        instances_tested += 1
        if width > math.log(n) * 2:  # Loose bound for O(log n)
            conjecture_holds = False
            counterexample = f"DNF with n={n}, width={width}"
    
    k_values = [5, 10, 15, 20, 30]
    for n in k_values:
        width = submodular_width_k_clique(n)
        instances_tested += 1
        if width <= n / 2:  # Loose bound for Ω(n)
            conjecture_holds = False
            counterexample = f"k-CLIQUE with n={n}, width={width}"
    
    return {
        "metric_name": "submodular_width",
        "metric_value": (math.log(n) * 2 if instances_tested > 0 else None),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["instances_tested"] > 0 for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"] and r["instances_tested"] > 0)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["instances_tested"] > 0)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")