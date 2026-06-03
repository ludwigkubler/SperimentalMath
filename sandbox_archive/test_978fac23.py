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
    
    def generate_circuit(depth, size):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(depth - 1, size // (2 ** depth)) for _ in range(2)]
            return [random.choice([0, 1]) + (x << (size // (2 ** depth))) for x in sum(subcircuits, [])]
    
    def topological_entropy(circuit):
        n = len(circuit)
        transitions = {}
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] == circuit[j]:
                    continue
                key = (circuit[i], circuit[j])
                if key not in transitions:
                    transitions[key] = []
                transitions[key].append(j - i)
        entropy = 0
        for times in transitions.values():
            p = len(times) / n
            entropy -= p * math.log2(p)
        return entropy
    
    def f(n):
        # Polynomial function to bound the number of literals
        return n ** 2
    
    metric_name = "topological_entropy"
    instances_tested = 0
    n_max = 0
    total_entropy = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        for _ in range(5):
            circuit = generate_circuit(3, n)
            entropy = topological_entropy(circuit)
            total_entropy += entropy
            instances_tested += 1
            n_max = max(n_max, len(circuit))
            
            if entropy < math.log2(n) or entropy > 0.1 * n:
                conjecture_holds = False
                counterexample = f"Circuit of size {n} with entropy {entropy}"
                break
    
    mean_entropy = total_entropy / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")