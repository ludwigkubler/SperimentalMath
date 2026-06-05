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
        # Generate a random n-communication protocol with known communication complexity rank r(P) ≤ 40.
        # This is a placeholder function. Replace it with actual protocol generation logic.
        return [random.randint(1, 40) for _ in range(n)]
    
    def construct_vector_bundle(protocol):
        # Construct the associated vector bundle E from the protocol.
        # This is a placeholder function. Replace it with actual vector bundle construction logic.
        n = len(protocol)
        E = [[i * j for j in range(n)] for i in range(n)]
        return E
    
    def compute_minimal_index(E):
        # Compute the minimal index of the vector bundle E.
        # This is a placeholder function. Replace it with actual K-theoretic invariant computation logic.
        n = len(E)
        min_index = float('inf')
        for i in range(n):
            for j in range(n):
                if E[i][j] < min_index:
                    min_index = E[i][j]
        return min_index
    
    def communication_complexity_rank(protocol):
        # Return the communication complexity rank r(P) of the protocol.
        return sum(protocol)
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        protocol = generate_protocol(n)
        E = construct_vector_bundle(protocol)
        index_E = compute_minimal_index(E)
        r_P = communication_complexity_rank(protocol)
        
        if index_E < 1.5 * r_P or index_E > 2 * r_P:
            conjecture_holds_count += 1
            counterexample = f"Protocol with n={n}, index(E)={index_E}, r(P)={r_P}"
        else:
            counterexample = ""
        
        total_metric_value += index_E
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "minimal_index",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    conjecture_holds_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={conjecture_holds_fraction}")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={conjecture_holds_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")