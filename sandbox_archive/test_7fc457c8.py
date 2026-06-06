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
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({left[0]} + {right[0]})', f'({left[0]} * {right[0]})']
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for token in circuit:
            if token.isdigit():
                stack.append(assignment[token])
            elif token == '+':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif token == '*':
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        return stack[0]
    
    def monotone_width(circuit):
        if not circuit:
            return 0
        max_width = 1
        current_width = 1
        for i in range(1, len(circuit)):
            if circuit[i] == '(':
                current_width += 1
            elif circuit[i] == ')':
                current_width -= 1
            max_width = max(max_width, current_width)
        return max_width
    
    def quaternionic_kahler_dimension(n):
        # Simplified approximation for demonstration purposes
        return Fraction(n ** (2 / 3))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        assignment = {str(i): random.randint(1, 10) for i in range(n)}
        value = evaluate_circuit(circuit, assignment)
        width = monotone_width(circuit)
        d = quaternionic_kahler_dimension(n)
        
        if width == 0:
            continue
        
        ratio = d / width
        results.append({
            "n": n,
            "value": value,
            "width": width,
            "d": d,
            "ratio": ratio
        })
    
    total_ratio = sum(result['ratio'] for result in results)
    avg_ratio = total_ratio / len(results) if results else 0
    
    return {
        "metric_name": "Ratio of Quaternionic Kähler Dimension to Monotone Width",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": all(0.5 * n ** (1 / 3) <= ratio <= 2 * n ** (2 / 3) for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_ratio = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(result['conjecture_holds'] for result in results) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0 support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='ratio_outside_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")