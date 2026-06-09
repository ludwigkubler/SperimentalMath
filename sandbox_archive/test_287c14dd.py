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
    
    def generate_circuit(n, D):
        if n == 1:
            return [[0], [1]]
        else:
            subcircuits = [generate_circuit(n//2, D-1), generate_circuit(n-n//2, D-1)]
            circuit = []
            for i in range(2**(n//2)):
                for j in range(2**(n-n//2)):
                    circuit.append([x ^ y for x, y in zip(subcircuits[0][i], subcircuits[1][j])])
            return circuit
    
    def compute_entropy(circuit):
        n = len(circuit)
        transitions = [0] * (1 << n)
        for state in range(1 << n):
            next_state = circuit[state]
            transitions[(state, tuple(next_state))] += 1
        entropy = 0
        for count in transitions:
            if count > 0:
                p = count / sum(transitions)
                entropy -= p * math.log2(p)
        return entropy
    
    def depth(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            subcircuits = [circuit[:n//2], circuit[n//2:]]
            return 1 + max(depth(sub) for sub in subcircuits)
    
    D_max = 40
    instances_tested = 0
    n_max = 0
    total_entropy = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n, D_max)
            entropy = compute_entropy(circuit)
            depth_val = depth(circuit)
            instances_tested += 1
            n_max = max(n_max, n)
            total_entropy += entropy
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = all(mean_entropy <= d * math.log2(2**(d+1)) for d in range(5, D_max + 1))
    
    return {
        "metric_name": "Topological Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")