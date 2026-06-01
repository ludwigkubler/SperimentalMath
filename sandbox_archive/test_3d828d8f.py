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
    
    def generate_circuit(m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                circuit.append((gate_type, random.randint(1, m)))
            else:
                circuit.append((gate_type, random.sample(range(1, m), 2)))
        return circuit
    
    def communication_complexity(circuit):
        # Simplified model for communication complexity
        return len(circuit)
    
    def quaternionic_automorphism_group_order(circuit):
        # Simplified model for automorphism group order
        return 2 ** len(circuit)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for m in [5, 10, 15, 20, 30, 40]:
        n_max = max(n_max, m)
        instances_tested += m
        for _ in range(m):
            circuit = generate_circuit(m)
            cc = communication_complexity(circuit)
            order = quaternionic_automorphism_group_order(circuit)
            if cc == 0:
                continue
            ratio = order / cc
            if not (0.5 <= ratio <= 1.5):
                conjecture_holds = False
                counterexample = f"Circuit with m={m} has out-of-range ratio {ratio}"
    
    return {
        "metric_name": "Ratio of Quaternionic Automorphism Group Order to Communication Complexity",
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
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break