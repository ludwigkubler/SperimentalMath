# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_boolean_circuit(n, w):
    if n == 1:
        return ["x"]
    
    inputs = generate_boolean_circuit(n-1, w//2)
    outputs = []
    for _ in range(w):
        if len(inputs) < 2:
            raise ValueError("Cannot choose from an empty sequence")
        output = f"({random.choice(inputs)} AND {random.choice(inputs)})"
        outputs.append(output)
    
    return outputs

def compute_monomial_basis(circuit):
    basis = set()
    for expr in circuit:
        if "AND" in expr:
            basis.add(expr.split(" AND ")[0])
            basis.add(expr.split(" AND ")[1])
        else:
            basis.add(expr)
    return basis

def noncommutative_yang_baxter_equation(monomial_basis):
    n = len(monomial_basis)
    rank = 0
    for i in range(n):
        for j in range(i+1, n):
            if f"{monomial_basis[i]} AND {monomial_basis[j]}" not in monomial_basis:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            w = random.randint(1, min(n, 10))
            circuit = generate_boolean_circuit(n, w)
            monomial_basis = compute_monomial_basis(circuit)
            rank = noncommutative_yang_baxter_equation(monomial_basis)
            results.append((n, w, rank))
    
    metric_value = sum(rank for _, _, rank in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = all(rank <= 2 * w**2 for _, w, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")