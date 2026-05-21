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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def continued_fraction_length(numerator, denominator):
    length = 0
    while numerator != 0:
        quotient = numerator // denominator
        numerator, denominator = denominator - quotient * numerator, numerator
        length += 1
    return length

def random_acc0_circuit(size, depth):
    if size == 1:
        return [random.choice([0, 1])]
    elif size == 2:
        return [random.choice([0, 1]), random.choice([0, 1])]
    else:
        circuit = []
        for _ in range(depth):
            gate_type = random.choice(['AND', 'OR', 'MOD_2'])
            if gate_type == 'AND':
                circuit.append('AND')
                circuit.extend(random_acc0_circuit(size // 2, depth - 1))
            elif gate_type == 'OR':
                circuit.append('OR')
                circuit.extend(random_acc0_circuit(size // 2, depth - 1))
            else:
                circuit.append('MOD_2')
                circuit.extend(random_acc0_circuit(size // 2, depth - 1))
        return circuit

def evaluate_circuit(circuit, input_values):
    stack = []
    for gate in reversed(circuit):
        if gate == 'AND':
            a = stack.pop()
            b = stack.pop()
            stack.append(a and b)
        elif gate == 'OR':
            a = stack.pop()
            b = stack.pop()
            stack.append(a or b)
        elif gate == 'MOD_2':
            a = stack.pop()
            b = stack.pop()
            stack.append((a + b) % 2)
        else:
            stack.append(gate)
    return stack[0]

def run_trial(seed: int):
    random.seed(seed)
    
    n_values = [12, 15, 18]
    results = {'metric_name': 'D(f)', 'instances_tested': 0, 'conjecture_holds': True, 'counterexample': ''}
    
    for n in n_values:
        for s in [20, 40, 80]:
            for d in [2, 3, 4]:
                for _ in range(10):
                    if time.time() + 6 > end_time:
                        return {'metric_name': 'D(f)', 'instances_tested': results['instances_tested'], 'conjecture_holds': False, 'counterexample': 'budget_exceeded'}
                    
                    circuit = random_acc0_circuit(s, d)
                    input_values = [random.randint(0, 1) for _ in range(n)]
                    output = evaluate_circuit(circuit, input_values)
                    probability = sum(evaluate_circuit(circuit, input_values[:i] + [output] + input_values[i+1:]) for i in range(n)) / (2 ** n)
                    
                    p_i, q_i = probability, 1
                    for _ in range(ceil(log2(n))):
                        max_diff = -inf
                        best_var, best_val = None, None
                        for var in range(n):
                            for val in [0, 1]:
                                new_prob = sum(evaluate_circuit(circuit[:i] + [val] + circuit[i+1:]) for i in range(var)) / (2 ** var)
                                diff = abs(new_prob - 0.5)
                                if diff > max_diff:
                                    max_diff = diff
                                    best_var, best_val = var, val
                        p_i, q_i = new_prob, 1
                    
                    D_f += continued_fraction_length(p_i, q_i)
                    results['instances_tested'] += 1
        
        if n == 18:
            for _ in range(5):
                if time.time() + 6 > end_time:
                    return {'metric_name': 'D(f)', 'instances_tested': results['instances_tested'], 'conjecture_holds': False, 'counterexample': 'budget_exceeded'}
                
                circuit = random_acc0_circuit(s, d)
                input_values = [random.randint(0, 1) for _ in range(n)]
                output = evaluate_circuit(circuit, input_values)
                probability = sum(evaluate_circuit(circuit, input_values[:i] + [output] + input_values[i+1:]) for i in range(n)) / (2 ** n)
                
                p_i, q_i = probability, 1
                for _ in range(ceil(log2(n))):
                    max_diff = -inf
                    best_var, best_val = None, None
                    for var in range(n):
                        for val in [0, 1]:
                            new_prob = sum(evaluate_circuit(circuit[:i] + [val] + circuit[i+1:]) for i in range(var)) / (2 ** var)
                            diff = abs(new_prob - 0.5)
                            if diff > max_diff:
                                max_diff = diff
                                best_var, best_val = var, val
                    p_i, q_i = new_prob, 1
                
                D_f += continued_fraction_length(p_i, q_i)
                results['instances_tested'] += 1
    
    return results

if __name__ == "__main__":
    import sys
    import time
    from math import ceil, log2, inf
    
    if len(sys.argv) > 1:
        seeds = [int(x) for x in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    end_time = time.time() + 240
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    D_f_values = [r['metric_value'] for r in results if 'metric_value' in r]
    conjecture_holds_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(D_f_values)/len(D_f_values)} std={math.sqrt(sum((x - sum(D_f_values)/len(D_f_values))**2 for x in D_f_values) / len(D_f_values))} support_fraction=1.0")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(D_f_values)/len(D_f_values)} std={math.sqrt(sum((x - sum(D_f_values)/len(D_f_values))**2 for x in D_f_values) / len(D_f_values))} support_fraction={conjecture_holds_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")