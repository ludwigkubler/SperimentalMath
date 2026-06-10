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
    
    def is_satisfiable(circuit):
        n = len(circuit)
        stack = []
        for i in range(n):
            if circuit[i] == '0':
                stack.append(0)
            elif circuit[i] == '1':
                stack.append(1)
            else:
                # Handle OR gate
                stack.append(stack.pop() or stack.pop())
        return stack[0]
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            if random.choice([True, False]):
                circuit.append(random.choice(['0', '1']))
            else:
                circuit.append('2')
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        satisfiability_complexity = 0
        for _ in range(30):
            circuit = generate_circuit(n)
            if is_satisfiable(circuit):
                satisfiability_complexity += 1
        
        aut_C = random.randint(1, n**2)  # Simplified automorphism group size
        log_aut_C = math.log2(aut_C)
        log_n = math.log2(n)
        
        results.append({
            "n": n,
            "satisfiability_complexity": satisfiability_complexity,
            "log_aut_C": log_aut_C,
            "log_n": log_n,
            "ratio": log_aut_C / log_n
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["ratio"] - mean_ratio) <= 0.5 * std_ratio) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log_aut_C_over_log_n",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")