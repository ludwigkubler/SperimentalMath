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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f):
        n = int(math.log2(len(f)))
        tensor = [[f[i * 2 + j] for j in range(2)] for i in range(2)]
        return tensor
    
    def geometric_entropy(tensor):
        n = len(tensor)
        total = 0
        for row in tensor:
            count_0 = row.count(0)
            count_1 = row.count(1)
            if count_0 > 0:
                total += count_0 * math.log2(count_0 / n)
            if count_1 > 0:
                total += count_1 * math.log2(count_1 / n)
        return -total
    
    def circuit_size(f):
        n = int(math.log2(len(f)))
        stack = []
        for bit in f:
            if not stack or stack[-1] != bit:
                stack.append(bit)
            else:
                stack.pop()
        return len(stack) + 1
    
    instances_tested = 0
    metric_values = []
    n_max = 5
    
    for n in range(5, 41):
        f = generate_random_boolean_function(n)
        tensor = tensor_representation(f)
        entropy = geometric_entropy(tensor)
        size = circuit_size(f)
        
        if entropy is None or size is None:
            continue
        
        instances_tested += 1
        metric_values.append((entropy, math.log(size)))
        n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((x[0] * x[1] for x in metric_values)) / len(metric_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")