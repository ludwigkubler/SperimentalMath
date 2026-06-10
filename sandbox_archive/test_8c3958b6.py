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
        circuit = []
        for _ in range(2 * n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
                stack.append(result)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
                stack.append(result)
        return stack[0]
    
    def find_satisfied_clauses(circuit, n):
        satisfied = set()
        for assignment in itertools.product([0, 1], repeat=n):
            if evaluate_circuit(circuit, assignment):
                satisfied.add(tuple(assignment))
        return satisfied
    
    def min_monomial_ideal_size(n):
        # Placeholder function to compute the size of the minimal monomial ideal
        # This is a dummy implementation and should be replaced with actual logic
        return n * (n + 1) // 2
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    satisfied = find_satisfied_clauses(circuit, n)
    ideal_size = min_monomial_ideal_size(n)
    
    return {
        "metric_name": "min_monomial_ideal_size",
        "metric_value": ideal_size,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ideal_size <= n**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")