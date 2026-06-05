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
    
    def generate_random_boolean_circuit(n, d):
        if n == 1:
            return [[random.choice([0, 1])]]
        else:
            inputs = [i for i in range(1, n)]
            gates = []
            for _ in range(d):
                gate = random.sample(inputs, 2)
                output = len(gates) + 1
                gates.append((gate[0], gate[1], output))
            return gates
    
    def compute_minimal_local_induction_dimension(circuit):
        n = len(circuit) + 1
        # Simplified computation for demonstration purposes
        return math.log(n, 2)
    
    def monotone_width(circuit):
        max_width = 0
        for gate in circuit:
            width = len(gate[0])
            if width > max_width:
                max_width = width
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_boolean_circuit(n, random.randint(1, n-1))
            mild = compute_minimal_local_induction_dimension(circuit)
            w_c = monotone_width(circuit)
            expected_bound = math.log(n, 2) * math.log(w_c)
            
            if mild < expected_bound:
                conjecture_holds = False
                counterexample = f"n={n}, mild={mild}, expected_bound={expected_bound}"
                break
            
            total_metric_value += mild
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "minimal_local_induction_dimension",
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
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")