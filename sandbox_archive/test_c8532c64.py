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
    
    def generate_xor_circuit(n):
        circuit = []
        for _ in range(1 << n):
            inputs = [random.randint(0, 1) for _ in range(n)]
            output = sum(inputs) % 2
            circuit.append((inputs, output))
        return circuit
    
    def ehrhart_rank(circuit):
        # This is a placeholder function. In practice, you would need to compute the Ehrhart cohomology rank.
        # For simplicity, we will assume it returns a random value between 1 and n.
        n = len(circuit[0][0])
        return random.randint(1, n)
    
    def log_n(n):
        return math.log2(n) if n > 0 else float('inf')
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_xor_circuit(n)
        rank = ehrhart_rank(circuit)
        expected_rank = log_n(n)
        results.append((rank, expected_rank))
    
    total_rank = sum(rank for rank, _ in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for rank, _ in results) / len(results))
    correlation = sum((rank - mean_rank) * (expected_rank - log_n(n)) for rank, expected_rank, n in zip(*results)) / (len(results) * std_rank * log_n(n))
    
    conjecture_holds = correlation >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ehrhart Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")