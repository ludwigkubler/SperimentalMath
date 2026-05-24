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
    
    def generate_random_qubit_system(n):
        # Generate a random n-qubit system using quantum circuits (simplified)
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quadratic_entanglement_pattern(qubits):
        # Compute the quadratic entanglement pattern (simplified)
        n = int(math.log2(len(qubits)))
        pattern = [[qubits[i] * qubits[j] for j in range(n)] for i in range(n)]
        return sum(sum(row) for row in pattern)
    
    def construct_bp_readtwice_circuit(pattern):
        # Construct the corresponding BP_ReadTwice circuit (simplified)
        n = int(math.log2(len(pattern)))
        depth = 0
        for _ in range(n):
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    qubits = generate_random_qubit_system(n)
    pattern = compute_quadratic_entanglement_pattern(qubits)
    depth = construct_bp_readtwice_circuit(pattern)
    
    if depth == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    minimal_rank = pattern
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": None,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] is None for r in results):
        RESULT = "INCONCLUSIVE mapping_undefined"
    else:
        supported_count = sum(1 for r in results if r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.7 or any(r["minimal_rank"] <= 5 * r["depth"] for r in results):
            RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}"
        else:
            first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
            RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)