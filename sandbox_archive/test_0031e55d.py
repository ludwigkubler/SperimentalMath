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
    
    def communication_protocol(f):
        n = len(f)
        protocol = []
        for i in range(2**n):
            input_bits = [i >> j & 1 for j in range(n)]
            output_bit = f[i]
            protocol.append((input_bits, output_bit))
        return protocol
    
    def shannon_entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    def geometric_entropy(protocol):
        n = len(protocol[0][0])
        counts = [0] * (2**n)
        for input_bits, _ in protocol:
            index = sum(bit << i for i, bit in enumerate(reversed(input_bits)))
            counts[index] += 1
        total_count = sum(counts)
        probabilities = [count / total_count for count in counts]
        return sum(shannon_entropy(p) for p in probabilities)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        protocol = communication_protocol(f)
        metric_value = geometric_entropy(protocol)
        metric_values.append(metric_value)
        instances_tested += len(protocol)
        n_max = max(n_max, n)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    if all(0.5 * n * math.log2(n) <= value <= 1.5 * n * math.log2(n) for value in metric_values):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "No linear correlation between H(G(P)) and n log n"
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) < 0.3:
        print(f"RESULT: FALSIFIED counterexample=\"No linear correlation between H(G(P)) and n log n\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_inconsistent_results")