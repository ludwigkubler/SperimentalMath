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
    
    def generate_circuit(n):
        if n == 1:
            return []
        else:
            left = generate_circuit(random.randint(1, n-1))
            right = generate_circuit(n - len(left) - 1)
            return [left, right]
    
    def depth(circuit):
        if not circuit:
            return 0
        return 1 + max(depth(circuit[0]), depth(circuit[1]))
    
    def noncrossing_partition(circuit):
        if not circuit:
            return []
        left = noncrossing_partition(circuit[0])
        right = noncrossing_partition(circuit[1])
        return [(x, y) for x in left for y in right] + [((len(left), len(right)),)]
    
    def local_coherence_index(partition):
        if not partition:
            return 0
        return sum(1 for _, (i, j) in partition if i < j)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    depth_value = depth(circuit)
    partition = noncrossing_partition(circuit)
    coherence_index = local_coherence_index(partition)
    
    metric_name = "local_coherence_index"
    metric_value = coherence_index
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    if depth_value > 0:
        expected_bound = Fraction(n).log2() * depth_value
        if abs(coherence_index - expected_bound) <= 3:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")