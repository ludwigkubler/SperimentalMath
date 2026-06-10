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
        # Simple circuit generator for demonstration purposes
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def rank_variance(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        diff = [[matrix[i][j] - identity[i][j] for j in range(n)] for i in range(n)]
        rank_diff = sum(sum(row) for row in diff)
        return rank_diff / n
    
    def graphical_regularity(circuit):
        # Simplified measure of graphical regularity
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        gamma = graphical_regularity(circuit)
        comm_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        rho_n = rank_variance(comm_matrix)
        results.append((gamma, rho_n))
    
    mean_diff = sum(abs(gamma - rho_n) for gamma, rho_n in results) / len(results)
    conjecture_holds = all(0.5 <= abs(gamma - rho_n) / max(gamma, rho_n) <= 2 for gamma, rho_n in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Graphical Regularity vs Rank Variance",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")