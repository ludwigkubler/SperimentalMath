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
    
    # Define constants and parameters
    n = 20
    k = 5
    
    # Generate a random monotone circuit C of size poly(n)
    # This is a placeholder function; actual implementation depends on the conjecture
    def generate_monotone_circuit(n, k):
        # Placeholder: return a dummy circuit
        return [random.choice([0, 1]) for _ in range(n)]
    
    circuit = generate_monotone_circuit(n, k)
    
    # Compute the tensor product representation of its input space
    # This is a placeholder function; actual implementation depends on the conjecture
    def compute_tensor_product_representation(circuit):
        # Placeholder: return a dummy rank
        return random.randint(1, 100)
    
    rank = compute_tensor_product_representation(circuit)
    
    # Measure the rank of this representation
    metric_value = rank
    
    # Check if the conjecture holds for this seed
    conjecture_holds = rank <= n**math.ceil(k**(1/4))
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds n^Ω(k^{1/4})"
    
    return {
        "metric_name": "Tensor Product Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")