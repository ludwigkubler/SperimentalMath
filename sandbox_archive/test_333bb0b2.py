# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def shannon_entropy(f):
        counts = [f.count(i) for i in range(2)]
        total = sum(counts)
        if total == 0:
            return 0
        probabilities = [count / total for count in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy
    
    def geometric_flow_order(f):
        n = len(f)
        order = 0
        while True:
            new_f = ''.join(str(1 - int(bit)) for bit in f)
            if new_f == f:
                break
            f = new_f
            order += 1
        return order
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    instances_tested = 0
    total_order = 0
    total_entropy = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 30:
            break
        for _ in range(5):
            f = generate_boolean_function(n)
            instances_tested += 1
            n_max = max(n_max, n)
            order = geometric_flow_order(f)
            entropy = shannon_entropy(f)
            total_order += order
            total_entropy += entropy
    
    if instances_tested < 30:
        return {
            "metric_name": "Order/Entropy Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ratio = total_order / total_entropy
    return {
        "metric_name": "Order/Entropy Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True if 1 <= ratio <= 2 else False,
        "counterexample": "" if 1 <= ratio <= 2 else f"Ratio out of bounds: {ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")