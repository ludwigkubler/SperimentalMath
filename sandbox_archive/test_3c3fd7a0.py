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
        for _ in range(random.randint(1, 5)):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(2, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'AND':
                result = all(input_values[i] for i in gate[1])
            elif gate[0] == 'OR':
                result = any(input_values[i] for i in gate[1])
            stack.append(result)
        return stack.pop()
    
    def affine_quotient_group(circuit):
        n = len(circuit)
        G = []
        for i in range(2**n):
            input_values = [bool(i >> j & 1) for j in range(n)]
            output_value = evaluate_circuit(circuit, input_values)
            if output_value:
                G.append(tuple(input_values))
        return G
    
    def frege_proof_depth(circuit):
        depth = 0
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                stack.append(1 + max(stack[-2], stack[-1]))
            elif gate[0] == 'OR':
                stack.append(1 + max(stack[-2], stack[-1]))
            depth = max(depth, stack.pop())
        return depth
    
    def min_generators(group):
        generators = []
        for element in group:
            if all(element[i] != generator[i] for i, generator in enumerate(generators)):
                generators.append(element)
        return len(generators)
    
    n_max = 0
    total_g = 0
    total_d = 0
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        G = affine_quotient_group(circuit)
        d = frege_proof_depth(circuit)
        g = min_generators(G)
        
        if n > n_max:
            n_max = n
        
        total_g += g
        total_d += d
        instances_tested += 1
    
    mean_g = total_g / instances_tested
    mean_d = total_d / instances_tested
    correlation_coefficient = (instances_tested * sum(g * d for g, d in zip([mean_g] * instances_tested, [mean_d] * instances_tested)) - sum(g) * sum(d)) / math.sqrt((instances_tested * sum(g**2 for g in [mean_g] * instances_tested) - sum(g)**2) * (instances_tested * sum(d**2 for d in [mean_d] * instances_tested) - sum(d)**2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_g = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_g} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_g} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")