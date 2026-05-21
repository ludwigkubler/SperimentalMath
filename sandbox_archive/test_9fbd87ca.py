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

def generate_monotone_circuit(n):
    gate_type = random.randint(1, n)
    inputs = [random.randint(0, n-1) for _ in range(gate_type)]
    outputs = [random.randint(0, n-1) for _ in range(gate_type)]
    circuit = []
    for i in range(gate_type):
        gate = (inputs[i], outputs[i])
        circuit.append(gate)
    return circuit

def compute_coxeter_group_rank(circuit):
    # Construct a simple Coxeter group based on the circuit
    # This is a placeholder implementation; replace with actual computation
    rank = len(set(input for input, _ in circuit))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_circuit(n)
        rank = compute_coxeter_group_rank(circuit)
        expected_rank = math.log2(n)
        
        if rank < expected_rank:
            return {
                "metric_name": "Coxeter Group Rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank} < log2({n}) = {expected_rank}"
            }
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.log2(n_values[0])) / len(results)
    
    if all(r >= math.log2(n_values[0]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < math.log2(n_values[0]) for r in results):
        first_failing = next(i for i, r in enumerate(results) if r < math.log2(n_values[0]))
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[first_failing]}, rank<{math.log2(n_values[first_failing])}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")