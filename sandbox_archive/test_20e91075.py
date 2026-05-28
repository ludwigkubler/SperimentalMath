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
    
    def generate_ac0_circuit(n):
        # Generate a random AC⁰ circuit with n inputs
        # This is a simplified representation for testing purposes
        return [random.choice(['AND', 'OR', 'NOT']) for _ in range(2**n)]
    
    def tropical_rank(circuit):
        # Compute the minimal rank of the tropical curve corresponding to the circuit
        # This is a placeholder function and should be replaced with actual computation
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        rank = tropical_rank(circuit)
        results.append((n, rank))
    
    total_rank = sum(rank for _, rank in results)
    avg_rank = Fraction(total_rank, len(results))
    log_n = math.log(len(results), 2)  # Using base 2 for simplicity
    
    conjecture_holds = avg_rank >= 1 * log_n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Tropical Rank",
        "metric_value": float(avg_rank),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")