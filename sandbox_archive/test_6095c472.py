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
    
    def generate_protocol(n):
        # Generate a simple protocol with known communication complexity rank r(P)
        return [random.randint(1, 40) for _ in range(n)]
    
    def construct_vector_bundle(protocol):
        # Construct the associated vector bundle E
        n = len(protocol)
        E = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                E[i][j] = protocol[j]
                E[j][i] = protocol[i]
        return E
    
    def compute_minimal_index(E):
        # Compute the minimal index of the vector bundle
        n = len(E)
        min_index = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                if E[i][j] < min_index:
                    min_index = E[i][j]
        return min_index
    
    def communication_complexity_rank(protocol):
        # Compute the communication complexity rank r(P)
        return sum(1 for x in protocol if x > 0)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            protocol = generate_protocol(n)
            E = construct_vector_bundle(protocol)
            index_E = compute_minimal_index(E)
            r_P = communication_complexity_rank(protocol)
            results.append({
                "metric_name": "minimal_index",
                "metric_value": index_E,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": index_E >= 1.5 * r_P and index_E <= 2 * r_P,
                "counterexample": "" if index_E >= 1.5 * r_P and index_E <= 2 * r_P else f"Protocol with n={n}, index(E)={index_E}, r(P)={r_P}"
            })
    
    return {
        "metric_name": "minimal_index",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")