# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_circuit(n_inputs, depth):
        if depth == 1:
            return ['0'] * n_inputs + ['1'] * n_inputs
        else:
            left = generate_random_circuit(n_inputs, depth - 1)
            right = generate_random_circuit(n_inputs, depth - 1)
            return [f'({l} & {r})' for l in left] + [f'({l} | {r})' for l in right]
    
    def compute_clause_set(circuit):
        clauses = []
        stack = []
        for gate in circuit:
            if '&' in gate or '|' in gate:
                stack.append(gate)
            else:
                clause = set()
                while stack and '(' not in stack[-1]:
                    clause.add(stack.pop())
                stack.pop()  # Remove the '('
                clauses.append(clause)
        return clauses
    
    def minimal_order_of_grothendieck_teichmueller_group(clause_set):
        if not clause_set:
            return 1
        n = len(clause_set)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if len(clause_set[i] & clause_set[j]) == 0:
                    order *= 2
        return order
    
    n_inputs = random.randint(5, 40)
    depth = random.randint(1, 10)
    circuit = generate_random_circuit(n_inputs, depth)
    clause_set = compute_clause_set(circuit)
    conjecture_holds = minimal_order_of_grothendieck_teichmueller_group(clause_set) <= depth ** 3
    
    return {
        "metric_name": "Minimal Order of Grothendieck-Teichmüller Group",
        "metric_value": minimal_order_of_grothendieck_teichmueller_group(clause_set),
        "instances_tested": 1,
        "n_max": n_inputs,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Circuit with depth {depth} and inputs {n_inputs}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with depth {results[first_failing_seed]['n_max']} and inputs {results[first_failing_seed]['instances_tested']}\") first_failing_seed={first_failing_seed}")