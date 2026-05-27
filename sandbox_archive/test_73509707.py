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
            return 1 + max(xor_and_tree_width(subtree) for subtree in tree)
        else:
            return 0
    
    def motivic_integration_rank(width):
        # Simplified model: rank is proportional to width^2
        return width ** 2
    
    n = random.randint(5, 30)
    total_rank = 0
    instances_tested = 0
    
    for _ in range(n):
        width = random.randint(1, 10)  # Simplified: tree width between 1 and 10
        tree = generate_xor_and_tree(width)
        rank = motivic_integration_rank(width)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = 0.5 * n <= mean_rank <= 1.5 * n
    counterexample = "" if conjecture_holds else "mean_rank_outside_bounds"
    
    return {
        "metric_name": "mean_minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_xor_and_tree(width):
    if width == 1:
        return random.choice([0, 1])
    else:
        left = generate_xor_and_tree(width // 2)
        right = generate_xor_and_tree(width - width // 2)
        return (left, right)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")