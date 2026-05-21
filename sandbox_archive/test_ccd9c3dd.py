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
            if gate[0] == 'AND':
                a = stack.pop()
                b = stack.pop()
                stack.append(a and b)
            elif gate[0] == 'OR':
                a = stack.pop()
                b = stack.pop()
                stack.append(a or b)
            elif gate[0] == '⊕':
                a = stack.pop()
                b = stack.pop()
                stack.append(a != b)
        return stack[0]
    
    def walsh_hadamard_transform(f, n):
        N = 2**n
        f_hat = [0] * N
        for k in range(N):
            sum_val = 0
            for j in range(N):
                sum_val += (-1)**(k & j) * f[j]
            f_hat[k] = Fraction(sum_val, N)
        return f_hat
    
    def hamming_weight(x):
        return bin(x).count('1')
    
    def doubling_gap(f_hat):
        HF = [S for S in range(len(f_hat)) if abs(f_hat[S]) >= 1/4]
        return len(HF) / max(1, len(HF))
    
    n_values = [16, 24, 32, 40]
    results = []
    
    for n in n_values:
        k = math.ceil(math.log2(n))
        num_instances = 30
        acc_doubles = []
        sipser_doubles = []
        
        for _ in range(num_instances):
            # Generate random depth-3 AC⁰[⊕] circuit
            s = int(n**1.5)
            d = 3
            circuit = []
            for _ in range(s):
                gate_type = random.choice(['AND', 'OR', '⊕'])
                if gate_type == '⊕':
                    fan_in = min(2, int(math.sqrt(n)))
                else:
                    fan_in = 1
                inputs = [random.randint(0, 1) for _ in range(fan_in)]
                circuit.append((gate_type, *inputs))
            
            # Evaluate on all surviving inputs
            f = [evaluate_circuit(circuit, i) for i in range(2**k)]
            f_hat = walsh_hadamard_transform(f, k)
            acc_doubles.append(doubling_gap(f_hat))
        
        results.extend(acc_doubles)
    
    if len(results) < 120:
        return {
            "metric_name": "Doubling Gap",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    acc_median_double = sorted(results)[:len(results)//2][-1]
    sipser_median_double = sorted(results[len(results)//2:])[len(results)//2:]
    
    return {
        "metric_name": "Doubling Gap",
        "metric_value": acc_median_double,
        "instances_tested": len(results),
        "conjecture_holds": acc_median_double <= (1 + math.log(30))**6 and sipser_median_double >= math.sqrt(math.log(40))/6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    acc_doubles = [r["metric_value"] for r in results if r["conjecture_holds"]]
    sipser_doubles = [r["metric_value"] for r in results if r["conjecture_holds"]]
    
    support_fraction = len(acc_doubles) / len(results)
    mean_double = sum(acc_doubles) / len(acc_doubles) if acc_doubles else None
    std_double = math.sqrt(sum((x - mean_double)**2 for x in acc_doubles)) / len(acc_doubles) if acc_doubles else None
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_double} std={std_double} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"median Doub(ACC[2]) or Doub(Sipser_n) violated\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")