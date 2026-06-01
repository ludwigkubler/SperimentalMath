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
    
    def monotone_width(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        width = float('inf')
        for i in range(1, n):
            left = circuit[:i]
            right = circuit[i:]
            if all(x <= y for x, y in zip(left, right)):
                width = min(width, monotone_width(left) + monotone_width(right))
        return width
    
    def local_ring_index(circuit):
        n = len(circuit)
        ring = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all(x <= y for x, y in zip(bin(i)[2:].zfill(n), bin(j)[2:].zfill(n))):
                    ring[i][j] = 1
        generators = []
        for i in range(2**n):
            if any(ring[i][j] == 1 for j in range(2**n)):
                generators.append(i)
        return len(generators)
    
    def correlation(xs, ys):
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n)) / n
        var_x = sum((xs[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((ys[i] - mean_y)**2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    def bootstrap(xs, ys, num_samples):
        n = len(xs)
        samples = []
        for _ in range(num_samples):
            indices = random.sample(range(n), n)
            sample_xs = [xs[i] for i in indices]
            sample_ys = [ys[i] for i in indices]
            samples.append(correlation(sample_xs, sample_ys))
        return samples
    
    n_values = [5, 10, 15, 20, 30, 40]
    idxs = []
    widths = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            idx = local_ring_index(circuit)
            width = monotone_width(circuit)
            idxs.append(idx)
            widths.append(width)
    
    corr = correlation(idxs, widths)
    bootstrap_samples = bootstrap(idxs, widths, 30)
    p_value = sum(1 for s in bootstrap_samples if abs(s) >= abs(corr)) / len(bootstrap_samples)
    
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(idxs),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.8 and p_value <= 0.05,
        "counterexample": "" if corr >= 0.8 and p_value <= 0.05 else f"correlation={corr}, p_value={p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")