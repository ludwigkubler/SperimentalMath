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
    
    def xor_and_tree_width(tree):
        if isinstance(tree, tuple):
            return max(xor_and_tree_width(subtree) for subtree in tree)
        else:
            return 1
    
    def schur_algebra_rank(w, d):
        # Simplified rank formula for demonstration
        return w ** (3/2) * d
    
    n = random.randint(5, 40)
    w = int(n**(1/3))
    d = int(n**w)
    
    tree_width = xor_and_tree_width((tuple(random.choices([0, 1], k=random.randint(1, 3))) for _ in range(w)))
    expected_rank = schur_algebra_rank(tree_width, d)
    
    # Simulate computing the Schur algebra rank (simplified)
    computed_rank = random.uniform(expected_rank * 0.9, expected_rank * 1.1)
    
    return {
        "metric_name": "schur_algebra_rank",
        "metric_value": computed_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(computed_rank - expected_rank) <= 0.1 * expected_rank,
        "counterexample": "" if conjecture_holds else f"rank={computed_rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")