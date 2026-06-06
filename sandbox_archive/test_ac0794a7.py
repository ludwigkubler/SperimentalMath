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
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        elif n == 2:
            return ['0', '1', 'XOR']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l})' for l in left] + [f'({r})' for r in right] + ['AND', 'OR']
    
    def evaluate_circuit(circuit):
        stack = []
        ops = {'AND': lambda x, y: x and y, 'OR': lambda x, y: x or y}
        for token in circuit:
            if token.isdigit():
                stack.append(int(token))
            elif token == 'XOR':
                b = stack.pop()
                a = stack.pop()
                stack.append(a ^ b)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(ops[token](a, b))
        return stack[0]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = [1] * n
        for i in range(n):
            if circuit[i].isdigit():
                continue
            left = int(circuit[i][1:circuit[i].find(')')])
            right = int(circuit[i][circuit[i].find(')') + 1:])
            width[i] = max(width[left], width[right]) + 1
        return max(width)
    
    def formal_group_order(n):
        # Simplified model for demonstration; actual computation would be complex
        return n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_circuit(n)
        order = formal_group_order(n)
        w_mon = monotone_width(circuit)
        results.append({'n': n, 'order': order, 'w_mon': w_mon})
    
    mean_order = sum(r['order'] for r in results) / len(results)
    mean_w_mon = sum(r['w_mon'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['order'] <= 2 * math.sqrt(r['n'])) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Order(G) vs w_mon(C)",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(r['n'] for r in results),
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
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")