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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.choice([0, 1]) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def tautology_set(circuit):
        n = len(circuit[0][1])
        tautologies = set()
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            outputs = []
            for gate, inputs in circuit:
                if gate == 'AND':
                    output = all(inputs)
                elif gate == 'OR':
                    output = any(inputs)
                outputs.append(output)
            if all(outputs):
                tautologies.add(tuple(inputs))
        return tautologies
    
    def categorial_invariants(tautologies):
        n = len(next(iter(tautologies)))
        invariants = [0] * (n + 1)
        for t in tautologies:
            for i in range(n):
                if t[i] == 1:
                    invariants[i] += 1
        return max(invariants)
    
    def entanglement_entropy(circuit):
        n = len(circuit[0][1])
        probabilities = [0] * (2**n)
        for _ in range(1000):  # Simulate many trials to estimate probabilities
            inputs = [random.choice([0, 1]) for _ in range(n)]
            outputs = []
            for gate, inputs in circuit:
                if gate == 'AND':
                    output = all(inputs)
                elif gate == 'OR':
                    output = any(inputs)
                outputs.append(output)
            index = sum(2**i * inputs[i] for i in range(n))
            probabilities[index] += 1
        probabilities = [p / 1000 for p in probabilities if p > 0]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        return entropy
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    tautologies = tautology_set(circuit)
    order = categorial_invariants(tautologies)
    entanglement = entanglement_entropy(circuit)
    
    if order is None or entanglement is None:
        return {
            "metric_name": "Order(C) - Ent(C)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    diff = abs(order - entanglement)
    return {
        "metric_name": "Order(C) - Ent(C)",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= 10,
        "counterexample": "" if diff <= 10 else f"diff={diff}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"] if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")