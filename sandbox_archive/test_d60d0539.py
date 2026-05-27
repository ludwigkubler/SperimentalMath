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
    
    def xor_and_tree(n):
        if n == 1:
            return [0, 1]
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return [x ^ y for x in left] + [x & y for x in left] + [x ^ y for x in right] + [x & y for x in right]
    
    def characteristic_polynomial(tree):
        if len(tree) == 1:
            return tree[0]
        else:
            poly = characteristic_polynomial(tree[:len(tree)//2])
            return [poly[i] ^ poly[j] for i in range(len(poly)) for j in range(i+1, len(poly))] + [tree[len(tree)//2]]
    
    def brauer_group_rank(n):
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return 2 * (brauer_group_rank(n // 2) - 1)
    
    results = []
    for n in range(5, 41):
        tree = xor_and_tree(n)
        char_poly = characteristic_polynomial(tree)
        rank = brauer_group_rank(n)
        if rank > 2 ** (n / 2):
            return {
                "metric_name": "brauer_group_rank",
                "metric_value": rank,
                "instances_tested": n - 4,
                "conjecture_holds": False,
                "counterexample": f"XOR-AND tree with {n} leaves has Brauer group rank {rank}, which is greater than 2^{n/2}"
            }
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    return {
        "metric_name": "brauer_group_rank",
        "metric_value": mean_rank,
        "instances_tested": 36,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2 ** (len(bin(len(seeds)) - 2) / 2)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r > 2 ** (len(bin(len(seeds)) - 2) / 2) for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='Brauer group rank exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")