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

def generate_random_circuit(n: int) -> list:
    """Generate a random n-input Boolean circuit."""
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_barycentric_coordinates(circuit: list) -> set:
    """Compute the minimal set of barycentric coordinates for a given circuit."""
    n = int(math.log2(len(circuit)))
    if 2**n != len(circuit):
        raise ValueError("Circuit length must be a power of 2")
    
    def is_barycentric(coord, circuit):
        """Check if the given coordinate represents the circuit."""
        for i in range(n):
            if coord[i] == 1:
                if circuit[2**i] != 1:
                    return False
            else:
                if circuit[2**i + 1] != 0:
                    return False
        return True
    
    barycentric_coords = set()
    for i in range(2**n):
        if is_barycentric(bin(i)[2:].zfill(n), circuit):
            barycentric_coords.add(i)
    
    return barycentric_coords

def compute_entanglement_complexity(circuit: list) -> int:
    """Compute the entanglement complexity of a given circuit."""
    n = int(math.log2(len(circuit)))
    if 2**n != len(circuit):
        raise ValueError("Circuit length must be a power of 2")
    
    # Simplified heuristic for entanglement complexity
    return sum(1 for i in range(n) if circuit[2**i] == 1 and circuit[2**i + 1] == 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        bc_set = compute_barycentric_coordinates(circuit)
        ec = compute_entanglement_complexity(circuit)
        
        if len(bc_set) == 0 or ec == 0:
            continue
        
        ratio = len(bc_set) / ec
        results.append((n, len(bc_set), ec, ratio))
    
    if not results:
        return {
            "metric_name": "Ratio of BC to EC",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    metric_value = sum(ratio for _, _, _, ratio in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _, _, _ in results)
    
    conjecture_holds = all(0.9 <= ratio <= 1.1 for _, _, _, ratio in results)
    counterexample = "" if conjecture_holds else "Ratio out of bounds"
    
    return {
        "metric_name": "Ratio of BC to EC",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No valid trials")
        sys.exit()
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 1) > 0.2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 1) > 0.2)
        print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason for failure unknown")