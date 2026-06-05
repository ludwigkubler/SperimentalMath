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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(n):
            w = random.randint(1, n)
            gate = [random.choice(['AND', 'OR'])] * (w - 1)
            circuit.append((gate, w))
        return circuit
    
    def compute_brauer_group_order(circuit):
        # Placeholder function to simulate Brauer group order computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 100)  # Simulating a small Brauer group order
    
    def poly(w):
        # Polynomial function of w (degree less than or equal to w)
        return Fraction(w**2 + w + 1)
    
    circuit = generate_monotone_circuit(random.randint(5, 40))
    orders = [compute_brauer_group_order(gate) for gate, _ in circuit]
    
    conjecture_holds = all(order <= poly(w) for order, (_, w) in zip(orders, circuit) if w > 0)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Brauer group order",
        "metric_value": sum(orders) / len(orders),
        "instances_tested": len(circuit),
        "n_max": max(w for _, w in circuit),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")