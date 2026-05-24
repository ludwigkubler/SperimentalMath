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
        bp = [random.choice([0, 1]) for _ in range(n)]
        return bp
    
    def quandle_representation(bp):
        n = len(bp)
        q = [[i for i in range(n)]]
        for i in range(1, n):
            new_q = []
            for j in range(len(q)):
                new_q.append([(q[j][k] + bp[k]) % n for k in range(i)])
            q.extend(new_q)
        return q
    
    def minimal_rank(q):
        n = len(q[0])
        rank = 1
        while True:
            found = False
            for i in range(n):
                if all(q[j][i] == j for j in range(rank)):
                    found = True
                    break
            if not found:
                return rank
            rank += 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_bp(n)
        q = quandle_representation(bp)
        rank = minimal_rank(q)
        results.append({"n": n, "rank": rank})
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    std_dev = math.sqrt(sum((result["rank"] - avg_rank) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(3 <= result["rank"] <= 5 * math.log(result["n"], 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")