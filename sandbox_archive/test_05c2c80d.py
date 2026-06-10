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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        inputs = [(i >> j) & 1 for i in range(2**n) for j in range(n)]
        outputs = [f[i] for i in range(2**n)]
        ranks = []
        for k in range(1, n):
            rank = 0
            for x in inputs:
                if sum(x >> j & 1 for j in range(k)) % 2 == 0:
                    rank += 1
            ranks.append(rank)
        return max(ranks) - min(ranks)
    
    def minimal_p_adic_derivative_rank(f):
        n = int(math.log2(len(f)))
        A = [[f[i ^ (1 << j)] for i in range(2**n)] for j in range(n)]
        mdr = 0
        for k in range(1, n):
            B = []
            for i in range(2**n):
                row = [A[j][i] * (i >> j & 1) for j in range(k)]
                if row not in B:
                    B.append(row)
            mdr = max(mdr, len(B))
        return mdr
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    seeds = random.sample(range(1, 30), 30) if seed == 0 else [seed]
    results = []
    for s in seeds:
        f = generate_boolean_function(s)
        delta_f = communication_complexity_rank_variance(f)
        mdr_f = minimal_p_adic_derivative_rank(f)
        results.append((delta_f, mdr_f))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(f) for f, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    delta_f_values = [delta_f for delta_f, _ in results]
    mdr_f_values = [mdr_f for _, mdr_f in results]
    correlation = pearson_correlation(delta_f_values, mdr_f_values)
    
    conjecture_holds = all(mdr_f <= 1.2 * delta_f for delta_f, mdr_f in results) and correlation >= 0.8
    counterexample = "" if conjecture_holds else "mdr(f) > 1.2 * Δ(f)"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")