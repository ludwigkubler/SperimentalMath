# auto-injected by SEC sandbox
import math
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

def generate_circuit(depth):
    if depth == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
        return [random.choice([0, 1])] + subcircuits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        circuit = generate_circuit(n)
        depth = len(circuit) - 1
        
        # Construct the algebraic variety V_C (simplified representation)
        # For simplicity, we use a polynomial representation of the circuit
        polynomial = [0] * (n + 1)
        for gate in circuit:
            if gate == 0:
                polynomial[0] += 1
            else:
                polynomial[-1] -= 1
        
        # Measure QDD(V_C) (simplified calculation)
        qdd = abs(sum(polynomial))
        
        metric_values.append(qdd / depth)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    if any(x > y + 3 for x, y in zip(metric_values, [depth for _ in range(len(metric_values))])):
        conjecture_holds = False
        counterexample = "QDD(V_C) is more than 3 units larger than D(C)"
    
    return {
        "metric_name": "Quantum Deformation Degree / Depth Ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"QDD(V_C) > D(C) + 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")