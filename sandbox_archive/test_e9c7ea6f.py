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

def xor_and_tree(n):
    if n == 1:
        return [0, 1]
    left = xor_and_tree(n // 2)
    right = xor_and_tree(n - n // 2)
    return [x ^ y for x in left] + [x & y for x in left] + [x ^ y for x in right] + [x & y for x in right]

def characteristic_polynomial(tree):
    if len(tree) == 1:
        return tree[0]
    else:
        poly = characteristic_polynomial(tree[:len(tree)//2])
        return [poly[i] ^ poly[j] for i in range(len(poly)) for j in range(i+1, len(poly))] + [poly[i] & poly[j] for i in range(len(poly)) for j in range(i+1, len(poly))]

def bruer_group_rank(tree):
    poly = characteristic_polynomial(tree)
    n = len(poly)
    rank = 0
    for i in range(n):
        if poly[i] != 0:
            rank += 1
            for j in range(i+1, n):
                if poly[j] % poly[i] == 0:
                    poly[j] = 0
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree = xor_and_tree(n)
        rank = bruer_group_rank(tree)
        if rank > 2**(n//2):
            return {
                "metric_name": "Brauer group rank",
                "metric_value": rank,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"Tree with {n} leaves has Brauer group rank {rank}, expected at most 2^{n//2}"
            }
        results.append((n, rank))
    return {
        "metric_name": "Brauer group rank",
        "metric_value": sum(rank for _, rank in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(rank <= 2**(n//2) for n, rank in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Brauer group rank exceeded expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")