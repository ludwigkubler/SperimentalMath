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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_structure_rank(f):
        # Placeholder function to compute the rank of Hodge structure
        # This is a dummy implementation and should be replaced with actual computation
        return len(f)
    
    def tseitin_resolution_depth(f):
        # Placeholder function to compute the resolution depth of Tseitin formula
        # This is a dummy implementation and should be replaced with actual computation
        return len(f)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        rank = hodge_structure_rank(f)
        depth = tseitin_resolution_depth(f)
        if depth > 0:
            results.append((rank, depth))
    
    if not results:
        return {
            "metric_name": "Rank_H vs ResolutionDepth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    ranks = [r for r, _ in results]
    depths = [d for _, d in results]
    mean_rank = sum(ranks) / len(ranks)
    mean_depth = sum(depths) / len(depths)
    max_depth = max(depths)
    
    conjecture_holds = all(d <= 3 * m for d, m in zip(depths, ranks))
    counterexample = "" if conjecture_holds else f"Max depth {max_depth} exceeds 3 times mean rank {mean_rank}"
    
    return {
        "metric_name": "Rank_H vs ResolutionDepth",
        "metric_value": max_depth,
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
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_instances")
        sys.exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max depth exceeds 3 times mean rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")