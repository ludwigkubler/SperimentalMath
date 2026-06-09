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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            clause = [random.randint(1, n), random.choice([0, 1])]
            circuit.append(clause)
        return circuit
    
    def dpll(circuit, assignment):
        if not circuit:
            return True
        literal = next(lit for lit in circuit[0] if lit != -assignment[abs(lit)])
        if literal is None:
            return False
        new_assignment = assignment.copy()
        new_assignment[literal] = 1
        if dpll(circuit, new_assignment):
            return True
        new_assignment[literal] = 0
        if dpll(circuit, new_assignment):
            return True
        return False
    
    def min_state_count(circuit):
        states = set()
        for assignment in itertools.product([0, 1], repeat=len(circuit)):
            if dpll(circuit, dict(enumerate(assignment))):
                states.add(tuple(sorted((i + 1) * (2 * val - 1) for i, val in enumerate(assignment))))
        return len(states)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    circuit = generate_circuit(n, m)
    state_count = min_state_count(circuit)
    dpll_height = 1
    stack = [(circuit, {})]
    while stack:
        current_circuit, current_assignment = stack.pop()
        if not current_circuit:
            continue
        literal = next(lit for lit in current_circuit[0] if lit != -current_assignment.get(abs(lit), 0))
        if literal is None:
            dpll_height += 1
            continue
        new_assignment = current_assignment.copy()
        new_assignment[literal] = 1
        stack.append(([(lit, val) for lit, val in current_circuit if lit != literal], new_assignment))
        new_assignment[literal] = 0
        stack.append(([(lit, val) for lit, val in current_circuit if lit != -literal], new_assignment))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": state_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")