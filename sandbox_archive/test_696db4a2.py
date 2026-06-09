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
    
    def generate_circuit(m):
        # Generate a random Boolean circuit for an m-literal clause
        variables = list(range(m))
        gates = []
        for _ in range(2 * m - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(variables, random.randint(1, m))
            gates.append((gate_type, inputs))
        return gates
    
    def evaluate_circuit(circuit, assignment):
        # Evaluate the circuit for a given assignment
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                result = True
                for var in gate[1]:
                    result &= assignment[var]
                stack.append(result)
            elif gate[0] == 'OR':
                result = False
                for var in gate[1]:
                    result |= assignment[var]
                stack.append(result)
        return stack[-1]
    
    def formal_group_representation(circuit):
        # Compute the minimal order of a formal group representation
        n = len(circuit)
        m = 2 ** n
        identity = [0] * n
        elements = [identity]
        for i in range(1, m):
            assignment = [(i >> j) & 1 for j in range(n)]
            result = evaluate_circuit(circuit, assignment)
            if result:
                elements.append(assignment)
        order = len(elements)
        return order
    
    def is_polynomial_relationship(data, c):
        # Check if the relationship between clause size and minimal order is polynomial
        n_values = [len(circuit) for circuit in data]
        orders = [formal_group_representation(circuit) for circuit in data]
        ratios = [order / (n ** c) for n, order in zip(n_values, orders)]
        return all(r <= 1.5 for r in ratios)
    
    data = []
    for m in range(1, 41):
        for _ in range(30):
            circuit = generate_circuit(m)
            data.append(circuit)
    
    c_values = [i / 10 for i in range(1, 11)]
    results = []
    for c in c_values:
        if is_polynomial_relationship(data, c):
            results.append(True)
        else:
            results.append(False)
    
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else f"c={c_values[results.index(False)]}"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": sum(formal_group_representation(circuit) for circuit in data) / len(data),
        "instances_tested": len(data),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"c={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")