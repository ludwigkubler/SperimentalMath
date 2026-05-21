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
    
    def evaluate_circuit(circuit, input):
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
            else:
                stack.append(gate(input))
        return stack[0]
    
    def walsh_hadamard_transform(f, n):
        N = 2**n
        result = [0] * N
        for i in range(N):
            for j in range(N):
                result[i] += f(j) * (-1)**(i & j)
        return [x / math.sqrt(N) for x in result]
    
    def hamming_weight(x):
        return bin(x).count('1')
    
    def freiman_family_size(k, n):
        return 2**(n - k + 1)
    
    def doubling(g, tau=0.25):
        N = len(g)
        HF = [g[i] for i in range(N) if abs(g[i]) >= tau]
        return sum(abs(HF[i] - HF[j]) for i in range(len(HF)) for j in range(i+1, len(HF))) / max(1, len(HF))
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR', '⊕'])
            if gate == '⊕':
                circuit.append(lambda x: x % 2)
            else:
                circuit.append(random.randint(0, n-1))
        return circuit
    
    def sipser_function(n, i):
        return (i & (i + 1)) != 0
    
    n_values = [16, 24, 32, 40]
    k_values = [math.ceil(math.log2(n)) for n in n_values]
    
    total_doubling_acc = []
    total_doubling_sipser = []
    
    for n, k in zip(n_values, k_values):
        s = math.floor(n**1.5)
        circuit = generate_random_circuit(s)
        
        for _ in range(30):
            k_window = random.sample(range(n), k)
            f_acc = [evaluate_circuit(circuit, i) for i in k_window]
            g_acc = walsh_hadamard_transform(f_acc, k)
            total_doubling_acc.append(doubling(g_acc))
            
            f_sipser = [sipser_function(n, i) for i in range(2**n)]
            g_sipser = walsh_hadamard_transform(f_sipser, n)
            total_doubling_sipser.append(doubling(g_sipser))
    
    median_doubling_acc = sorted(total_doubling_acc)[len(total_doubling_acc) // 2]
    median_doubling_sipser = sorted(total_doubling_sipser)[len(total_doubling_sipser) // 2]
    
    conjecture_holds = (median_doubling_acc <= (1 + math.log2(s))**6 and
                        median_doubling_sipser >= math.sqrt(math.log2(n))/6)
    
    return {
        "metric_name": "Doubling Gap",
        "metric_value": median_doubling_acc,
        "instances_tested": len(total_doubling_acc),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"ACC: {median_doubling_acc}, Sipser: {median_doubling_sipser}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_doubling_acc = [r["metric_value"] for r in results if "ACC" in r["counterexample"]]
    total_doubling_sipser = [r["metric_value"] for r in results if "Sipser" in r["counterexample"]]
    
    mean_doubling_acc = sum(total_doubling_acc) / len(total_doubling_acc)
    std_doubling_acc = math.sqrt(sum((x - mean_doubling_acc)**2 for x in total_doubling_acc) / len(total_doubling_acc))
    support_fraction_acc = sum(1 for r in results if "ACC" not in r["counterexample"]) / len(results)
    
    mean_doubling_sipser = sum(total_doubling_sipser) / len(total_doubling_sipser)
    std_doubling_sipser = math.sqrt(sum((x - mean_doubling_sipser)**2 for x in total_doubling_sipser) / len(total_doubling_sipser))
    support_fraction_sipser = sum(1 for r in results if "Sipser" not in r["counterexample"]) / len(results)
    
    if all("ACC" not in r["counterexample"] and "Sipser" not in r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_doubling_acc} std={std_doubling_acc} support_fraction={support_fraction_acc}")
    elif any("ACC" in r["counterexample"] for r in results) and all("Sipser" not in r["counterexample"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"ACC\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if 'ACC' in r['counterexample'])]}")
    elif any("Sipser" in r["counterexample"] for r in results) and all("ACC" not in r["counterexample"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Sipser\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if 'Sipser' in r['counterexample'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")