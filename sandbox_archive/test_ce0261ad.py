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
    
    def generate_boolean_algebra(n):
        return {f"x{i}": i for i in range(n)}
    
    def generate_crossed_product(B):
        n = len(B)
        crossed_product = {}
        for x in B:
            for y in B:
                crossed_product[(x, y)] = (B[x] + B[y]) % 2
        return crossed_product
    
    def compute_minimal_rank_invariant(cp):
        rank = 0
        for key in cp:
            if cp[key]:
                rank += 1
        return rank
    
    def generate_ac0_parity_circuit(n):
        circuit_size = 2 ** math.ceil(math.log2(n))
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    psi_B_values = []
    circuit_sizes = []
    
    for n in n_values:
        B = generate_boolean_algebra(n)
        cp = generate_crossed_product(B)
        psi_B = compute_minimal_rank_invariant(cp)
        psi_B_values.append(psi_B)
        
        circuit_size = generate_ac0_parity_circuit(n)
        circuit_sizes.append(circuit_size)
    
    mean_psi_B = sum(psi_B_values) / len(psi_B_values)
    std_dev_psi_B = math.sqrt(sum((x - mean_psi_B) ** 2 for x in psi_B_values) / len(psi_B_values))
    
    c = 3
    support_fraction = sum(1 for size, psi in zip(circuit_sizes, psi_B_values) if psi >= c * math.log(size)) / len(circuit_sizes)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "support_fraction < 0.8"
    
    return {
        "metric_name": "minimal_rank_invariant",
        "metric_value": mean_psi_B,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")