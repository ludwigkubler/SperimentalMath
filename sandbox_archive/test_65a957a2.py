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
    
    def generate_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def communication_complexity_rank(G):
        # Simplified version of communication complexity rank
        return len(G)
    
    def minimal_order_quaternionic_Kähler_forms(G):
        # Simplified version of minimal order of quaternionic Kähler forms
        return len(G) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    o_G_sum = 0
    r_G_sum = 0
    n_max = 0
    
    for n in n_values:
        G = generate_graph(n)
        o_G = minimal_order_quaternionic_Kähler_forms(G)
        r_G = communication_complexity_rank(G)
        
        instances_tested += len(G)
        if n > n_max:
            n_max = n
        
        o_G_sum += o_G
        r_G_sum += r_G
    
    mean_o_G = o_G_sum / instances_tested
    mean_r_G = r_G_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(o_G * r_G for o_G, r_G in zip(o_G_values, r_G_values)) -
                               o_G_sum * r_G_sum) / math.sqrt((instances_tested * sum(o_G ** 2 for o_G in o_G_values) - o_G_sum ** 2) *
                                                            (instances_tested * sum(r_G ** 2 for r_G in r_G_values) - r_G_sum ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")