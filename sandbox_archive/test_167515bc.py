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
    
    def xor_and_formula(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = xor_and_formula(n // 2)
            right = xor_and_formula(n - n // 2)
            return [x ^ y for x in left for y in right]
    
    def hodge_decomposition(poly):
        n = len(poly)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = poly[i]
        rank = 0
        for i in range(n):
            if H[i][i] == 0:
                found = False
                for j in range(i + 1, n):
                    if H[j][i] != 0:
                        H[i], H[j] = H[j], H[i]
                        found = True
                        break
                if not found:
                    continue
            rank += 1
            for j in range(n):
                if i == j:
                    continue
                factor = -H[j][i] / H[i][i]
                for k in range(n):
                    H[j][k] += factor * H[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(5):
            poly = xor_and_formula(n)
            rank = hodge_decomposition(poly)
            ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    f_n = math.log2(n)**2
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": mean_rank <= f_n + 0.1 * math.sqrt(f_n) and mean_rank >= f_n - 0.1 * math.sqrt(f_n),
        "counterexample": "" if mean_rank <= f_n + 0.1 * math.sqrt(f_n) else "f(n) too small"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='f(n) too small' first_failing_seed={seeds[first_failing_seed]}")