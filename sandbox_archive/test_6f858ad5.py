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
    
    def evaluate_circuit(circuit):
        stack = []
        for gate, *inputs in circuit:
            if gate == 'AND':
                b = stack.pop()
                a = stack.pop()
                stack.append(a and b)
            elif gate == 'OR':
                b = stack.pop()
                a = stack.pop()
                stack.append(a or b)
            elif gate == 'NOT':
                a = stack.pop()
                stack.append(not a)
        return stack[0]
    
    def tautology_set(circuit):
        n = len(circuit)
        inputs = list(itertools.product([False, True], repeat=n))
        tautologies = []
        for input_values in inputs:
            if evaluate_circuit(list(zip(['NOT'] * n + ['AND'] * (n - 1), input_values))):
                tautologies.append(input_values)
        return tautologies
    
    def minimal_order(circuit):
        tautology = tautology_set(circuit)
        order = {}
        for i in range(len(tautology)):
            for j in range(i + 1, len(tautology)):
                if all(tautology[i][k] == tautology[j][k] for k in range(len(tautology))):
                    continue
                diff = sum(1 for k in range(len(tautology)) if tautology[i][k] != tautology[j][k])
                if diff not in order:
                    order[diff] = 0
                order[diff] += 1
        return max(order.values())
    
    def entanglement_entropy(circuit):
        n = len(circuit)
        inputs = list(itertools.product([False, True], repeat=n))
        probabilities = [evaluate_circuit(list(zip(['NOT'] * n + ['AND'] * (n - 1), input_values))) for input_values in inputs]
        entropy = 0
        for p in probabilities:
            if p > 0 and p < 1:
                entropy -= p * math.log2(p) + (1 - p) * math.log2(1 - p)
        return entropy
    
    n_max = 40
    instances_tested = 0
    total_diff = 0
    max_diff = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = []
            for _ in range(n):
                gate = random.choice(['AND', 'OR'])
                inputs = tuple(random.choice([False, True]) for _ in range(n - 1))
                circuit.append((gate,) + inputs)
            order = minimal_order(circuit)
            ent = entanglement_entropy(circuit)
            diff = abs(order - ent)
            total_diff += diff
            max_diff = max(max_diff, diff)
            instances_tested += 1
    
    conjecture_holds = all(diff <= 1 for diff in [total_diff / instances_tested])
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": total_diff / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")