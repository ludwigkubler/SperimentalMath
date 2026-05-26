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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        min_bits = float('inf')
        for i in range(2**n):
            x = [int(b) for b in format(i, f'0{n}b')]
            y = [int(b) for b in format(i + 1, f'0{n}b')]
            if f[i] == 1 and f[i + 1] == 0:
                min_bits = min(min_bits, math.ceil(math.log2(sum(abs(a - b) for a, b in zip(x, y)))))
        return min_bits
    
    def tropical_motive_rank(f):
        n = int(math.log2(len(f)))
        T = [[0 if i != j else 1 if f[i] == 1 else float('inf') for j in range(2**n)] for i in range(2**n)]
        rank = 0
        for _ in range(2**n):
            min_val = float('inf')
            min_idx = -1
            for i in range(2**n):
                if T[i][i] == float('inf'):
                    continue
                for j in range(i + 1, 2**n):
                    if T[j][j] < min_val:
                        min_val = T[j][j]
                        min_idx = j
            if min_idx == -1:
                break
            rank += 1
            for i in range(2**n):
                T[i][min_idx] = float('inf')
                T[min_idx][i] = float('inf')
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_function(n)
        cc = communication_complexity(f)
        mr = tropical_motive_rank(f)
        results.append({
            "n": n,
            "cc": cc,
            "mr": mr
        })
    
    min_mr = min(result["mr"] for result in results)
    max_cc = max(result["cc"] for result in results)
    
    conjecture_holds = min_mr >= math.log2(max_cc)
    counterexample = "" if conjecture_holds else f"min_rank(M_f)={min_mr}, log_2 CC_R(f)={math.log2(max_cc)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_mr,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")