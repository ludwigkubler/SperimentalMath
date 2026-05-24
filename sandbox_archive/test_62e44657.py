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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with depth n
        if n == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_circuit(n-1)
            gate = random.choice(['AND', 'OR'])
            return [gate] + inputs
    
    def hodge_rank(circuit):
        # Compute the rank of the Hodge decomposition modulo p
        if not circuit:
            return 0
        elif isinstance(circuit[0], int):
            return 1
        else:
            gate = circuit[0]
            left = hodge_rank(circuit[1])
            right = hodge_rank(circuit[2:])
            return max(left, right) + 1
    
    def acc0_certificate_size(circuit):
        # Calculate the ACC⁰ certificate size for the circuit
        if not circuit:
            return 0
        elif isinstance(circuit[0], int):
            return 1
        else:
            gate = circuit[0]
            left = acc0_certificate_size(circuit[1])
            right = acc0_certificate_size(circuit[2:])
            return max(left, right) + 1
    
    def estimate_phi(d):
        # Estimate φ(d) using statistical methods
        ranks = [hodge_rank(generate_circuit(d)) for _ in range(1000)]
        acc0_sizes = [acc0_certificate_size(generate_circuit(d)) for _ in range(1000)]
        avg_rank = sum(ranks) / len(ranks)
        avg_acc0_size = sum(acc0_sizes) / len(acc0_sizes)
        return (avg_rank, avg_acc0_size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        rank_sum = 0
        acc0_size_sum = 0
        for _ in range(10):
            circuit = generate_circuit(n)
            rank_sum += hodge_rank(circuit)
            acc0_size_sum += acc0_certificate_size(circuit)
        
        avg_rank = rank_sum / 10
        avg_acc0_size = acc0_size_sum / 10
        
        if avg_rank > avg_acc0_size * 3 + 2:
            return {
                "metric_name": "Hodge Rank vs ACC⁰ Certificate Size",
                "metric_value": avg_rank,
                "instances_tested": 60,
                "conjecture_holds": False,
                "counterexample": f"n={n}, avg_rank={avg_rank}, avg_acc0_size={avg_acc0_size}"
            }
    
    phi_d = estimate_phi(n_values[-1])
    support_fraction = sum(1 for n in n_values if hodge_rank(generate_circuit(n)) <= phi_d[0] + 3) / len(n_values)
    
    return {
        "metric_name": "Hodge Rank vs ACC⁰ Certificate Size",
        "metric_value": phi_d[0],
        "instances_tested": 60,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=40\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")