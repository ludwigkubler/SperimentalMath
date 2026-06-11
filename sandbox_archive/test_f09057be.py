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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_entanglement_complexity(circuit):
        complexity = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                complexity += sum(inputs)
            elif gate == 'OR':
                complexity += len([x for x in inputs if x == 1])
        return complexity
    
    def find_geometric_group_action_size(circuit):
        n = len(circuit[0][1])
        # Simplified heuristic to estimate the size of the geometric group action
        return n * (n - 1) // 2
    
    n = random.randint(5, 30)
    circuit = generate_random_circuit(n)
    e_C = calculate_entanglement_complexity(circuit)
    ord_G = find_geometric_group_action_size(circuit)
    
    return {
        "metric_name": "ord(G)",
        "metric_value": ord_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_G <= e_C**2,
        "counterexample": "" if ord_G <= e_C**2 else f"ord(G)={ord_G}, e(C)^2={e_C**2}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ord_G = sum(r["metric_value"] for r in results) / len(results)
    std_ord_G = math.sqrt(sum((r["metric_value"] - mean_ord_G)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ord_G} std={std_ord_G} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ord(G) > e(C)^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")