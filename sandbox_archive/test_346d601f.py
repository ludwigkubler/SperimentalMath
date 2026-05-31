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
    
    def generate_circuit(n, m):
        circuit = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
        return circuit
    
    def hyperbolic_metric_entropy(circuit):
        n = len(circuit)
        m = len(circuit[0])
        entropy = 0
        for i in range(n):
            for j in range(m):
                if circuit[i][j] == 1:
                    entropy += math.log2(1 + n * m)
        return entropy
    
    def satisfiability_time(circuit):
        n = len(circuit)
        m = len(circuit[0])
        time = 0
        for i in range(n):
            for j in range(m):
                if circuit[i][j] == 1:
                    time += 1
        return time
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * 2)
        circuit = generate_circuit(n, m)
        entropy = hyperbolic_metric_entropy(circuit)
        time = satisfiability_time(circuit)
        
        if entropy > 10:
            return {
                "metric_name": "hyperbolic_metric_entropy",
                "metric_value": entropy,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "entropy_exceeds_10"
            }
        
        metric_values.append((entropy, time))
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        mean_entropy = sum(x for x, _ in metric_values) / len(metric_values)
        mean_time = sum(y for _, y in metric_values) / len(metric_values)
        
        numerator = sum((x - mean_entropy) * (y - mean_time) for x, y in metric_values)
        denominator = math.sqrt(sum((x - mean_entropy) ** 2 for x, _ in metric_values)) * math.sqrt(sum((y - mean_time) ** 2 for _, y in metric_values))
        
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "hyperbolic_metric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")