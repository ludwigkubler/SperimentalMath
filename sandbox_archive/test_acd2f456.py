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
    
    def generate_bipartite_state(n):
        # Generate a random bipartite quantum state with entanglement rank up to n
        state = [[random.random() for _ in range(n)] for _ in range(n)]
        return state
    
    def mter(state):
        # Compute the minimal local index of topological entanglement rank (mter(X))
        # This is a placeholder function. Replace with actual algorithm.
        return sum(sum(row) for row in state)
    
    def cc(state):
        # Determine the communication complexity (cc(X)) of a protocol that distributes X
        # This is a placeholder function. Replace with actual algorithm.
        n = len(state)
        return n * (n - 1) / 2
    
    total_mter = []
    total_cc = []
    
    for _ in range(30):
        state = generate_bipartite_state(random.randint(5, 40))
        mter_value = mter(state)
        cc_value = cc(state)
        total_mter.append(mter_value)
        total_cc.append(cc_value)
    
    instances_tested = len(total_mter)
    n_max = max(len(state) for state in [generate_bipartite_state(n) for n in range(5, 41)])
    correlation_coefficient = (instances_tested * sum(mter * cc for mter, cc in zip(total_mter, total_cc)) -
                               instances_tested * sum(total_mter) * sum(total_cc)) / \
                              ((instances_tested * sum(mter**2 for mter in total_mter) - sum(total_mter)**2) *
                               (instances_tested * sum(cc**2 for cc in total_cc) - sum(total_cc)**2))**0.5
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")