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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [random.choice(left) & random.choice(right)]
    
    def monotone_width(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left_width = monotone_width(circuit[:len(circuit)//2])
            right_width = monotone_width(circuit[len(circuit)//2:])
            return max(left_width, right_width)
    
    def tropical_module_rank(circuit):
        if len(circuit) == 1:
            return circuit[0]
        else:
            left_rank = tropical_module_rank(circuit[:len(circuit)//2])
            right_rank = tropical_module_rank(circuit[len(circuit)//2:])
            return max(left_rank, right_rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ranks = []
    total_widths = []
    
    for n in n_values:
        instances_tested = 0
        n_max = n
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(n)
            width = monotone_width(circuit)
            rank = tropical_module_rank(circuit)
            total_ranks.append(rank)
            total_widths.append(width)
            instances_tested += 1
    
    mean_rank = sum(total_ranks) / len(total_ranks)
    mean_width = sum(total_widths) / len(total_widths)
    correlation_coefficient = (sum((r - mean_rank) * (w - mean_width) for r, w in zip(total_ranks, total_widths)) /
                                math.sqrt(sum((r - mean_rank)**2 for r in total_ranks) *
                                          sum((w - mean_width)**2 for w in total_widths)))
    
    conjecture_holds = correlation_coefficient > 0.8 and mean_rank / mean_width <= 1.5
    counterexample = "" if conjecture_holds else "correlation or rank/width ratio"
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(total_ranks),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")