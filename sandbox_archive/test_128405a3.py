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
    
    def generate_function(n):
        if n == 4:
            return random.choice([lambda x: all(x), lambda x: any(x), lambda x: x[0] and x[1], lambda x: not (x[0] or x[1])])
        elif n == 6:
            return random.choice([lambda x: all(x[:3]), lambda x: any(x[:3]), lambda x: x[0] and x[1], lambda x: not (x[0] or x[1])])
        elif n == 8:
            return random.choice([lambda x: all(x[:4]), lambda x: any(x[:4]), lambda x: x[0] and x[1], lambda x: not (x[0] or x[1])])
        elif n == 10:
            return random.choice([lambda x: all(x[:5]), lambda x: any(x[:5]), lambda x: x[0] and x[1], lambda x: not (x[0] or x[1])])
        else:
            return "mapping_undefined"
    
    def generate_conflict_family(f, n):
        L_f = set()
        for x in range(2**n):
            x_bits = [int(b) for b in format(x, f'0{n}b')]
            for y in range(2**n):
                y_bits = [int(b) for b in format(y, f'0{n}b')]
                if f(x_bits) != f(y_bits):
                    L_f.add(tuple(i for i in range(n) if x_bits[i] != y_bits[i]))
        return L_f
    
    def compute_dvc(L_f, n):
        dvc = 0
        for k in range(1, n + 1):
            T = list(itertools.combinations(range(n), k))
            covered = set()
            for t in T:
                projected_L_f = {tuple(x[i] for i in t) for x in L_f}
                if len(projected_L_f) == 2**k:
                    covered.update(t)
                    if len(covered) == n:
                        dvc = k
                        break
        return dvc
    
    def compute_depth(f, n):
        if n == 4:
            truth_tables = [f(x) for x in range(16)]
            dp = [[0] * (n + 1) for _ in range(n + 1)]
            for i in range(1, n + 1):
                for j in range(1 << i):
                    dp[i][j] = min(dp[i - 1][j & ~(1 << k)] + dp[i - 1][(j >> (k + 1)) & ((1 << k) - 1)] for k in range(i))
            return dp[n][(1 << n) - 1]
        else:
            return "mapping_undefined"
    
    n = random.choice([4, 6, 8, 10])
    f = generate_function(n)
    if f == "mapping_undefined":
        return {
            "metric_name": "dvc(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    L_f = generate_conflict_family(f, n)
    dvc = compute_dvc(L_f, n)
    depth = compute_depth(f, n)
    
    if depth is None:
        return {
            "metric_name": "dvc(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = depth >= math.ceil(math.log2(dvc + 1))
    counterexample = "" if conjecture_holds else f"Counterexample: d(f)={depth}, ceil(log2(dvc+1))={math.ceil(math.log2(dvc + 1))}"
    
    return {
        "metric_name": "dvc(f)",
        "metric_value": dvc,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")