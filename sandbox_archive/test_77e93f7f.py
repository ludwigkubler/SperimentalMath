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
    
    # Generate a random XOR-AND tree with width w and depth d
    def generate_tree(w, d):
        if d == 0:
            return []
        else:
            children = [generate_tree(random.randint(1, w), d - 1) for _ in range(random.randint(1, w))]
            return [children]
    
    # Compute the minimal rank of the Schur algebra for a given tree
    def schur_algebra_rank(tree):
        if not tree:
            return 0
        else:
            children_ranks = [schur_algebra_rank(child) for child in tree[0]]
            return max(children_ranks) + 1
    
    # Parameters
    n = random.randint(5, 40)
    w = int(n ** (1/3))
    d = int(math.log2(n)) + 1
    
    # Generate the tree
    tree = generate_tree(w, d)
    
    # Compute the minimal rank of the Schur algebra
    computed_rank = schur_algebra_rank(tree)
    
    # Expected rank based on the conjecture
    expected_rank = math.floor(w ** (3/2) * d)
    
    # Check if the conjecture holds for this seed
    conjecture_holds = computed_rank >= expected_rank
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": computed_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={computed_rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")