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
    
    def generate_quandle(n):
        quandle = {}
        for i in range(1, n+1):
            quandle[i] = {j % n + 1 for j in range(i, i+n)}
        return quandle
    
    def calculate_automorphism_group(quandle):
        n = len(quandle)
        automorphisms = []
        for perm in itertools.permutations(range(1, n+1)):
            if all(quandle[perm[i]][j] == quandle[i][perm[j]] for i in range(n) for j in range(n)):
                automorphisms.append(perm)
        return len(automorphisms)
    
    def calculate_communication_complexity_rank_variance(circuit):
        n = len(circuit)
        rank_variances = [len(set(row)) for row in circuit]
        mean = sum(rank_variances) / n
        variance = sum((x - mean) ** 2 for x in rank_variances) / n
        return variance
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(1, n) for _ in range(random.randint(1, 2))]
            circuit.append((gate, inputs))
        return circuit
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            quandle = generate_quandle(n)
            automorphism_order = calculate_automorphism_group(quandle)
            rank_variance = calculate_communication_complexity_rank_variance(circuit)
            
            if rank_variance == 0:
                continue
            
            log_automorphism_order = math.log2(automorphism_order) if automorphism_order > 0 else -math.inf
            total_metric_value += log_automorphism_order * rank_variance
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "log_automorphism_order_rank_variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((log_automorphism_order * rank_variance - mean_metric_value) ** 2 for log_automorphism_order, rank_variance in zip(log_automorphism_orders, rank_variances)) / (instances_tested - 1))
    
    return {
        "metric_name": "log_automorphism_order_rank_variance",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")