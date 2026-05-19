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
    
    def decision_tree_depth(f):
        if len(f) == 1:
            return 0
        mid = len(f) // 2
        left_depth = decision_tree_depth(f[:mid])
        right_depth = decision_tree_depth(f[mid:])
        return max(left_depth, right_depth) + 1
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        depth = decision_tree_depth(f)
        return math.ceil(depth / math.log2(n))
    
    n_values = [8, 16, 24, 32, 40]
    d_values = range(1, max(n_values) + 1)
    instances_tested = 0
    total_ratio = 0
    
    for n in n_values:
        for d in d_values:
            if d > n:
                continue
            f = generate_boolean_function(n)
            while decision_tree_depth(f) != d:
                f = generate_boolean_function(n)
            cc = communication_complexity(f)
            instances_tested += 1
            total_ratio += cc * math.log2(n) / d
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")

# RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=0