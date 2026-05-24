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
    
    def generate_bp(n):
        bp = []
        for _ in range(n):
            if random.choice([0, 1]):
                bp.append((random.randint(0, n-1), random.randint(0, n-1)))
            else:
                bp.append((random.randint(0, n-1),))
        return bp
    
    def quandle_representation(bp):
        q = {}
        for i in range(len(bp)):
            if len(bp[i]) == 2:
                x, y = bp[i]
                if (x, y) not in q:
                    q[(x, y)] = random.randint(0, n-1)
                if (y, x) not in q:
                    q[(y, x)] = random.randint(0, n-1)
            else:
                x = bp[i][0]
                if x not in q:
                    q[x] = random.randint(0, n-1)
        return q
    
    def minimal_rank(q):
        rank = 0
        for key in q:
            if isinstance(key, tuple):
                rank = max(rank, abs(q[key]))
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        bp = generate_bp(n)
        q = quandle_representation(bp)
        rank = minimal_rank(q)
        results.append({"n": n, "rank": rank})
    
    avg_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - avg_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["rank"] - math.log2(result["n"])) <= 3) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, std_rank={std_rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - avg_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_rank={avg_rank}, std_rank={std_rank}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")