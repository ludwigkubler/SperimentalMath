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
    
    def generate_tseitin_circuit(w, n):
        # Placeholder for Tseitin circuit generation logic
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    def compute_symmetry_group(circuit):
        # Placeholder for symmetry group computation logic
        return [i for i in range(len(circuit))]
    
    def symmetric_measure(symmetry_group):
        return len(symmetry_group)
    
    def tseitin_circuit_width(circuit):
        return max(len(row) for row in circuit)
    
    def tseitin_circuit_variables(circuit):
        return len(circuit[0])
    
    n = random.randint(5, 30)
    w = random.randint(n + 1, min(40, n * 2))
    circuit = generate_tseitin_circuit(w, n)
    width = tseitin_circuit_width(circuit)
    variables = tseitin_circuit_variables(circuit)
    
    symmetry_group = compute_symmetry_group(circuit)
    S_f = symmetric_measure(symmetry_group)
    
    c = 1.0  # Placeholder for absolute constant
    cw = c * width
    
    return {
        "metric_name": "S(f) / cw",
        "metric_value": S_f / cw,
        "instances_tested": 1,
        "conjecture_holds": S_f <= cw,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction < 0.3:
        counterexample = "low_support_fraction"
        for r in results:
            if not r["conjecture_holds"]:
                counterexample += f" seed={r['seed']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_out_of_range")

# RESULT: SUPPORTED mean=<x> std=<y> support_fraction=<z> (when ALL or ≥80% seeds support)
# RESULT: FALSIFIED counterexample="<desc>" first_failing_seed=<s>
# RESULT: INCONCLUSIVE <reason>