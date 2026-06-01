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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = float('inf')
        for i in range(1 << n):
            if all(circuit[j] == (i & (1 << j)) >> j for j in range(n)):
                width = min(width, bin(i).count('1'))
        return width
    
    def local_ring_index(circuit):
        n = len(circuit)
        ring = []
        for i in range(1 << n):
            row = [circuit[j] if (i & (1 << j)) else 0 for j in range(n)]
            ring.append(row)
        generators = []
        for i in range(n):
            generator = [0] * n
            generator[i] = 1
            generators.append(generator)
        return len(generators)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / (n - 1))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / (n - 1))
        return cov / (std_x * std_y)
    
    def bootstrap_test(x, y, n_samples=30):
        n = len(x)
        samples = []
        for _ in range(n_samples):
            indices = random.sample(range(n), n)
            sample_x = [x[i] for i in indices]
            sample_y = [y[i] for i in indices]
            samples.append(correlation_coefficient(sample_x, sample_y))
        mean_sample = sum(samples) / len(samples)
        std_sample = math.sqrt(sum((s - mean_sample)**2 for s in samples) / (len(samples) - 1))
        return mean_sample, std_sample
    
    n_values = [5, 10, 15, 20, 30, 40]
    idx_values = []
    width_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            idx = local_ring_index(circuit)
            width = monotone_width(circuit)
            idx_values.append(idx)
            width_values.append(width)
    
    mean_idx = sum(idx_values) / len(idx_values)
    std_idx = math.sqrt(sum((idx - mean_idx)**2 for idx in idx_values) / (len(idx_values) - 1))
    mean_width = sum(width_values) / len(width_values)
    std_width = math.sqrt(sum((width - mean_width)**2 for width in width_values) / (len(width_values) - 1))
    
    alpha = 0.8
    p_value, _ = bootstrap_test(idx_values, width_values)
    
    metric_name = "correlation_coefficient"
    metric_value = correlation_coefficient(idx_values, width_values)
    instances_tested = len(idx_values)
    n_max = max(n_values)
    conjecture_holds = metric_value >= alpha and p_value <= 0.05
    counterexample = "" if conjecture_holds else f"alpha={alpha}, p_value={p_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha={alpha}, p_value={p_value}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")