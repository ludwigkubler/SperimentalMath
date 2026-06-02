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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def depth(circuit):
        if not circuit:
            return 0
        max_depth = 0
        for i in range(len(circuit)):
            if circuit[i] == 1:
                sub_circuit = circuit[:i] + circuit[i+1:]
                max_depth = max(max_depth, depth(sub_circuit) + 1)
        return max_depth
    
    def mlc(circuit):
        # Placeholder for minimal local coherence calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(circuit) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    mlc_values = []
    depth_values = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        mlc_value = mlc(circuit)
        depth_value = depth(circuit)
        mlc_values.append(mlc_value)
        depth_values.append(depth_value)
    
    correlation_coefficient = sum((mlc_values[i] - mean_mlc) * (depth_values[i] - mean_depth) for i in range(len(n_values))) / len(n_values)
    mean_mlc = sum(mlc_values) / len(mlc_values)
    mean_depth = sum(depth_values) / len(depth_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= abs(correlation_coefficient) <= 1.2 and all(0.5 <= abs(mlc_val - depth_val) / (mlc_val + depth_val) <= 3 for mlc_val, depth_val in zip(mlc_values, depth_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")