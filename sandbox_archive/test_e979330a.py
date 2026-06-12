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
    
    def generate_circuit(depth):
        if depth == 0:
            return []
        else:
            inputs = [random.randint(1, 2) for _ in range(2)]
            operation = random.choice(['AND', 'OR'])
            return [(inputs, operation)] + generate_circuit(depth - 1)
    
    def calculate_quandle_rank(circuit):
        if not circuit:
            return 0
        quandle = {}
        for input_pair, op in circuit:
            key = (input_pair[0], input_pair[1], op)
            if key not in quandle:
                quandle[key] = len(quandle) + 1
        return len(quandle)
    
    def calculate_correlation(circuits):
        depths = [len(circuit) for circuit in circuits]
        ranks = [calculate_quandle_rank(circuit) for circuit in circuits]
        n = len(depths)
        if n < 2:
            return 0
        mean_depth = sum(depths) / n
        mean_rank = sum(ranks) / n
        numerator = sum((depths[i] - mean_depth) * (ranks[i] - mean_rank) for i in range(n))
        denominator = math.sqrt(sum((depths[i] - mean_depth) ** 2 for i in range(n)) * sum((ranks[i] - mean_rank) ** 2 for i in range(n)))
        if denominator == 0:
            return 0
        correlation_coefficient = numerator / denominator
        return abs(correlation_coefficient)
    
    circuits = [generate_circuit(d) for d in range(5, 41)]
    correlation_coefficient = calculate_correlation(circuits)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuits),
        "n_max": max(len(circuit) for circuit in circuits),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")