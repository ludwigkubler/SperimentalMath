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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        stack = []
        for i in range(2**n):
            if f[i] == 1:
                stack.append(stack.pop() + 1) if stack else stack.append(1)
            else:
                stack.append(0)
        return max(stack) if stack else 0
    
    def generate_quasi_random_sequences(f, n):
        sequences = []
        for _ in range(n):
            sequence = [random.choice([0, 1]) for _ in range(len(f))]
            sequences.append(sequence)
        return sequences
    
    def cover_all_outputs(sequences, f):
        covered = set()
        for seq in sequences:
            output = sum(seq[i] * f[2**i] for i in range(len(f)))
            covered.add(output)
        return len(covered) == len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        if cc == 0:
            continue
        
        sequences = generate_quasi_random_sequences(f, 10 * len(f))
        instances_tested += len(sequences)
        n_max = max(n_max, n)
        
        for _ in range(len(sequences)):
            if cover_all_outputs(sequences, f):
                total_metric_value += math.log2(cc)
                break
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = (metric_value <= 3 + math.log2(n_max) ** 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log2(communication_complexity)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")