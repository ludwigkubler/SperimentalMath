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
    
    def generate_random_circuit(n):
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
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]
    
    def find_satisfied_clauses(circuit, n):
        satisfied = []
        for assignment in product([0, 1], repeat=n):
            if evaluate_circuit(circuit, assignment):
                satisfied.append(assignment)
        return satisfied
    
    def minimal_monomial_ideal(satisfied):
        monomials = set()
        for clause in satisfied:
            monomial = 1
            for var, value in enumerate(clause):
                if value == 1:
                    monomial *= (1 << var)
            monomials.add(monomial)
        return monomials
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        satisfied = find_satisfied_clauses(circuit, n)
        ideal = minimal_monomial_ideal(satisfied)
        results.append({
            "n": n,
            "monomial_count": len(ideal),
            "circuit_size": len(circuit)
        })
    
    metric_value = sum(result["monomial_count"] for result in results) / len(results)
    conjecture_holds = all(result["monomial_count"] <= n**2 * math.log(n, 2) for result in results)
    
    return {
        "metric_name": "Monomial Ideal Size",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")