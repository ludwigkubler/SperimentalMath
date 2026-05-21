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
    
    def VC(R):
        B_size = len(R[0])
        for d in range(1, 2**B_size + 1):
            if all(any(all(R[j][i] == R[k][i] for i in range(B_size)) for j in S) for k in range(len(R)) for S in itertools.combinations(range(len(R)), d)):
                return d - 1
        return len(R)

    def log2_rank_GF2(M):
        n, m = len(M), len(M[0])
        rank = 0
        for i in range(n):
            if any(M[i][j] != 0 for j in range(m)):
                rank += 1
                for j in range(m):
                    M[i][j] /= M[i][j]
                for k in range(n):
                    if k != i and any(M[k][j] != 0 for j in range(m)):
                        for j in range(m):
                            M[k][j] -= M[i][j] * M[k][i]
        return rank

    def index_b(a, b):
        return a == b

    def inner_product_b(a, b):
        return sum(x * y for x, y in zip(a, b))

    def equality_gadget(a, b):
        return [int(i == j) for i, j in zip(a, b)]

    gadgets = {
        "index": index_b,
        "inner_product": inner_product_b,
        "equality": equality_gadget
    }

    results = []
    for n in {2, 3, 4}:
        for A_size in {4, 8}:
            for B_size in {2, 3, 4}:
                f = [random.choice([0, 1]) for _ in range(2**n)]
                g = random.choice(list(gadgets.values()))
                R_g = [[g(a, b) for b in range(B_size)] for a in range(A_size)]
                d = VC(R_g)
                
                M = [[f[int(''.join(map(str, g(a, b))), 2)] for b in range(B_size)] for _ in range(A_size**n)]
                rank = log2_rank_GF2(M)
                
                slack = rank - (0.5 * n * d - n)
                results.append({
                    "metric_name": "slack",
                    "metric_value": slack,
                    "instances_tested": 1,
                    "conjecture_holds": slack >= 0,
                    "counterexample": ""
                })

    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    return {
        "seed": seed,
        "mean_slack": mean_slack,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_slack = sum(result["mean_slack"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)

    if all(result["support_fraction"] >= 0.9 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slack < 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")