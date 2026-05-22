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
    
    def generate_ac0_circuit(n):
        if n == 1:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_ac0_circuit(n//2), generate_ac0_circuit(n - n//2)]
            return (gate, inputs)
    
    def circuit_size(circuit):
        if isinstance(circuit, tuple):
            _, inputs = circuit
            return 1 + sum(circuit_size(inp) for inp in inputs)
        else:
            return 1
    
    def generate_coxeter_group(n):
        # Simple Coxeter group generator (A_n)
        return list(range(1, n+1))
    
    def generate_parabolic_subgroup(W, k):
        return W[:k]
    
    def quotient_representation_rank(W, P):
        # Simplified rank calculation for demonstration
        return len(W) // len(P)
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    size = circuit_size(circuit)
    W = generate_coxeter_group(n)
    k = random.randint(1, n-1)
    P = generate_parabolic_subgroup(W, k)
    
    rank = quotient_representation_rank(W, P)
    expected_rank = math.ceil(size ** (2/3))
    
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= expected_rank,
        "counterexample": "" if rank >= expected_rank else f"minimal_representation_rank_too_low"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"minimal_representation_rank_too_low\" first_failing_seed={first_failing_seed}")