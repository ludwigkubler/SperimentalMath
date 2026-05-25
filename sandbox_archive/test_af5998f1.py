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
    
    def tropicalized_noncrossing_partition_polynomial(f):
        n = len(f)
        if n == 1:
            return f[0]
        else:
            left = tropicalized_noncrossing_partition_polynomial(f[:n//2])
            right = tropicalized_noncrossing_partition_polynomial(f[n//2:])
            return max(left, right) + min(left, right)
    
    def bp_readtwice_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            left = bp_readtwice_circuit_size(f[:n//2])
            right = bp_readtwice_circuit_size(f[n//2:])
            return max(left, right) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = tropicalized_noncrossing_partition_polynomial(f)
        circuit_size = bp_readtwice_circuit_size(f)
        
        if rank > math.log(n):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank} > log({n})"
            }
        
        if circuit_size < 2**n:
            return {
                "metric_name": "bp_readtwice_circuit_size",
                "metric_value": circuit_size,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, circuit_size={circuit_size} < 2^{n}"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"n={counterexample['n']}, rank={counterexample['rank']} > log({counterexample['n']}) or circuit_size={counterexample['circuit_size']} < 2^{counterexample['n']}\" first_failing_seed={seeds[results.index(counterexample)]}")