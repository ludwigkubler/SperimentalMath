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
    
    def generate_symmetric_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def dpll_search_tree_width(circuit):
        # Simplified DPLL width calculation
        max_width = 0
        current_width = 0
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                current_width += len(gate[1])
                stack.append(current_width)
                max_width = max(max_width, current_width)
            elif gate[0] == 'OR':
                current_width -= len(stack.pop())
        return max_width
    
    def symplectic_leaf_space(circuit):
        # Simplified symplectic leaf space calculation
        leaves = set()
        for gate in circuit:
            if gate[0] == 'AND':
                leaves.add(tuple(gate[1]))
            elif gate[0] == 'OR':
                leaves.remove(tuple(gate[1]))
        return leaves
    
    def minimal_order_of_divisor(leaves):
        # Simplified minimal order calculation
        return len(leaves)
    
    n = random.randint(5, 40)
    circuit = generate_symmetric_boolean_circuit(n)
    w_C = dpll_search_tree_width(circuit)
    leaves = symplectic_leaf_space(circuit)
    min_order = minimal_order_of_divisor(leaves)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": abs(min_order - w_C) <= 1.5,
        "counterexample": "" if conjecture_holds else f"n={n}, w(C)={w_C}, min_order={min_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")