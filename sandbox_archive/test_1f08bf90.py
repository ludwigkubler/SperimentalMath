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
    
    def evaluate_circuit(circuit, input_val):
        stack = []
        for gate in circuit:
            if gate == 'AND':
                a = stack.pop()
                b = stack.pop()
                stack.append(a and b)
            elif gate == 'OR':
                a = stack.pop()
                b = stack.pop()
                stack.append(a or b)
            elif gate == '⊕':
                a = stack.pop()
                b = stack.pop()
                stack.append(a != b)
        return stack[0]
    
    def walsh_hadamard_transform(f, k):
        n = 2**k
        f_values = [f(i) for i in range(n)]
        
        # Compute the Walsh-Hadamard transform
        for s in range(k):
            for j in range(2**(s+1)):
                for t in range(2**s):
                    if (j // 2**s + t) % 2 == 0:
                        f_values[j] += f_values[j + 2**s]
                    else:
                        f_values[j] -= f_values[j + 2**s]
        
        # Normalize
        for j in range(n):
            f_values[j] /= n
        
        return f_values
    
    def hamming_distance(set1, set2):
        return len(set1.symmetric_difference(set2))
    
    def doubling_gap(f_values):
        S = [i for i, val in enumerate(f_values) if abs(val) >= 0.25]
        return hamming_distance(S, set(range(len(f_values))))
    
    n_values = [16, 24, 32, 40]
    results = []
    
    for n in n_values:
        k = math.ceil(math.log2(n))
        s = int(n**1.5)
        
        # Generate random depth-3 AC⁰[⊕] circuit
        circuit = []
        for _ in range(s):
            gate = random.choice(['AND', 'OR', '⊕'])
            if gate == '⊕':
                circuit.append(gate)
            else:
                circuit.append(random.choice([0, 1]))
        
        # Generate Sipser function
        sipser_circuit = ['AND'] * (k - 2) + ['OR'] + ['AND'] * (k - 3)
        
        for _ in range(30):
            k_window = random.sample(range(n), k)
            f_acc = [evaluate_circuit(circuit, i) for i in k_window]
            f_sipser = [evaluate_circuit(sipser_circuit, i) for i in k_window]
            
            ghf_acc = walsh_hadamard_transform(f_acc, k)
            ghf_sipser = walsh_hadamard_transform(f_sipser, k)
            
            doubling_acc = doubling_gap(ghf_acc)
            doubling_sipser = doubling_gap(ghf_sipser)
            
            results.append({
                "n": n,
                "doubling_acc": doubling_acc,
                "doubling_sipser": doubling_sipser
            })
    
    # Compute metrics
    acc_doublings = [res["doubling_acc"] for res in results]
    sipser_doublings = [res["doubling_sipser"] for res in results]
    
    mean_acc_doubling = sum(acc_doublings) / len(acc_doublings)
    std_acc_doubling = (sum((x - mean_acc_doubling)**2 for x in acc_doublings) / len(acc_doublings))**0.5
    mean_sipser_doubling = sum(sipser_doublings) / len(sipser_doublings)
    std_sipser_doubling = (sum((x - mean_sipser_doubling)**2 for x in sipser_doublings) / len(sipser_doublings))**0.5
    
    # Check conjecture
    acc_support = all(d <= (1 + math.log2(s))**6 for d, s in zip(acc_doublings, [int(n**1.5) for n in n_values]))
    sipser_support = all(d >= math.sqrt(math.log2(n)) / 6 for d, n in zip(sipser_doublings, n_values))
    
    if acc_support and sipser_support:
        return {
            "metric_name": "Doubling Gap",
            "metric_value": mean_acc_doubling,
            "instances_tested": len(acc_doublings),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for res in results:
            if not acc_support and res["doubling_acc"] > (1 + math.log2(int(res["n"]**1.5)))**6:
                return {
                    "metric_name": "Doubling Gap",
                    "metric_value": mean_acc_doubling,
                    "instances_tested": len(acc_doublings),
                    "conjecture_holds": False,
                    "counterexample": f"ACC[2] doubling gap exceeds bound for n={res['n']}"
                }
            elif not sipser_support and res["doubling_sipser"] < math.sqrt(math.log2(res["n"])) / 6:
                return {
                    "metric_name": "Doubling Gap",
                    "metric_value": mean_sipser_doubling,
                    "instances_tested": len(sipser_doublings),
                    "conjecture_holds": False,
                    "counterexample": f"Sipser function doubling gap below bound for n={res['n']}"
                }
    
    return {
        "metric_name": "Doubling Gap",
        "metric_value": mean_acc_doubling,
        "instances_tested": len(acc_doublings),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")