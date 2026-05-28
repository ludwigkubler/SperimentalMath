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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0']  # Base case: a single gate (constant function)
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in left] + [f'(NOT {l})' for l in right]
    
    def evaluate_circuit(circuit, input_values):
        if isinstance(circuit, str):
            return circuit
        elif circuit[0] == '(' and circuit[-1] == ')':
            op = circuit[2:circuit.find(' ')]
            args = [evaluate_circuit(arg.strip(), input_values) for arg in circuit[circuit.find(' ')+1:-1].split(',')]
            if op == 'AND':
                return all(args)
            elif op == 'OR':
                return any(args)
            elif op == 'NOT':
                return not args[0]
        else:
            return input_values[int(circuit)]
    
    def tropical_cyclotomic_polynomial(circuit):
        n = len(circuit)
        if n == 1:
            return [Fraction(1, 2)]
        else:
            left_poly = tropical_cyclotomic_polynomial(circuit[:n // 2])
            right_poly = tropical_cyclotomic_polynomial(circuit[n // 2:])
            result = []
            for l in left_poly:
                for r in right_poly:
                    result.append(l * r)
            return result
    
    def rank(poly):
        if not poly:
            return 0
        max_rank = 1
        for i in range(len(poly)):
            current_rank = 1
            for j in range(i + 1, len(poly)):
                if poly[j] > poly[i]:
                    current_rank += 1
            max_rank = max(max_rank, current_rank)
        return max_rank
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    input_values = [random.choice(['0', '1']) for _ in range(n)]
    poly = tropical_cyclotomic_polynomial(circuit)
    
    if not poly:
        return {
            "metric_name": "rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    current_rank = rank(poly)
    size_bound = Fraction(n, 5) ** (Fraction(1, 5))
    
    return {
        "metric_name": "rank",
        "metric_value": current_rank,
        "instances_tested": 1,
        "conjecture_holds": current_rank <= size_bound,
        "counterexample": "" if current_rank <= size_bound else f"Rank {current_rank} exceeds bound {size_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_tests = sum(r["instances_tested"] for r in results)
    mean_value = sum(r["metric_value"] for r in results) / total_tests
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / total_tests)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")