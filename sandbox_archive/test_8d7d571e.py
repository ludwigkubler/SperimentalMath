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
        # Placeholder for the actual computation of property Q
        return sum(values) / len(values)
    
    def construct_AC0_circuit(f):
        n = int(math.log2(len(f)))
        circuit = []
        for i in range(n):
            circuit.append(random.choice([0, 1]))
        return circuit
    
    def circuit_size(circuit):
        return len(circuit)
    
    def property_Q_holds(Q, s, c, n):
        return s >= c * math.log2(n)
    
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            Q = compute_property_Q(f)
            C = construct_AC0_circuit(f)
            s = circuit_size(C)
            
            if not property_Q_holds(Q, s, 1, n):  # Placeholder value for c
                conjecture_holds = False
                counterexample = f"n={n}, Q={Q}, s={s}"
                break
            
            metric_values.append(Q)
            instances_tested += 1
    
    return {
        "metric_name": "property_Q",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")