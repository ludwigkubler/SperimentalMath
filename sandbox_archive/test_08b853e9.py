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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_size(f):
        n = len(f)
        max_length = 5 * n
        count = 0
        for length in range(1, max_length + 1):
            if length % 2 == 0:
                continue
            for proof in itertools.product([0, 1], repeat=length):
                if evaluate_proof(proof, f) == f[0]:
                    count += 1
        return count
    
    def evaluate_proof(proof, f):
        n = len(f)
        if len(proof) != n:
            return None
        x = 0
        for bit in proof:
            x = (2 * x + bit) % n
        return f[x]
    
    def geometric_entropy(morse_function):
        n = len(morse_function)
        grid_size = 100
        step = 1 / grid_size
        entropy = 0
        for i in range(grid_size):
            for j in range(grid_size):
                x, y = i * step, j * step
                value = morse_function(x, y)
                if value is not None:
                    prob = (value + 1) / 2
                    entropy -= prob * math.log2(prob) - (1 - prob) * math.log2(1 - prob)
        return entropy
    
    def morse_function(x, y):
        n = len(f)
        x_bin = bin(int(x))[2:].zfill(n)
        y_bin = bin(int(y))[2:].zfill(n)
        f_value = 0
        for i in range(n):
            if x_bin[i] == '1':
                f_value += f[2**i]
            if y_bin[i] == '1':
                f_value -= f[2**i]
        return f_value
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_entropy = 0
    total_proof_size = 0
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        proof_size = frege_proof_size(f)
        entropy = geometric_entropy(morse_function)
        
        if entropy <= proof_size:
            counterexample = "Entropy not greater than proof size"
            break
        
        total_instances += 1
        total_entropy += entropy
        total_proof_size += proof_size
    
    mean_entropy = total_entropy / total_instances if total_instances > 0 else 0
    mean_proof_size = total_proof_size / total_instances if total_instances > 0 else 0
    
    return {
        "metric_name": "Entropy vs Proof Size",
        "metric_value": mean_entropy,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": mean_entropy >= 0.7 * mean_proof_size,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 2**31-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")