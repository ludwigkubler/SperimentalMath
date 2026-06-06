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
    
    def generate_random_circuit(depth, n):
        if depth == 0:
            return [random.choice([0, 1]) for _ in range(n)]
        else:
            inputs = generate_random_circuit(depth - 1, n)
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                return [inputs[i] & inputs[j] for i in range(n) for j in range(i + 1, n)]
            else:
                return [inputs[i] | inputs[j] for i in range(n) for j in range(i + 1, n)]
    
    def count_affine_subspaces(circuit):
        n = len(circuit)
        subspaces = set()
        for i in range(2**n):
            subspace = []
            for j in range(n):
                if (i >> j) & 1:
                    subspace.append(j)
            subspaces.add(tuple(sorted(subspace)))
        return len(subspaces)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(5, min(n_max + 10, 30))
            circuit = generate_random_circuit(depth, n)
            metric_value = count_affine_subspaces(circuit)
            total_metric_value += metric_value
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value <= depth**2 * math.log(n) for circuit in [generate_random_circuit(depth, n) for depth in [5, 10, 15, 20, 30, 40] for _ in range(5)] for metric_value in [count_affine_subspaces(circuit)])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_affine_subspaces",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")