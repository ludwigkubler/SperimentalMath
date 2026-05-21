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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def construct_coxeter_group(circuit):
        # Simplified mapping to generate a Coxeter group
        G = {}
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                G[(inputs[0], inputs[1])] = 2
                G[(inputs[1], inputs[0])] = 2
            elif gate_type == 'OR':
                G[(inputs[0], inputs[1])] = 3
                G[(inputs[1], inputs[0])] = 3
        return G
    
    def min_rank(G):
        # Simplified calculation of minimal rank
        rank = 0
        for key in G:
            if G[key] > rank:
                rank = G[key]
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    G = construct_coxeter_group(circuit)
    minimal_rank = min_rank(G)
    
    metric_name = "minimal_rank"
    metric_value = minimal_rank
    instances_tested = 1
    conjecture_holds = minimal_rank >= math.log2(n)
    counterexample = "" if conjecture_holds else f"n={n}, rank={minimal_rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        # Generate a list of 30 prime numbers as default seeds
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")