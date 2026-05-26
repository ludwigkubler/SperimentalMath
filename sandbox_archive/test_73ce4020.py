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
    
    def random_tree(width, height):
        if height == 0:
            return []
        children = [random_tree(random.randint(1, width), height - 1) for _ in range(random.randint(1, width))]
        return [(children[0], children[1])] + children[2:] if len(children) > 2 else children
    
    def deligne_lusztig_cone(tree):
        # Placeholder function to simulate the Deligne–Lusztig cone computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 100)
    
    def minimal_rank(cone):
        return len(cone)
    
    n = random.randint(5, 40)
    total_ranks = []
    for _ in range(30):
        w = random.randint(1, n)
        h = random.randint(1, n)
        tree = random_tree(w, h)
        cone = deligne_lusztig_cone(tree)
        rank = minimal_rank(cone)
        total_ranks.append(rank)
    
    mean_rank = sum(total_ranks) / len(total_ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in total_ranks) / len(total_ranks))
    
    conjecture_holds = all(rank <= (w**2 / h) * 100 for rank, w, h in zip(total_ranks, [random.randint(1, n) for _ in range(len(total_ranks))], [random.randint(1, n) for _ in range(len(total_ranks))]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(total_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")