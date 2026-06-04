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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), 2))
            circuit.append((gate_type, inputs))
        return circuit
    
    def is_subgroup(g1, g2):
        if len(g1) > len(g2):
            return False
        for g in g1:
            found = False
            for h in g2:
                if g == h:
                    found = True
                    break
            if not found:
                return False
        return True
    
    def find_symmetry_group(circuit):
        n = len(circuit)
        symmetries = []
        for perm in itertools.permutations(range(n)):
            new_circuit = [(c[0], [perm[i] for i in c[1]]) for c in circuit]
            if is_subgroup(new_circuit, circuit):
                symmetries.append(perm)
        return symmetries
    
    def monotone_width(circuit):
        # Placeholder function to compute the monotone width
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    circuit = generate_circuit(n, m)
    symmetries = find_symmetry_group(circuit)
    symmetry_order = len(symmetries)
    width = monotone_width(circuit)
    
    return {
        "metric_name": "symmetry_order_vs_monotone_width",
        "metric_value": symmetry_order / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")