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
    
    def generate_circuit(n):
        if n <= 1:
            return []
        gate = random.randint(2, n-1)
        inputs = [random.randint(0, 1) for _ in range(gate)]
        circuit = [(gate, inputs)]
        for _ in range(n - gate - 1):
            new_gate = random.randint(2, gate + 1)
            inputs = [random.randint(0, 1) for _ in range(new_gate)]
            circuit.append((new_gate, inputs))
            gate += new_gate
        return circuit
    
    def calculate_local_indeterminacy(circuit):
        if not circuit:
            return 0
        n = len(circuit)
        local_indeterminacy = [0] * n
        for i in range(n):
            gate, inputs = circuit[i]
            for j in range(gate):
                if inputs[j] == 1:
                    local_indeterminacy[i] += 1
        return max(local_indeterminacy)
    
    def monotone_width(circuit):
        width = 0
        for gate, _ in circuit:
            width = max(width, gate)
        return width
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        w_n = monotone_width(circuit)
        local_indeterminacy = calculate_local_indeterminacy(circuit)
        alpha_w_n = math.log(n) if n > 0 else 0
        alpha_w_n_over_2 = math.log((n // 2)) if (n // 2) > 0 else 0
        
        metric_values.append(local_indeterminacy)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(alpha_w_n <= math.log(n) and alpha_w_n_over_2 <= math.log((n // 2)) for n, alpha_w_n, alpha_w_n_over_2 in zip(range(5, n_max + 1), metric_values, [math.log(n) if n > 0 else 0 for n in range(5, n_max + 1)], [math.log((n // 2)) if (n // 2) > 0 else 0 for n in range(5, n_max + 1)]))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": mean_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")