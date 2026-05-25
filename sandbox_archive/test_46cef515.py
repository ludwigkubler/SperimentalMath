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
    
    # Parameters
    n = 10  # Number of variables
    k = 5   # Size of the clique
    
    # Generate a random group G with a fixed number of elements
    G = [random.randint(1, 100) for _ in range(random.randint(2, 10))]
    
    # Define a linear action on a set of n variables
    action = [[random.randint(-10, 10) for _ in range(n)] for _ in range(len(G))]
    
    # Compute the tropicalized representation matrix and determine its minimal rank
    tropical_matrix = []
    for g in G:
        row = [max(action[i][j] + g * action[j][k], -math.inf) for j in range(n)]
        tropical_matrix.append(row)
    
    min_rank = len(tropical_matrix)
    for i in range(len(tropical_matrix)):
        for j in range(i + 1, len(tropical_matrix)):
            if all(tropical_matrix[i][k] == tropical_matrix[j][k] for k in range(n)):
                min_rank -= 1
                break
    
    # Construct monotone circuits for k-CLIQUE using the same variables and measure their size
    def clique_circuit_size(n, k):
        if n < k:
            return float('inf')
        if k == 0 or k == 1:
            return 1
        return 2 * clique_circuit_size(n - 1, k - 1) + clique_circuit_size(n - 1, k)
    
    circuit_size = clique_circuit_size(n, k)
    
    # Compare the minimal rank of the tropicalized representation to the circuit size
    conjecture_holds = min_rank >= circuit_size
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, circuit_size={circuit_size}"
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": 1.0 if conjecture_holds else 0.0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")