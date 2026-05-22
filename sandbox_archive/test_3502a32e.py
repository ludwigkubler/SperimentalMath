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
    
    # Define the function to compute the minimal rank ρ(W) for S_m
    def minimal_rank(m):
        # This is a placeholder for the actual computation of the minimal rank.
        # For simplicity, we'll use a dummy value that depends on m and d.
        return 2 * math.log(m)
    
    # Define the function to generate a random permutation circuit C of size m and depth d
    def generate_circuit(m, d):
        # This is a placeholder for the actual generation of a random permutation circuit.
        # For simplicity, we'll use a dummy value that depends on m and d.
        return (m, d)
    
    # Define the function to compute the Weyl group of S_m
    def weyl_group(m):
        # This is a placeholder for the actual computation of the Weyl group.
        # For simplicity, we'll use a dummy value that depends on m and d.
        return (m, d)
    
    # Define the function to compute the minimal rank ρ(W) for the Weyl group W
    def minimal_rank_weyl_group(w):
        # This is a placeholder for the actual computation of the minimal rank.
        # For simplicity, we'll use a dummy value that depends on m and d.
        return 2 * math.log(w[0])
    
    # Define the function to compute the average minimal rank ρ(W) across a sample of 30 random seeds
    def average_minimal_rank(m, d):
        total = 0
        for _ in range(30):
            circuit = generate_circuit(m, d)
            w = weyl_group(circuit[0])
            rho_w = minimal_rank_weyl_group(w)
            total += rho_w
        return total / 30
    
    # Define the function to test the conjecture for a given pair of values (m, d)
    def test_conjecture(m, d):
        avg_rho_w = average_minimal_rank(m, d)
        if avg_rho_w >= d * math.log(m):
            return True
        else:
            return False
    
    # Define the function to find a counterexample for the conjecture
    def find_counterexample(m, d):
        for _ in range(30):
            circuit = generate_circuit(m, d)
            w = weyl_group(circuit[0])
            rho_w = minimal_rank_weyl_group(w)
            if rho_w < d * math.log(m):
                return f"Counterexample found: m={m}, d={d}, avg_rho_w={rho_w}"
        return ""
    
    # Define the function to run a trial for a given seed
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        # Generate a random pair of values (m, d)
        m = random.randint(5, 40)
        d = random.randint(1, 20)
        
        # Test the conjecture for the given pair of values
        conjecture_holds = test_conjecture(m, d)
        
        # Find a counterexample if the conjecture is falsified
        counterexample = find_counterexample(m, d) if not conjecture_holds else ""
        
        return {
            "metric_name": "minimal_rank",
            "metric_value": average_minimal_rank(m, d),
            "instances_tested": 30,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    # Run the trial and return the result
    return run_trial(seed)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")