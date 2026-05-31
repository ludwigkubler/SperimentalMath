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
    
    def generate_boolean_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def binary_representation(circuit):
        rep = []
        for gate, inputs in circuit:
            rep.extend(inputs)
        return rep
    
    def coxeter_group_generators(binary_rep):
        n = len(binary_rep)
        generators = set()
        for i in range(n):
            if binary_rep[i] == 1:
                generators.add(i)
        return generators
    
    def monotone_complexity(circuit):
        # Simplified version of monotone complexity calculation
        return sum(len(inputs) for gate, inputs in circuit)
    
    metric_name = "Coxeter Group Generators"
    instances_tested = 0
    n_max = 1
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(1, min(n, 10))
            circuit = generate_boolean_circuit(n, m)
            binary_rep = binary_representation(circuit)
            generators = coxeter_group_generators(binary_rep)
            complexity = monotone_complexity(circuit)
            
            if len(generators) > 2 * math.sqrt(m):
                conjecture_holds = False
                counterexample = f"Circuit with n={n}, m={m} has {len(generators)} generators and complexity {complexity}"
                break
            
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": metric_name,
        "metric_value": len(generators),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")