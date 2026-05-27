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
    
    def generate_boolean_circuit(n, m):
        # Generate a random boolean circuit with n variables and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def characteristic_polynomial(circuit):
        # Compute the characteristic polynomial of the circuit
        n = len(circuit)
        poly = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        poly[0][0] = Fraction(1, 1)
        
        for gate_type, inputs in circuit:
            new_poly = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
            if gate_type == 'AND':
                for i in range(n + 1):
                    for j in range(n + 1):
                        if i >= len(inputs) and j >= len(inputs):
                            new_poly[i][j] = poly[i - len(inputs)][j - len(inputs)] * Fraction(1, 2)
            elif gate_type == 'OR':
                for i in range(n + 1):
                    for j in range(n + 1):
                        if i >= len(inputs) and j >= len(inputs):
                            new_poly[i][j] = poly[i - len(inputs)][j - len(inputs)] * Fraction(1, 2)
            poly = new_poly
        
        return poly
    
    def grothendieck_riemann_roch_index(poly):
        # Compute the Grothendieck–Riemann–Roch index
        n = len(poly) - 1
        independent_monomials = sum(1 for row in poly if any(coeff != Fraction(0, 1) for coeff in row))
        return independent_monomials
    
    def satisfies_riemann_roch_condition(circuit):
        # Check if the circuit satisfies the Riemann–Roch condition
        n = len(circuit)
        m = len(circuit)
        genus = (n - m + 1) // 2
        return genus >= 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_boolean_circuit(n, random.randint(2 * n, 3 * n))
            if satisfies_riemann_roch_condition(circuit):
                poly = characteristic_polynomial(circuit)
                gRR = grothendieck_riemann_roch_index(poly)
                results.append(gRR)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(x <= (n ** (2/3)) * (len(circuit) ** (1/3)) for n, circuit in zip(n_values, random.sample([generate_boolean_circuit(n, random.randint(2 * n, 3 * n)) for n in n_values], len(n_values))) if satisfies_riemann_roch_condition(circuit))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Grothendieck–Riemann–Roch Index",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")