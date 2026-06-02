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

def generate_boolean_circuit(n, w):
    if n == 1:
        return ['0', '1']
    elif n == 2:
        inputs = generate_boolean_circuit(1, w//2)
        return [f'NOT {i}' for i in inputs] + [f'AND {inputs[0]} {inputs[1]}'] + [f'OR {inputs[0]} {inputs[1]}']
    else:
        inputs = generate_boolean_circuit(n-1, w//2)
        if not inputs:
            raise ValueError("Cannot choose from an empty sequence")
        return [f'NOT {i}' for i in inputs] + [f'AND {inputs[0]} {inputs[-1]}'] + [f'OR {inputs[0]} {inputs[-1]}']

def calculate_monomial_basis(circuit):
    basis = set()
    for expr in circuit:
        if 'NOT' not in expr and 'AND' not in expr and 'OR' not in expr:
            basis.add(expr)
    return basis

def calculate_noncommutative_yang_baxter_equation(monomial_basis):
    n = len(monomial_basis)
    rank = 0
    for i in range(n):
        for j in range(i+1, n):
            if monomial_basis[i] != monomial_basis[j]:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            w = random.randint(1, n)
            try:
                circuit = generate_boolean_circuit(n, w)
                basis = calculate_monomial_basis(circuit)
                rank = calculate_noncommutative_yang_baxter_equation(basis)
                results.append((n, w, rank))
            except Exception as e:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": None,
                    "instances_tested": 0,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank = min(rank for _, _, rank in results)
    max_w = max(w for _, w, _ in results)
    instances_tested = len(results)
    n_max = 40
    conjecture_holds = all(rank <= w**2 for _, w, rank in results)
    counterexample = "" if conjecture_holds else "minimal_rank > w^2"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")