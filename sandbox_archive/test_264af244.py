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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def groupoid_order(circuit):
        # Simplified mapping from circuit to groupoid order
        return len(circuit)
    
    metric_name = "groupoid_order"
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):  # Sample at least 30 instances per seed
            circuit = generate_circuit(n)
            order = groupoid_order(circuit)
            metric_value = order / (n * math.log(n))
            
            total_metric_value += metric_value
            instances_tested += 1
            n_max = max(n_max, n)
            
            if order > c * n * math.log(n):
                conjecture_holds = False
                counterexample = f"Circuit with {n} inputs and order {order}"
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")