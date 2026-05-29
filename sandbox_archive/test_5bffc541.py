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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        resolvents = []
        while True:
            new_resolvent = False
            for i in range(len(resolvents)):
                for j in range(i + 1, len(resolvents)):
                    if -resolvents[i][0] in resolvents[j]:
                        new_clause = tuple(sorted([c for c in resolvents[i] + resolvents[j] if c != -resolvents[i][0]]))
                        if new_clause not in clauses:
                            clauses.add(new_clause)
                            resolvents.append(new_clause)
                            new_resolvent = True
            if not new_resolvent:
                break
        return len(resolvents)
    
    def tropical_rank(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        rank = 0
        while n > 0:
            rank += sum(1 for clause in cnf if any(x == n or -x == n for x in clause))
            n -= 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        t_star = resolution_width(cnf)
        r_min = tropical_rank(cnf)
        results.append((r_min, t_star))
    
    mean_diff = sum(abs(r - t) for r, t in results) / len(results)
    ratio_mean = sum(r / t for r, t in results if t > 0) / sum(1 for _, t in results if t > 0)
    
    conjecture_holds = all(r / max(t, 1) >= 0.8 for r, t in results) and mean_diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")