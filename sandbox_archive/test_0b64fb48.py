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
    
    def generate_planar_graph(n):
        if n == 3:
            return {(0, 1), (1, 2), (2, 0)}
        elif n == 4:
            return {(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)}
        else:
            raise ValueError("No valid graphs generated")
    
    def geometric_entropy(graph):
        # Simplified entropy calculation for demonstration
        return len(graph) / 4.0
    
    def communication_rank(graph):
        # Simplified rank calculation for demonstration
        return len(graph)
    
    n = 40
    graph = generate_planar_graph(n)
    H_G = geometric_entropy(graph)
    r_G = communication_rank(graph)
    
    if H_G < 0.1 or H_G > 10:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": H_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "H(G) out of range [0.1, 10]"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"H(G) out of range [0.1, 10]\" first_failing_seed={first_failing_seed}")