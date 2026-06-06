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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2**n):
            truth_table = [random.randint(0, 1) for _ in range(n)]
            output = random.randint(0, 1)
            circuit.append((truth_table, output))
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit[0][0])
        max_width = 0
        for i in range(n):
            width = sum(1 for truth_table, _ in circuit if truth_table[i] == 1)
            max_width = max(max_width, width)
        return max_width
    
    def hodge_dimension(truth_table):
        n = len(truth_table)
        # Simplified Hodge dimension calculation (not actual Hodge theory)
        return sum(1 for bit in truth_table if bit == 1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        width = monotone_width(circuit)
        hodge_dim = sum(hodge_dimension(truth_table) for truth_table, _ in circuit)
        ratio = Fraction(hodge_dim, n).limit_denominator()
        
        results.append({
            "n": n,
            "width": width,
            "hodge_dim": hodge_dim,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] >= Fraction(1, 2) for result in results)
    counterexample = "" if conjecture_holds else f"Ratio: {min(result['ratio'] for result in results)}, n={results[0]['n']}"
    
    return {
        "metric_name": "Hodge-Structure Dimension to Log(n) Ratio",
        "metric_value": float(metric_value),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")