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
    
    def walsh_hadamard_transform(truth_table):
        n = len(truth_table)
        for k in range(1, n):
            mask = 1 << k
            for i in range(n // (2 ** (k + 1))):
                for j in range(2 ** k):
                    truth_table[i * (2 ** (k + 1)) + j] += truth_table[i * (2 ** (k + 1)) + j + mask]
        return [x / (2 ** n) if x >= 0 else -x / (2 ** n) for x in truth_table]

    def generate_bp(n, w):
        layers = [[] for _ in range(w)]
        variables = list(range(2 * n))
        random.shuffle(variables)
        
        for i in range(w):
            layer = []
            for j in range(n // w):
                var1, var2 = variables.pop(), variables.pop()
                label = random.choice([0, 1])
                layer.append((var1, var2, label))
            layers[i] = layer
        
        sink_label = random.choice([0, 1])
        return layers, sink_label

    def compute_fourier_l1_norm(truth_table):
        n = len(truth_table)
        return sum(abs(x) for x in truth_table)

    results = []
    for n in [6, 8, 10, 12, 14]:
        for w in [2, 3, 4]:
            s = 2 * n * w + 2
            for _ in range(30):
                layers, sink_label = generate_bp(n, w)
                truth_table = [0] * (2 ** n)
                for x in range(2 ** n):
                    state = x
                    for layer in layers:
                        var1, var2, label = layer[(state & 1) ^ label]
                        if state & (1 << var1):
                            state ^= 1 << var2
                        else:
                            state ^= 1 << var1
                    truth_table[x] += (-1) ** sink_label
    
                fourier_norm = compute_fourier_l1_norm(truth_table)
                results.append({
                    "n": n,
                    "w": w,
                    "s": s,
                    "fourier_norm": fourier_norm
                })

    mean_norm = sum(result["fourier_norm"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["fourier_norm"] - mean_norm) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["fourier_norm"] <= (result["s"] + 1) ** 3) / len(results)

    return {
        "metric_name": "Fourier L1 Norm",
        "metric_value": mean_norm,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 28 / 30,
        "counterexample": "" if support_fraction >= 28 / 30 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["metric_value"] - mean_norm) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")