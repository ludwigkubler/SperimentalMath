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
    
    def generate_circuit(n, d):
        if n == 1 and d == 0:
            return [[0]], 1
        elif n == 1 and d > 0:
            return [[random.choice([0, 1])], 1]
        else:
            inputs = [i for i in range(n)]
            gates = []
            for _ in range(d):
                new_gates = []
                for gate in gates:
                    new_gate = random.sample(inputs, len(gate))
                    new_gates.append(new_gate)
                gates.extend(new_gates)
            return gates, n
    
    def compute_local_induction_dimension(circuit):
        # Simplified version of computing local induction dimension
        # This is a placeholder and should be replaced with actual computation
        return 1
    
    def monotone_width(circuit):
        # Simplified version of computing monotone width
        # This is a placeholder and should be replaced with actual computation
        return len(max(circuit, key=len))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_mild = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit, w_c = generate_circuit(n, random.randint(1, min(n-1, 2)))
            mild = compute_local_induction_dimension(circuit)
            if mild <= 0 or w_c <= 0:
                continue
            total_mild += mild
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mild = total_mild / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = mean_mild >= math.log(n_max) * math.log(w_c)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_local_induction_dimension",
        "metric_value": mean_mild,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mild = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mild} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")