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
    n_values = [16, 24, 32, 40]
    results = []
    
    for n in n_values:
        k = math.ceil(math.log2(n))
        instances_tested = 0
        
        def walsh_hadamard_transform(f):
            N = len(f)
            if N == 1:
                return f
            even = walsh_hadamard_transform([f[i] + f[i+N//2] for i in range(N//2)])
            odd = walsh_hadamard_transform([f[i] - f[i+N//2] for i in range(N//2)])
            return [even[i] + odd[i] for i in range(N//2)] + [even[i] - odd[i] for i in range(N//2)]
        
        def random_ac0plus_circuit(n):
            size = int(math.floor(n**1.5))
            depth = 3
            circuit = []
            for _ in range(size):
                gate_type = random.choice(['AND', 'OR', '⊕'])
                if gate_type == '⊕':
                    fan_in = random.randint(2, math.isqrt(n))
                else:
                    fan_in = random.randint(1, math.isqrt(n))
                circuit.append((gate_type, fan_in))
            return circuit
        
        def evaluate_circuit(circuit, inputs):
            stack = []
            for gate in reversed(circuit):
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
                    stack.append(a ^ b)
            return stack[0]
        
        def random_sipser_function(n):
            return [i % 2 for i in range(1, n+1)]
        
        def compute_doub(f):
            f_hadamard = walsh_hadamard_transform(f)
            hf = {S: sum(f_hadamard[i] for i in S) / len(f_hadamard) for S in itertools.combinations(range(n), k)}
            hf_filtered = {S: v for S, v in hf.items() if abs(v) >= 1/4}
            return sum(abs(hf[S]) - abs(hf[S^i]) for i in range(1, 2**k)) / max(1, len(hf_filtered))
        
        random.seed(seed)
        
        for _ in range(30):
            if n == 16:
                circuit = random_ac0plus_circuit(n)
            else:
                circuit = random_sipser_function(n)
            
            f = [evaluate_circuit(circuit, i) for i in range(2**k)]
            doub = compute_doub(f)
            
            results.append({
                "n": n,
                "doub": doub
            })
    
    mean_doub = sum(result["doub"] for result in results) / len(results)
    std_doub = math.sqrt(sum((result["doub"] - mean_doub)**2 for result in results) / len(results))
    conjecture_holds = all(result["doub"] <= (1 + math.log2(size))**(6 if n == 16 else 4) for result in results)
    
    return {
        "metric_name": "Doub",
        "metric_value": mean_doub,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, doub={result['doub']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_doub = sum(result["metric_value"] for result in results) / len(results)
    std_doub = math.sqrt(sum((result["metric_value"] - mean_doub)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_doub} std={std_doub} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")