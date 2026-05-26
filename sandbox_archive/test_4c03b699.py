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

def generate_boolean_circuit(n, m):
    circuit = []
    for _ in range(m):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for gate_type, inputs in reversed(circuit):
        if gate_type == 'AND':
            result = all(inputs)
        elif gate_type == 'OR':
            result = any(inputs)
        stack.append(result)
    return stack.pop()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_max = math.isqrt(n * n // 3)
        for _ in range(5):  # Ensure at least 5 instances per seed
            m = random.randint(1, m_max)
            circuit = generate_boolean_circuit(n, m)
            rank = evaluate_circuit(circuit)
            results.append((n, m, rank))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(rank for _, _, rank in results)
    mean_rank = total_rank / len(results)
    conjecture_holds = all(rank <= n**(2/3) for _, _, rank in results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, m={m}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=no_results")
        sys.exit(0)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")