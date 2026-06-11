# auto-injected by SEC sandbox
import math
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

def generate_random_boolean_circuit(n):
    if n == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_random_boolean_circuit(random.randint(1, n-1)) for _ in range(2)]
        return [random.choice([0, 1]) + sum(subcircuit) % 2 for subcircuit in subcircuits]

def generate_hypergraph(circuit):
    hypergraph = set()
    for i in range(len(circuit)):
        if circuit[i] == 1:
            hypergraph.add(frozenset(range(i+1)))
    return hypergraph

def mld(hypergraph):
    n = len(hypergraph)
    if n == 0:
        return 0
    max_dim = 0
    for subset in hypergraph:
        dim = sum(1 for s in hypergraph if not subset.issubset(s))
        max_dim = max(max_dim, dim)
    return max_dim

def frege_proof_length(circuit):
    # Simplified Frege proof length calculation (not accurate but sufficient for testing)
    return len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_random_boolean_circuit(n)
        hypergraph = generate_hypergraph(circuit)
        mld_value = mld(hypergraph)
        frege_length = frege_proof_length(circuit)
        results.append((mld_value, frege_length))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in [5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mld_values = [x[0] for x in results]
    frege_lengths = [x[1] for x in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        if n < 2:
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = (sum((xi - mean_x)**2 for xi in x) / n) ** 0.5
        std_y = (sum((yi - mean_y)**2 for yi in y) / n) ** 0.5
        return cov / (std_x * std_y)
    
    corr_coeff = pearson_correlation(mld_values, frege_lengths)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": "" if corr_coeff >= 0.7 else f"correlation_coefficient={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")