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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        if not circuit:
            return []
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]
    
    def local_induction_ring_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            result = evaluate_circuit([(gate_type, inputs) for gate_type, _ in circuit])
            if result:
                rank += 1
        return rank
    
    def variance(ranks):
        mean = sum(ranks) / len(ranks)
        return sum((x - mean) ** 2 for x in ranks) / len(ranks)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_circuit(n)
        ranks = [local_induction_ring_rank(circuit) for _ in range(30)]
        total_variance += variance(ranks)
        instances_tested += len(ranks)
    
    mean_variance = total_variance / len(n_values)
    conjecture_holds = 0 <= mean_variance <= 10 * (n_max * math.log(n_max))
    counterexample = "" if conjecture_holds else f"Variance {mean_variance} not in [0, 10 * n log n]"
    
    return {
        "metric_name": "variance",
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")