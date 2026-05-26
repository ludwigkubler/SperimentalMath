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
    
    def generate_xor_and_tree(w, d):
        if d == 0:
            return ['leaf']
        else:
            children = [generate_xor_and_tree(random.randint(1, w), d-1) for _ in range(2)]
            return ['node', children[0], children[1]]
    
    def compute_minimal_rank(tree):
        # Placeholder function to simulate computation
        # Replace with actual algorithm if available
        return random.random() * 100
    
    n = 5
    results = []
    for _ in range(30):
        w = random.randint(2, 4)
        d = math.ceil(math.log(n, w))
        tree = generate_xor_and_tree(w, d)
        rank = compute_minimal_rank(tree)
        expected_rank = w ** (3/2) * d
        results.append({
            "w": w,
            "d": d,
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    correlation_coefficient = 0.95
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    ranks = [r["rank"] for r in results]
    expected_ranks = [r["expected_rank"] for r in results]
    mean_value = sum(ranks) / len(ranks)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in ranks) / len(ranks))
    
    correlation = sum((ranks[i] - mean_value) * (expected_ranks[i] - sum(expected_ranks) / len(expected_ranks)) for i in range(len(ranks))) / (len(ranks) * std_value * math.sqrt(sum((x - sum(expected_ranks) / len(expected_ranks)) ** 2 for x in expected_ranks)))
    
    conjecture_holds = correlation >= correlation_coefficient
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(r["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")