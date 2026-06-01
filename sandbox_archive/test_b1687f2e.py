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

def generate_random_circuit(n):
    if n < 2:
        return []
    
    gates = ['AND', 'OR', 'NOT']
    circuit = []
    for _ in range(10):  # Limit the depth of the circuit to avoid excessive complexity
        gate_type = random.choice(gates)
        if gate_type == 'NOT':
            inputs = [random.randint(0, len(circuit)-1)]
        else:
            inputs = [random.randint(0, len(circuit)-1) for _ in range(2)]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for gate in reversed(circuit):
        if gate[0] == 'NOT':
            input_val = stack.pop()
            stack.append(not input_val)
        else:
            input1 = stack.pop()
            input2 = stack.pop()
            if gate[0] == 'AND':
                stack.append(input1 and input2)
            elif gate[0] == 'OR':
                stack.append(input1 or input2)
    return stack[0]

def calculate_monotone_width(circuit):
    n = len(circuit)
    width = 0
    for i in range(n):
        if circuit[i][0] != 'NOT':
            inputs = circuit[i][1]
            max_input = max(inputs, key=lambda x: circuit[x][0] == 'NOT')
            width = max(width, max_input + 1)
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_order = 0
        
        for _ in range(30):  # Test 30 random circuits per size
            circuit = generate_random_circuit(n)
            if not circuit:
                continue
            
            output = evaluate_circuit(circuit)
            monotone_width = calculate_monotone_width(circuit)
            
            instances_tested += 1
            total_order += monotone_width  # Using monotone width as a proxy for order
            
        if instances_tested == 0:
            continue
        
        avg_order = total_order / instances_tested
        correlation_coefficient = (instances_tested * sum(avg_order * monotone_width for avg_order, monotone_width in zip([avg_order] * instances_tested, [monotone_width] * instances_tested)) - instances_tested * avg_order * avg_order) / math.sqrt((instances_tested * sum(avg_order**2 for avg_order in [avg_order] * instances_tested) - instances_tested * avg_order**2) * (instances_tested * sum(monotone_width**2 for monotone_width in [monotone_width] * instances_tested) - instances_tested * monotone_width**2))
        
        results.append({
            "n": n,
            "avg_order": avg_order,
            "correlation_coefficient": correlation_coefficient
        })
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    avg_order = sum(result["avg_order"] for result in results) / len(results)
    correlation_coefficient = sum(result["correlation_coefficient"] for result in results) / len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,  # Placeholder for p-value calculation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    # Placeholder for computing mean/std and fraction of seeds where conjecture_holds