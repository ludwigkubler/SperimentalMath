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
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def is_satisfiable(circuit):
        stack = []
        for gate, inputs in reversed(circuit):
            if not stack:
                stack.append(inputs[0])
            else:
                a = stack.pop()
                b = inputs[1]
                if gate == 'AND':
                    stack.append(a and b)
                elif gate == 'OR':
                    stack.append(a or b)
        return stack[0] if stack else False
    
    def automorphism_group(circuit):
        n = len(circuit)
        G = []
        for perm in itertools.permutations(range(n)):
            new_circuit = [(gate, [perm[i] for i in inputs]) for gate, inputs in circuit]
            if is_satisfiable(new_circuit) == is_satisfiable(circuit):
                G.append(perm)
        return G
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        Aut_C = automorphism_group(circuit)
        satisfiability_complexity = sum(is_satisfiable(circuit) for _ in range(100))
        
        if not Aut_C or len(Aut_C[0]) == 0:
            continue
        
        log_Aut_C = math.log2(len(Aut_C))
        log_n = math.log(n)
        ratio = log_Aut_C / log_n
        results.append((n, satisfiability_complexity, ratio))
    
    if not results:
        return {
            "metric_name": "log_Aut_C_over_log_n",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(ratio for _, _, ratio in results) / len(results)
    std_dev = math.sqrt(sum((ratio - mean_ratio)**2 for _, _, ratio in results) / len(results))
    support_fraction = sum(1 for _, _, ratio in results if abs(ratio - mean_ratio) <= 0.5 * std_dev) / len(results)
    
    return {
        "metric_name": "log_Aut_C_over_log_n",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds if "counterexample" not in result]
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - mean_ratio) <= 0.5 * std_dev) / len(results)
    
    if all("counterexample" not in result for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")