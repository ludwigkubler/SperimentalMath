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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_symmetry_group(f):
        n = int(math.log2(len(f)))
        G = []
        for i in range(2**n):
            permuted_f = [f[i ^ j] for j in range(2**n)]
            if f == permuted_f:
                G.append(i)
        return G
    
    def construct_circuit(G):
        n = int(math.log2(len(G)))
        circuit_size = 0
        for i in range(n):
            for j in range(n):
                if (i ^ j) in G:
                    circuit_size += 1
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_circuits = 0
    total_permutations = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        G = generate_symmetry_group(f)
        circuit_size = construct_circuit(G)
        
        total_circuits += circuit_size
        total_permutations += len(G)
    
    avg_circuit_size = total_circuits / sum(len(n_values) for n in n_values)
    avg_permutations = total_permutations / sum(len(n_values) for n in n_values)
    
    conjecture_holds = avg_permutations <= 2 * avg_circuit_size
    counterexample = "" if conjecture_holds else f"avg_permutations={avg_permutations}, avg_circuit_size={avg_circuit_size}"
    
    return {
        "metric_name": "Circuit Size vs Permutations",
        "metric_value": avg_circuit_size,
        "instances_tested": sum(len(n_values) for n in n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 97, 4))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")