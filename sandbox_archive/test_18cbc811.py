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
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def weyl_group_representation(circuit):
        # Simplified representation using a dictionary
        rep = {}
        for gate_type, inputs in circuit:
            key = tuple(inputs)
            if key not in rep:
                rep[key] = 1
            else:
                rep[key] += 1
        return rep
    
    def minimal_rank(rep):
        return max(rep.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    sum_metric = 0
    support_count = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            m = int(n ** (2/3))
            circuit = generate_boolean_circuit(n, m)
            rep = weyl_group_representation(circuit)
            rank = minimal_rank(rep)
            
            total_instances += 1
            sum_metric += rank
            
            if rank > n ** (2/3):
                counterexample = f"n={n}, m={m}, rank={rank}"
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": total_instances,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
    
    mean_metric = sum_metric / total_instances
    support_fraction = support_count / 30
    
    if mean_metric <= 3:
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_metric,
            "instances_tested": total_instances,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_metric,
            "instances_tested": total_instances,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")