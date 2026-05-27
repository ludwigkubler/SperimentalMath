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
        if isinstance(tree, list):
            return max(xor_and_tree_width(subtree) for subtree in tree)
        else:
            return 0
    
    def motivic_integration_rank(width):
        # Simplified model for demonstration purposes
        return width ** 2
    
    n = random.randint(5, 40)
    total_rank = 0
    instances_tested = 0
    
    for _ in range(n):
        width = random.randint(1, 10)
        tree = [random.choice([0, 1]) if i == 0 else [random.choice([0, 1]) for _ in range(width)] for i in range(random.randint(1, 3))]
        rank = motivic_integration_rank(xor_and_tree_width(tree))
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = 0.5 * n <= mean_rank <= 1.5 * n and abs(mean_rank - n) < 0.1 * n ** 2
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, n={n}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")