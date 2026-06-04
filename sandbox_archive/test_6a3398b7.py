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
        for _ in range(n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, assignment):
        stack = list(assignment)
        for gate_type, inputs in reversed(circuit):
            if len(stack) < len(inputs):
                return None
            operands = [stack.pop() for _ in inputs]
            if gate_type == 'AND':
                result = all(operands)
            elif gate_type == 'OR':
                result = any(operands)
            stack.append(result)
        return stack[0] if len(stack) == 1 else None
    
    def calculate_local_indeterminacy(circuit):
        n = len(circuit) + 1
        assignments = []
        for i in range(2 ** n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            result = evaluate_circuit(circuit, assignment)
            if result is not None:
                assignments.append((assignment, result))
        
        if len(assignments) < 2:
            return None
        
        values = [result for _, result in assignments]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return None
        
        local_indeterminacy = std_dev / mean
        return local_indeterminacy
    
    def monotone_width(circuit):
        width = 0
        stack = []
        for gate_type, inputs in circuit:
            stack.append(len(inputs))
            width = max(width, len(stack))
        while stack:
            stack.pop()
            width = max(width, len(stack))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        w_n = monotone_width(circuit)
        local_indeterminacy = calculate_local_indeterminacy(circuit)
        
        if local_indeterminacy is None or w_n == 0:
            continue
        
        results.append({
            "n": n,
            "w_n": w_n,
            "local_indeterminacy": local_indeterminacy
        })
    
    if not results:
        return {
            "metric_name": "local_indeterminacy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    local_indeterminacies = [result["local_indeterminacy"] for result in results]
    mean_local_indeterminacy = sum(local_indeterminacies) / instances_tested
    std_dev_local_indeterminacy = math.sqrt(sum((x - mean_local_indeterminacy) ** 2 for x in local_indeterminacies) / instances_tested)
    
    conjecture_holds = all(
        result["local_indeterminacy"] <= math.log(result["n"], 2) and
        result["local_indeterminacy"] <= (math.log(result["n"], 2)) ** (3/2)
        for result in results
    )
    
    counterexample = ""
    if not conjecture_holds:
        first_failing_result = next(result for result in results if 
            result["local_indeterminacy"] > math.log(result["n"], 2) or
            result["local_indeterminacy"] > (math.log(result["n"], 2)) ** (3/2)
        )
        counterexample = f"w({first_failing_result['n']})={first_failing_result['w_n']}, local_indeterminacy={first_failing_result['local_indeterminacy']}"

    return {
        "metric_name": "local_indeterminacy",
        "metric_value": mean_local_indeterminacy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = result["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")