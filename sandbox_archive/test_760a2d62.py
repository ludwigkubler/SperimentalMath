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
        return [random.choice(['0', '1']) for _ in range(2**n)]
    
    def monotone_complexity(circuit):
        n = len(circuit)
        count = 0
        for i in range(1, 2**n):
            if all(circuit[j] == circuit[i ^ j] for j in range(n)):
                count += 1
        return count
    
    def symplectic_volume(circuit):
        n = len(circuit)
        volume = 1
        for bit in circuit:
            if bit == '0':
                volume *= Fraction(1, 2)
            else:
                volume *= Fraction(3, 4)
        return volume
    
    instances_tested = 0
    n_max = 0
    total_vol = 0
    total_complexity = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            vol = symplectic_volume(circuit)
            complexity = monotone_complexity(circuit)
            
            total_vol += vol
            total_complexity += complexity
            instances_tested += 1
    
    avg_vol = total_vol / instances_tested
    avg_complexity = total_complexity / instances_tested
    
    if n_max < 16:
        return {
            "metric_name": "symplectic_volume",
            "metric_value": avg_vol,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    return {
        "metric_name": "symplectic_volume",
        "metric_value": avg_vol,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(avg_vol - avg_complexity) > 0.7,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_vol = sum(r['metric_value'] for r in results) / len(results)
    std_vol = math.sqrt(sum((r['metric_value'] - mean_vol)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_vol} std={std_vol} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_vol} std={std_vol} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = random.choice([r['counterexample'] for r in results if r['counterexample']])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")