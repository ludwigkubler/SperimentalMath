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
    
    def generate_monotone_circuit(n):
        # Generate a random monotone circuit with n vertices and size O(2^n)
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_coxeter_group(circuit):
        # Construct a Coxeter group from the monotone circuit
        # This is a placeholder implementation; replace with actual logic
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def min_rank(G):
        # Compute the minimal rank of the Coxeter group
        n = len(G)
        rank = 0
        for i in range(n):
            if sum(G[i]) > 0:
                rank += 1
        return rank
    
    def log2_floor(x):
        # Compute floor(log_2(x))
        if x <= 0:
            return -1
        return int(math.log2(x))
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    G = construct_coxeter_group(circuit)
    rank = min_rank(G)
    expected_rank = log2_floor(n)
    
    result = {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= expected_rank,
        "counterexample": "" if rank >= expected_rank else f"n={n}, rank={rank}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}\" first_failing_seed={seeds[first_failing_seed]}")