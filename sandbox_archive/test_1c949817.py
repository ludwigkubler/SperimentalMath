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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_depth = 0
        stack = []
        for bit in f:
            if bit == 0:
                stack.append(0)
            else:
                stack.append(stack.pop() + 1)
            max_depth = max(max_depth, len(stack))
        return max_depth
    
    def quasi_random_sequences(f):
        n = len(f)
        sequences = []
        for _ in range(n * n):
            sequence = [random.choice([0, 1]) for _ in range(n)]
            if all(sequence[i] == f[i] for i in range(n)):
                sequences.append(sequence)
        return sequences
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_sequences = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        sequences = quasi_random_sequences(f)
        total_sequences += len(sequences)
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_sequences = total_sequences / instances_tested
    log_n_values = [math.log2(n) for n in n_values]
    log_mean_sequences = math.log2(mean_sequences)
    diff = abs(log_mean_sequences - (log_n_values[-1] ** 2))
    
    conjecture_holds = diff <= 3
    counterexample = "" if conjecture_holds else f"mean_diff={diff}"
    
    return {
        "metric_name": "Logarithm of Mean Sequences",
        "metric_value": log_mean_sequences,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")