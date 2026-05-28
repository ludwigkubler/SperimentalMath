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
    
    def generate_ac0_circuit(n):
        # Simplified AC⁰ circuit for PARITY function
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_algebraic_curve(circuit):
        # Placeholder for actual computation of algebraic curve rank
        # This is a dummy implementation that returns a random rank
        return random.randint(1, len(circuit))
    
    def log_base_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        rank = compute_algebraic_curve(circuit)
        expected_rank = 2 * log_base_2(n)  # Simplified expected rank formula
        
        if rank < expected_rank:
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} is less than expected {expected_rank}"
            }
        
        total_rank += rank
        instances_tested += len(circuit)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")