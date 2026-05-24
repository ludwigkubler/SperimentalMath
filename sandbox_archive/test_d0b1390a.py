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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
            bp.append(random.choice([0, 1]))
        return bp
    
    def compute_tropical_curve(bp):
        n = len(bp) // 2
        curve = [bp[0]]
        for i in range(1, n):
            curve.append(curve[-1] ^ bp[i])
        return curve
    
    def rank(tropical_curve):
        m = len(tropical_curve)
        if m == 0:
            return 0
        A = [[tropical_curve[j] ^ tropical_curve[i] for j in range(m)] for i in range(m)]
        r = 0
        for i in range(m):
            if A[i][i]:
                r += 1
                for j in range(i + 1, m):
                    A[j][i] /= A[i][i]
                for k in range(i + 1, m):
                    for j in range(i, m):
                        A[k][j] -= A[k][i] * A[i][j]
        return r
    
    def is_ip2(bp):
        n = len(bp) // 2
        return all(bp[2*i] == bp[2*i+1] for i in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            bp = generate_read_twice_bp(n)
            curve = compute_tropical_curve(bp)
            rank_value = rank(curve)
            total_rank += rank_value
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    
    if is_ip2(bp):
        conjecture_holds = mean_rank >= n / 5
        counterexample = "" if conjecture_holds else "IP_2 does not meet the lower bound"
    else:
        c = 0.1  # Example constant, adjust as needed
        conjecture_holds = mean_rank <= c * math.log(n)
        counterexample = "" if conjecture_holds else f"Non-IP_2 BP does not meet the upper bound with c={c}"
    
    return {
        "metric_name": "Mean Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")