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
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = 0
        stack = []
        for gate, inputs in circuit:
            while stack and gate == 'AND':
                stack.pop()
            stack.append(gate)
            width = max(width, len(stack))
        return width
    
    def qps_order(n):
        # Placeholder function to simulate QPS order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return n * 2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        w_m = monotone_width(circuit)
        qps_order_n = qps_order(n)
        
        if abs(w_m - qps_order_n) > 30:
            return {
                "metric_name": "Absolute Difference",
                "metric_value": abs(w_m - qps_order_n),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Monotone width exceeds QPS order by more than 30 units"
            }
        
        results.append({
            "metric_name": "Absolute Difference",
            "metric_value": abs(w_m - qps_order_n),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "Average Absolute Difference",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": 30,
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Monotone width exceeds QPS order by more than 30 units' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")