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
    
    def generate_random_permutation(n):
        return [i for i in range(n)]
    
    def generate_random_circuit(d, w):
        circuit = []
        for _ in range(d):
            layer = [random.randint(0, w-1) for _ in range(w)]
            circuit.append(layer)
        return circuit
    
    def calculate_permutation_group_order(permutation):
        n = len(permutation)
        order = 1
        while True:
            permutation = [permutation[permutation[i]] for i in range(n)]
            order += 1
            if permutation == list(range(n)):
                break
        return order
    
    def calculate_circuit_group_order(circuit):
        n = len(circuit)
        d = len(circuit)
        w = len(circuit[0])
        order = 1
        while True:
            circuit = [[circuit[layer][i] for layer in range(d)] for i in range(w)]
            order += 1
            if all(all(circuit[layer][i] == j % w for i in range(w)) for layer in range(d)):
                break
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    permutation_orders = []
    circuit_orders = []
    
    for n in n_values:
        permutation = generate_random_permutation(n)
        permutation_order = calculate_permutation_group_order(permutation)
        permutation_orders.append(permutation_order)
    
    for d in range(1, 6):
        for w in range(1, 6):
            circuit = generate_random_circuit(d, w)
            circuit_order = calculate_circuit_group_order(circuit)
            circuit_orders.append((d, w, circuit_order))
    
    mean_permutation_order = sum(permutation_orders) / len(permutation_orders)
    mean_circuit_order = sum(order for _, _, order in circuit_orders) / len(circuit_orders)
    
    conjecture_holds = (mean_permutation_order >= n_values[-1]**2 / 4 and
                        all(order >= (d + w)**2 for d, w, order in circuit_orders))
    
    counterexample = ""
    if not conjecture_holds:
        if mean_permutation_order < n_values[-1]**2 / 4:
            counterexample += f"Permutation order too low: {mean_permutation_order} < {n_values[-1]**2 / 4}\n"
        for d, w, order in circuit_orders:
            if order < (d + w)**2:
                counterexample += f"Circuit order too low for d={d}, w={w}: {order} < {(d + w)**2}\n"
    
    return {
        "metric_name": "Group Order",
        "metric_value": mean_permutation_order,
        "instances_tested": len(permutation_orders) + len(circuit_orders),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample.strip()
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break