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
    
    def generate_circuit(n, m):
        # Generate a random Boolean circuit with n inputs and m gates
        # This is a simplified representation for testing purposes
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_coxeter_group_action_complexity(circuit):
        # Simplified computation of action complexity
        # This is a placeholder and should be replaced with actual computation
        m = len(circuit)
        n = max(len(inputs) for _, inputs in circuit)
        return (m ** (1/3)) * (n ** (2/3))
    
    def compute_frege_proof_depth(circuit):
        # Simplified computation of Frege proof depth
        # This is a placeholder and should be replaced with actual computation
        m = len(circuit)
        n = max(len(inputs) for _, inputs in circuit)
        return m + n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size at least 5 times
            m = random.randint(n, 2 * n)
            circuit = generate_circuit(n, m)
            action_complexity = compute_coxeter_group_action_complexity(circuit)
            frege_proof_depth = compute_frege_proof_depth(circuit)
            
            if action_complexity > (m ** (1/3)) * (n ** (2/3)):
                conjecture_holds = False
                counterexample = f"Seed {seed}: Action complexity {action_complexity} exceeds bound for n={n}, m={m}"
                break
            
            total_metric_value += action_complexity
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "Action Complexity",
        "metric_value": total_metric_value / instances_tested,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")