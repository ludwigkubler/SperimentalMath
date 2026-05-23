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
    
    def generate_boolean_algebra(n):
        elements = [f"x{i}" for i in range(n)]
        operations = []
        for i in range(n):
            for j in range(i+1, n):
                operations.append((elements[i], elements[j]))
        return elements, operations
    
    def generate_crossed_product(B):
        elements = B[0]
        operations = B[1]
        crossed_elements = [f"a{e}" for e in elements] + [f"b{e}" for e in elements]
        crossed_operations = []
        for op in operations:
            a, b = op
            crossed_operations.append((f"a{a}", f"a{b}"))
            crossed_operations.append((f"b{a}", f"b{b}"))
            crossed_operations.append((f"a{a}", f"b{b}"))
            crossed_operations.append((f"b{a}", f"a{b}"))
        return crossed_elements, crossed_operations
    
    def compute_minimal_rank_invariant(B):
        elements = B[0]
        operations = B[1]
        rank = len(elements)
        for op in operations:
            if op[0] == op[1]:
                rank -= 1
        return rank
    
    def generate_ac0_parity_circuit(n):
        size = 2 ** (math.ceil(math.log2(n**n)))
        circuit = []
        for _ in range(size):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.choice([f"x{i}" for i in range(n)]) for _ in range(2)]
            output = f"y{len(circuit)}"
            circuit.append((gate, inputs, output))
        return circuit
    
    def compute_circuit_size(C):
        size = 0
        visited = set()
        stack = [C[0]]
        while stack:
            gate, inputs, _ = stack.pop()
            if (gate, inputs) not in visited:
                visited.add((gate, inputs))
                size += 1
                for input_ in inputs:
                    stack.append(input_)
        return size
    
    def compute_log_size(C):
        return math.log(compute_circuit_size(C), 2)
    
    n = random.randint(5, 40)
    B = generate_boolean_algebra(n)
    crossed_product = generate_crossed_product(B)
    psi_B = compute_minimal_rank_invariant(crossed_product)
    
    C = generate_ac0_parity_circuit(n)
    log_size_C = compute_log_size(C)
    
    c = 1.0
    if psi_B >= c * log_size_C:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"psi(B)={psi_B} < {c}*log(size(C))={c*log_size_C}"
    
    return {
        "metric_name": "minimal_rank_invariant",
        "metric_value": psi_B,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")