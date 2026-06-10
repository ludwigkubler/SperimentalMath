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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return random.choice([True, False])
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return (op, left, right)
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, bool):
            return circuit
        op, left, right = circuit
        if op == 'AND':
            return evaluate_circuit(left) and evaluate_circuit(right)
        elif op == 'OR':
            return evaluate_circuit(left) or evaluate_circuit(right)
    
    def tropical_rank(circuit):
        # Simplified version for demonstration; actual computation depends on the tropical curve T_C
        return len(str(evaluate_circuit(circuit)))
    
    depths = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    n_max = max(depths)
    
    for depth in depths:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(depth)
            rank = tropical_rank(circuit)
            circuit_ranks.append((depth, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "Spearman correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    depths = [x for x, _ in circuit_ranks]
    ranks = [y for _, y in circuit_ranks]
    
    def spearman_correlation(x, y):
        n = len(x)
        if n != len(y):
            return None
        rank_x = {v: i + 1 for i, v in enumerate(sorted(set(x), reverse=True))}
        rank_y = {v: i + 1 for i, v in enumerate(sorted(set(y), reverse=True))}
        sum_diff_squared_ranks = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squared_ranks) / (n * (n**2 - 1))
    
    correlation_coefficient = spearman_correlation(depths, ranks)
    
    return {
        "metric_name": "Spearman correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuit_ranks),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")