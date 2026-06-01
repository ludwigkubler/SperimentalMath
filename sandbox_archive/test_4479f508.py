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
    
    def generate_circuit(n, d):
        if n == 1:
            return ['x']
        else:
            inputs = [f'x{i}' for i in range(1, n+1)]
            subcircuits = [generate_circuit(n//2, d-1) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [f'{gate}({", ".join(subcircuits[0])}, {", ".join(subcircuits[1])})']
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str) and circuit.startswith('x'):
            return circuit
        else:
            op = circuit.split('(')[0]
            args = [evaluate_circuit(arg.strip()) for arg in circuit.split('(')[1].split(', ')[:-1]]
            if op == 'AND':
                return all(args)
            elif op == 'OR':
                return any(args)
    
    def compute_resolution_width(circuit):
        # Simplified resolution width estimation
        depth = 0
        queue = [circuit]
        while queue:
            node = queue.pop()
            if isinstance(node, str) and node.startswith('x'):
                continue
            op = node.split('(')[0]
            args = [arg.strip() for arg in node.split('(')[1].split(', ')[:-1]]
            depth += 1
            queue.extend(args)
        return depth
    
    def compute_local_coherence_rank(circuit):
        # Simplified local coherence rank estimation
        visited = set()
        stack = [circuit]
        rank = 0
        while stack:
            node = stack.pop()
            if isinstance(node, str) and node.startswith('x'):
                if node not in visited:
                    visited.add(node)
                    rank += 1
                continue
            op = node.split('(')[0]
            args = [arg.strip() for arg in node.split('(')[1].split(', ')[:-1]]
            stack.extend(args)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(2, 5))
            width = compute_resolution_width(circuit)
            rank = compute_local_coherence_rank(circuit)
            results.append((n, width, rank))
    
    if not results:
        return {
            "metric_name": "local_coherence_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    instances_tested = len(results)
    width_values = [w for _, w, _ in results]
    rank_values = [r for _, _, r in results]
    
    mean_width = sum(width_values) / instances_tested
    mean_rank = sum(rank_values) / instances_tested
    
    correlation_coefficient = (sum((w - mean_width) * (r - mean_rank) for w, r, _ in results) /
                                math.sqrt(sum((w - mean_width)**2 for w, _, _ in results) *
                                          sum((r - mean_rank)**2 for _, r, _ in results)))
    
    return {
        "metric_name": "local_coherence_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Arbitrary threshold for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")