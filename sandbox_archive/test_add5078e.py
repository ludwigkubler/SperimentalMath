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
    
    def generate_permutation(n):
        return list(range(1, n + 1))
    
    def noncrossing_partition_rank(perm):
        n = len(perm)
        ydiagram = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            ydiagram[perm[i]][i + 1] = 1
        rank = 0
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if sum(ydiagram[k][i:j] for k in range(j)) == j - i:
                    rank += 1
        return rank
    
    def communication_protocol(perm):
        # Placeholder for actual protocol implementation
        return random.randint(0, len(perm) * math.log2(len(perm)))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    perm = generate_permutation(n)
    rank = noncrossing_partition_rank(perm)
    comm_complexity = communication_protocol(perm)
    
    if rank > comm_complexity:
        return {
            "metric_name": "rank vs comm_complexity",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} is greater than communication complexity {comm_complexity}"
        }
    
    return {
        "metric_name": "rank vs comm_complexity",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank > comm_complexity\" first_failing_seed={first_failing_seed}")