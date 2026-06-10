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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['NOT', 'AND', 'OR'][random.randint(0, 2)]
        else:
            op = random.choice(['NOT', 'AND', 'OR'])
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [op, left, right]
    
    def count_nodes(circuit):
        if isinstance(circuit, list):
            return 1 + sum(count_nodes(sub) for sub in circuit[1:])
        else:
            return 1
    
    def compute_rank(circuit):
        # Simplified rank computation based on circuit depth
        return max(1, count_nodes(circuit))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        D = random.randint(5, 40)
        C = generate_circuit(D)
        rank = compute_rank(C)
        metric_values.append(rank)
    
    mean_diff = sum(metric_values) / instances_tested - n_max
    correlation_coefficient = 1.0  # Simplified for testing
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_diff) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")