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
    
    def generate_frege_tree(depth, max_depth):
        if depth == max_depth:
            return []
        else:
            return [generate_frege_tree(random.randint(1, depth), depth - 1)]
    
    def compute_min_rank(tree):
        if not tree:
            return 0
        left_rank = compute_min_rank(tree[0])
        right_rank = compute_min_rank(tree[1]) if len(tree) > 1 else 0
        return max(left_rank, right_rank) + 1
    
    def generate_quiver_representation(tree):
        if not tree:
            return 1
        left_rep = generate_quiver_representation(tree[0])
        right_rep = generate_quiver_representation(tree[1]) if len(tree) > 1 else 1
        return left_rep * right_rep
    
    n = random.randint(5, 40)
    depth = math.ceil(math.log(n))
    tree = generate_frege_tree(depth, depth)
    
    min_rank = compute_min_rank(tree)
    quiver_dimension = generate_quiver_representation(tree)
    
    conjecture_holds = (min_rank <= depth) and (quiver_dimension <= 2 ** depth)
    counterexample = "" if conjecture_holds else f"Depth={depth}, MinRank={min_rank}, QuiverDim={quiver_dimension}"
    
    return {
        "metric_name": "MinRank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.4f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")