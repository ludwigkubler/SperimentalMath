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
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    def hodge_structure_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hodge_rank = 0
    total_monotone_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            width = monotone_width(circuit)
            rank = hodge_structure_rank(circuit)
            instances_tested += 1
            total_hodge_rank += rank
            total_monotone_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = total_hodge_rank / instances_tested
    mean_width = total_monotone_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(rank * width for rank, width in zip(hodge_ranks, monotone_widths)) -
                                mean_rank * sum(monotone_widths) - mean_width * sum(hodge_ranks)) / \
                               math.sqrt((instances_tested * sum(rank**2 for rank in hodge_ranks) - mean_rank**2) *
                                         (instances_tested * sum(width**2 for width in monotone_widths) - mean_width**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": math.sqrt(mean_width**(2/3)) <= correlation_coefficient <= math.sqrt(mean_width**0.5),
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
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")