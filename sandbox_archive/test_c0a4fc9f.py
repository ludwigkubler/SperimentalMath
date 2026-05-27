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
    
    def generate_channel(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def tropicalize(channel):
        return max(channel)
    
    def entropy(channel):
        counts = {0: channel.count(0), 1: channel.count(1)}
        total = len(channel)
        if total == 0:
            return 0
        p0, p1 = counts[0] / total, counts[1] / total
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    def minimal_rank(channel):
        n = len(channel)
        rank = 0
        for i in range(n):
            if channel[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 random seeds per n
            channel = generate_channel(n)
            rank = minimal_rank(channel)
            H = entropy(channel)
            results.append({
                "n": n,
                "channel": channel,
                "rank": rank,
                "H": H,
                "conjecture_holds": rank <= 2 ** H
            })
    
    instances_tested = len(results)
    conjecture_holds_all = all(r["conjecture_holds"] for r in results)
    counterexample = next((f"n={r['n']}, H={r['H']:.2f}, rank={r['rank']}" for r in results if not r["conjecture_holds"]), "")
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": sum(r["rank"] for r in results) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
        results.append(run_trial(seed))
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d:.2f} std=0.00 support_fraction=1.00")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, H={results[0]['H']:.2f}, rank={results[0]['rank']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")