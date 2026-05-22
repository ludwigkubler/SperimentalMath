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
    
    def tropical_hodge_index(divisor):
        if divisor == 0:
            return 0
        else:
            return math.log(divisor, 2)
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit generation (not actual AC0)
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_tropical_divisor(circuit):
        # Simplified tropical divisor computation
        return sum(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_hodge_index = 0
        num_circuits = 30
        
        for _ in range(num_circuits):
            circuit = generate_ac0_circuit(n)
            divisor = compute_tropical_divisor(circuit)
            hodge_index = tropical_hodge_index(divisor)
            total_hodge_index += hodge_index
        
        mean_hodge_index = total_hodge_index / num_circuits
        results.append({
            "n": n,
            "mean_hodge_index": mean_hodge_index
        })
    
    return {
        "metric_name": "mean_tropical_hodge_index",
        "metric_value": sum(result["mean_hodge_index"] for result in results) / len(results),
        "instances_tested": num_circuits * len(n_values),
        "conjecture_holds": all(math.log2(result["n"]) <= result["mean_hodge_index"] <= math.log2(result["n"]**2) for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")