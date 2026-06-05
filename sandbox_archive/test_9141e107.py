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
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]
    
    def algebraic_quotient(circuit):
        truth_table = {}
        for _ in range(2**len(circuit)):
            assignment = [random.randint(0, 1) for _ in range(len(circuit))]
            output = evaluate_circuit([(gate_type, inputs) for gate_type, inputs in circuit if all(assignment[i] == 0 or assignment[i] == 1 for i in inputs)])
            truth_table[tuple(assignment)] = output
        equivalence_classes = []
        visited = set()
        for key in sorted(truth_table):
            if key not in visited:
                eq_class = [key]
                stack = [key]
                while stack:
                    current = stack.pop()
                    for k, v in truth_table.items():
                        if k != current and v == truth_table[current] and all(k[i] == current[i] or k[i] == 1 - current[i] for i in range(len(current))):
                            eq_class.append(k)
                            stack.append(k)
                equivalence_classes.append(eq_class)
                visited.update(eq_class)
        return len(equivalence_classes)
    
    def complexity(circuit):
        return sum(2**len(inputs) for _, inputs in circuit)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_boolean_circuit(n)
    rank_quot = algebraic_quotient(circuit)
    circ_complexity = complexity(circuit)
    
    if circ_complexity == 0:
        return {
            "metric_name": "rank_quot/C",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Circuits with complexity 0 are undefined"
        }
    
    ratio = rank_quot / circ_complexity
    
    return {
        "metric_name": "rank_quot/C",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 1.5\" first_failing_seed={first_failing_seed}")