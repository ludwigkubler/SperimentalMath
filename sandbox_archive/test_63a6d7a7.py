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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(phi):
        # Placeholder function to simulate Frege proof depth
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)
    
    def quadratic_form_representation(phi):
        n = int(math.log2(len(phi)))
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = sum(phi[k] * phi[k + 1] for k in range(2**n)) / (2**(n+1))
                Q[j][i] = Q[i][j]
        return Q
    
    def tensor_product_rank(Q):
        # Placeholder function to simulate minimal tensor product rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 50)
    
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
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_instances_with_rank_le_40"
        }
    
    correlation = sum((x - mean_x) * (y - mean_y) for x, y in results) / len(results)
    mean_x = sum(x for x, _ in results) / len(results)
    mean_y = sum(y for _, y in results) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_missing_metric_value")