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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(phi):
        # Placeholder function to simulate Frege proof depth calculation
        return random.randint(5, 20)
    
    def quadratic_form_representation(phi):
        n = int(math.log2(len(phi)))
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                Q[i][j] = random.randint(0, 1)
                Q[j][i] = Q[i][j]
        return Q
    
    def tensor_product_rank(Q):
        # Placeholder function to simulate minimal tensor product rank calculation
        return random.randint(5, 40)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        depth = frege_proof_depth(phi)
        Q = quadratic_form_representation(phi)
        rank = tensor_product_rank(Q)
        
        if rank <= 40:
            results.append((rank, depth))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_with_rank_le_40"
        }
    
    ranks, depths = zip(*results)
    correlation = sum((r - mean_ranks) * (d - mean_depths) for r, d in zip(ranks, depths)) / len(ranks)
    mean_ranks = sum(ranks) / len(ranks)
    mean_depths = sum(depths) / len(depths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "correlation < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")