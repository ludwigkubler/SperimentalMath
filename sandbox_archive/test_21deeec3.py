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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def continued_fraction(numerator, denominator):
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    p0, q0 = numerator, denominator
    p1, q1 = 1 - numerator, 1 - denominator
    a0 = numerator // denominator
    a1 = (1 - numerator) // (1 - denominator)
    
    if a0 == a1:
        return [a0]
    
    cf = [a0, a1]
    while True:
        p2 = q1 * a1 + p1
        q2 = q1 * a1 + q1
        a2 = (p2 - numerator) // q2
        if a2 == a1:
            break
        cf.append(a2)
        p1, q1 = p2, q2
        a1 = a2
    
    return cf

def build_random_circuit(n, size, depth):
    gates = ['AND', 'OR', 'MOD_2', 'MOD_3', 'NOT']
    circuit = []
    
    def add_gate(gate, inputs=None):
        if gate == 'NOT':
            input_index = random.randint(0, len(circuit) - 1)
            circuit.append((gate, input_index))
        else:
            input_indices = [random.randint(0, len(circuit) - 1) for _ in range(3)]
            circuit.append((gate, input_indices))
    
    stack = []
    for _ in range(depth):
        gate = random.choice(gates)
        add_gate(gate)
        if gate == 'NOT':
            stack.append((gate, stack.pop()))
        else:
            stack.extend([(gate, stack.pop())] * 3)
    
    return circuit

def is_acc0_circuit(circuit):
    for gate, inputs in circuit:
        if gate == 'MOD_2' or gate == 'MOD_3':
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 15, 18]
    results = []
    
    for n in n_values:
        for size in [20, 40, 80]:
            for depth in [2, 3, 4]:
                circuit = build_random_circuit(n, size, depth)
                if not is_acc0_circuit(circuit):
                    continue
                
                truth_table = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
                p_values = [sum(truth_table[i][j] for j in range(2**n)) / (2**n) for i in range(2**n)]
                
                tau = []
                rho = truth_table
                for _ in range(math.ceil(math.log2(n))):
                    max_diff = -1
                    best_var, best_val = None, None
                    for var in range(n):
                        for val in [0, 1]:
                            new_rho = [[rho[i][j] if (i >> var) & 1 == val else 0 for j in range(2**n)] for i in range(2**n)]
                            diff = abs(sum(new_rho[i][j] for j in range(2**n)) / (2**n) - 0.5)
                            if diff > max_diff:
                                max_diff = diff
                                best_var, best_val = var, val
                    tau.append(max_diff)
                    rho = [[rho[i][j] if (i >> best_var) & 1 == best_val else 0 for j in range(2**n)] for i in range(2**n)]
                
                p_i_q_i = [p_values[rho.index([1]*2**n)] / (2**n)]
                cf_counts = [len(continued_fraction(p, q)) for p, q in zip(p_i_q_i, [2**i for i in range(len(p_i_q_i))])]
                D_f = sum(cf_counts)
                
                results.append({
                    "metric_name": "D(f)",
                    "metric_value": D_f,
                    "instances_tested": 1,
                    "conjecture_holds": D_f <= 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                    "counterexample": "" if D_f <= 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n) else f"n={n}, size={size}, depth={depth}"
                })
    
    return {
        "seed": seed,
        "metric_name": "D(f)",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.5:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"D(f) > bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")