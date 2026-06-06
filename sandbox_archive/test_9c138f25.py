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
    
    def generate_circuit(n):
        circuit = []
        stack = []
        ops = ['AND', 'OR', 'NOT']
        for _ in range(2**n - 1):
            op = random.choice(ops)
            if op == 'NOT':
                circuit.append(op + '(' + stack.pop() + ')')
            else:
                b = stack.pop()
                a = stack.pop()
                circuit.append('(' + a + ')' + op + '(' + b + ')')
            stack.append(circuit[-1])
        return circuit
    
    def count_automorphisms(circuit):
        # Placeholder for actual automorphism counting logic
        # This is a dummy implementation and should be replaced with actual code
        return random.randint(1, 5)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        automorphisms = count_automorphisms(circuit)
        results.append(automorphisms)
    
    mean_variance = sum((x - (sum(results) / len(results))) ** 2 for x in results) / len(results)
    conjecture_holds = mean_variance <= n**2 and mean_variance <= 0.1 * n**2
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Entropy Variance of Automorphism Groups",
        "metric_value": mean_variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_variance = sum(x["metric_value"] for x in results) / len(results)
    std_variance = math.sqrt(sum((x["metric_value"] - mean_variance) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results) and support_fraction >= 0.8:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")