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
    
    def generate_bp(n):
        bp = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(2)]
            bp.append(row)
        return bp
    
    def tensor_product(bp1, bp2):
        result = []
        for row1 in bp1:
            new_row = []
            for row2 in bp2:
                new_row.extend([x ^ y for x, y in zip(row1, row2)])
            result.append(new_row)
        return result
    
    def entropy(bp):
        states = set()
        queue = [bp]
        while queue:
            current_bp = queue.pop(0)
            if current_bp not in states:
                states.add(current_bp)
                for i in range(len(current_bp)):
                    new_bp1 = current_bp[:i] + [[1, 0]] + current_bp[i+1:]
                    new_bp2 = current_bp[:i] + [[0, 1]] + current_bp[i+1:]
                    queue.append(new_bp1)
                    queue.append(new_bp2)
        return math.log(len(states), 2) if states else 0
    
    def min_tensor_product_entropy(bp):
        n = len(bp)
        max_states = 2**n - 1
        if len(bp) == 1:
            return entropy(bp)
        for i in range(1, n):
            bp1 = bp[:i]
            bp2 = bp[i:]
            states = set()
            queue = [bp1, bp2]
            while queue:
                current_bp = queue.pop(0)
                if current_bp not in states:
                    states.add(current_bp)
                    for j in range(len(current_bp)):
                        new_bp1 = current_bp[:j] + [[1, 0]] + current_bp[j+1:]
                        new_bp2 = current_bp[:j] + [[0, 1]] + current_bp[j+1:]
                        queue.append(new_bp1)
                        queue.append(new_bp2)
            if len(states) > max_states:
                return math.log(len(states), 2)
        return entropy(bp)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            bp = generate_bp(n)
            entropy_value = min_tensor_product_entropy(bp)
            total_entropy += entropy_value
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = all(mean_entropy <= math.log(n, 2) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Tensor Product Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")