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
            return [f'({x} & {y})' for x in left for y in right]
    
    def circuit_satisfiability_threshold(circuit):
        if isinstance(circuit, list):
            circuit = ' '.join(circuit)
        stack = []
        for token in circuit.split():
            if token == '0':
                stack.append('0')
            elif token == '1':
                stack.append('1')
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(f'({left} & {right})')
        return len(stack[0])
    
    def grammar_complexity(circuit):
        if isinstance(circuit, list):
            circuit = ' '.join(circuit)
        productions = {}
        for token in circuit.split():
            if '(' not in token:
                continue
            left, right = token[1:-1].split(' & ')
            if left not in productions:
                productions[left] = set()
            if right not in productions:
                productions[right] = set()
            productions[left].add(right)
        grammar_size = len(productions)
        return grammar_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        theta_C = circuit_satisfiability_threshold(circuit)
        g_L = grammar_complexity(circuit)
        metrics.append({
            'n': n,
            'theta_C': theta_C,
            'g_L': g_L
        })
    
    correlation_sum = 0
    g_L_sum = 0
    for metric in metrics:
        correlation_sum += (metric['theta_C'] - sum(m['theta_C'] for m in metrics) / len(metrics)) * \
                           (metric['g_L'] - sum(m['g_L'] for m in metrics) / len(metrics))
        g_L_sum += metric['g_L']
    
    n = len(metrics)
    correlation = correlation_sum / ((n - 1) * math.sqrt(sum((m['theta_C'] - sum(m['theta_C'] for m in metrics) / n) ** 2 for m in metrics)) *
                                      math.sqrt(sum((m['g_L'] - sum(m['g_L'] for m in metrics) / n) ** 2 for m in metrics)))
    
    if correlation > 0.8 and g_L_sum / n <= 3:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(metric['n'] for metric in metrics),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
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
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")