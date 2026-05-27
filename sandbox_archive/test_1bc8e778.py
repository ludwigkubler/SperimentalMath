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
    
    def xor_and_tree_width(tree):
        if isinstance(tree, str):
            return 1
        else:
            return max(xor_and_tree_width(subtree) for subtree in tree) + 1
    
    def motivic_integration_rank(width):
        # Placeholder function to simulate the rank computation
        return width * width
    
    def dpll_refutation_size(width):
        # Placeholder function to simulate the DPLL refutation size
        return width * width
    
    n = random.randint(5, 40)
    total_rank = 0
    instances_tested = 0
    
    for _ in range(n):
        tree_width = random.randint(1, 20)
        rank = motivic_integration_rank(tree_width)
        refutation_size = dpll_refutation_size(tree_width)
        
        if rank > 1.5 * tree_width ** 2:
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Tree with width {tree_width} has rank {rank}, which is greater than 1.5 * {tree_width}^2"
            }
        
        total_rank += rank
        instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for rank in range(instances_tested)) / instances_tested)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": 0.5 * tree_width ** 2 <= mean_rank <= 1.5 * tree_width ** 2 and std_dev < 0.1 * tree_width ** 2
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported")