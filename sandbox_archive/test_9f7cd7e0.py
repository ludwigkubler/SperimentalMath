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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_property_Q(values):
        # Placeholder for property Q computation
        return sum(values) / len(values)
    
    def construct_AC0_circuit(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input size must be a power of 2")
        
        circuit = []
        for i in range(n):
            circuit.append((i, (f[i] + f[n+i]) % 2))
        return circuit
    
    def circuit_size(circuit):
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_sum = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        values = [f[i] for i in range(2**n)]
        Q = compute_property_Q(values)
        
        try:
            circuit = construct_AC0_circuit(f)
        except ValueError as e:
            counterexample = str(e)
            conjecture_holds = False
            break
        
        s = circuit_size(circuit)
        metric_sum += s
        instances_tested += 1
        
        if s < n * math.log(n, 2):
            counterexample = f"Circuit size {s} is less than {n * math.log(n, 2)}"
            conjecture_holds = False
    
    metric_mean = metric_sum / instances_tested if instances_tested > 0 else float('nan')
    
    return {
        "metric_name": "Circuit Size",
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if not math.isnan(r["metric_value"])]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")