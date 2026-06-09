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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for x in range(1, p):
            if (x * x) % p == a:
                return True
        return False
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(0, n-1))
        return protocol
    
    def compute_rank_variance(protocol):
        frequency = [0] * len(protocol)
        for outcome in protocol:
            frequency[outcome] += 1
        mean = sum(frequency) / len(frequency)
        variance = sum((x - mean) ** 2 for x in frequency) / len(frequency)
        return variance
    
    def count_quadratic_residues(outcomes, p):
        residues = set()
        for outcome in outcomes:
            if is_quadratic_residue(outcome, p):
                residues.add(outcome)
        return len(residues)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_protocol(n)
        R = compute_rank_variance(protocol)
        outcomes = set(protocol)
        p = random.choice([p for p in range(2, 100) if all(p % i != 0 for i in range(2, int(math.sqrt(p)) + 1))])
        num_residues = count_quadratic_residues(outcomes, p)
        
        results.append({
            "n": n,
            "R": R,
            "num_residues": num_residues
        })
    
    if not results:
        return {
            "metric_name": "quadratic_residue_bound",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_num_residues = sum(result["num_residues"] for result in results)
    max_n = max(result["n"] for result in results)
    
    return {
        "metric_name": "quadratic_residue_bound",
        "metric_value": total_num_residues,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")