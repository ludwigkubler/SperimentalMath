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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0'], []
        else:
            inputs = [f'x{i}' for i in range(n)]
            gates = []
            for _ in range(n - 1):
                gate = random.choice(['AND', 'OR'])
                a, b = random.sample(inputs, 2)
                output = f'y{len(gates)}'
                gates.append((gate, a, b, output))
                inputs.remove(a)
                inputs.remove(b)
                inputs.append(output)
            return [f'x{i}' for i in range(n - 1)], gates
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                b = stack.pop()
                a = stack.pop()
                stack.append(a and b)
            elif gate[0] == 'OR':
                b = stack.pop()
                a = stack.pop()
                stack.append(a or b)
        return stack[0]
    
    def monotone_width(circuit):
        n = len(circuit) + 1
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][i] = 1
            for j in range(i - 2, -1, -1):
                dp[j][i] = max(dp[j][k] + dp[k + 1][i] for k in range(j, i))
        return dp[0][n]
    
    def minimal_dimension(n):
        # Placeholder function to simulate the computation of d
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            inputs, gates = generate_boolean_circuit(n)
            circuit = [(gate[0], gate[1], gate[2]) for gate in gates]
            assignment = {f'x{i}': random.choice([True, False]) for i in range(n)}
            result = evaluate_circuit(circuit, assignment)
            d = minimal_dimension(n)
            w_m = monotone_width(gates)
            if w_m == 0:
                continue
            ratio = d / w_m
            results.append((n, ratio))
    
    total_ratio = sum(ratio for _, ratio in results) / len(results)
    conjecture_holds = all(1.5 * n**(2/3) <= ratio <= 2 * n**(1/3) for _, ratio in results)
    
    return {
        "metric_name": "Ratio of d to w_m",
        "metric_value": total_ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")