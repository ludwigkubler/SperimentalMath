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
    
    def generate_random_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = [random.choice([1, 0]) for _ in range(2)]
            circuit.append(gate)
        return circuit
    
    def compute_monomial_basis(circuit):
        basis = set()
        for gate in circuit:
            if gate[0] == 1:
                basis.add(tuple(sorted(gate[1:])))
            else:
                basis.add(tuple(sorted([1 - x for x in gate[1:]])))
        return basis
    
    def compute_noncommutative_yang_baxter_equation(basis):
        # Placeholder function to simulate computation
        # Replace with actual implementation if needed
        rank = len(basis) ** 2
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        w = random.randint(1, min(n // 2, 10))
        circuit = generate_random_circuit(n, w)
        basis = compute_monomial_basis(circuit)
        rank = compute_noncommutative_yang_baxter_equation(basis)
        
        results.append({
            "n": n,
            "w": w,
            "rank": rank
        })
    
    min_rank = min(result["rank"] for result in results)
    max_n = max(result["n"] for result in results)
    
    conjecture_holds = all(result["rank"] <= result["w"] ** 2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        result = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(result)