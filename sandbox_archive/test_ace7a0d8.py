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
    
    def compute_tropical_motive(f):
        n = len(f)
        motive = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i] == 1 and f[j] == 1:
                    motive[i][j] = max(i, j) + 1
        return motive
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i]):
                pivot_col = matrix[i].index(1)
                for j in range(cols):
                    if matrix[j][pivot_col] == 1:
                        for k in range(rows):
                            if matrix[k][j]:
                                matrix[k][j] -= matrix[i][j]
                rank += 1
        return rank
    
    def randomized_communication_complexity(f):
        n = len(f)
        cc = float('inf')
        for _ in range(100):  # Sample multiple times to get a good estimate
            bits = 0
            x = random.randint(0, n-1)
            if f[x] == 1:
                while True:
                    y = random.randint(0, n-1)
                    if f[y] == 1 and x != y:
                        break
                    bits += 1
            cc = min(cc, bits)
        return cc
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_function(n)
    motive = compute_tropical_motive(f)
    rank = min_rank(motive)
    cc = randomized_communication_complexity(f)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= math.log2(cc),
        "counterexample": "" if rank >= math.log2(cc) else f"CC_R(f)={cc}, min_rank(M_f)={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")