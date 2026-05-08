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

def duval_algorithm(s):
    n = len(s)
    i, j, k = 0, 1, 2
    factors = []
    
    while i < n:
        if j >= n or s[i] < s[j]:
            factors.append(j - i)
            i = j
            j = k
            k += 1
        elif s[i] > s[j]:
            i = max(i + 1, k)
            j = k
            k += 1
        else:
            l = i
            while l < j and s[l] == s[j]:
                l += 1
            if l >= j:
                factors.append(j - i)
                i = j
                j = k
                k += 1
            else:
                d = j - l
                for m in range(i, l):
                    s[m], s[m + d] = s[m + d], s[m]
                i += d
                j += d
    
    factors.append(n - i)
    return factors

def generate_and_circuit(n):
    log_n = math.ceil(math.log2(n))
    and_gates = [random.sample(range(1, n+1), log_n + 2) for _ in range(n**2)]
    circuit = []
    for gate in and_gates:
        circuit.append(gate)
    return circuit

def generate_mod_3_circuit(n):
    def popcount(x):
        count = 0
        while x:
            count += x & 1
            x >>= 1
        return count
    
    mod_3_circuit = [popcount(i) % 3 == 0 for i in range(2**n)]
    return mod_3_circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12]
    results = []
    
    for n in n_values:
        circuit = generate_and_circuit(n)
        tt_circuit = [circuit[i] for i in range(2**n)]
        lyndon_factors_circuit = duval_algorithm(''.join(str(bit) for bit in tt_circuit))
        
        mod_3_circuit = generate_mod_3_circuit(n)
        lyndon_factors_mod_3 = duval_algorithm(''.join(str(bit) for bit in mod_3_circuit))
        
        results.append({
            "n": n,
            "lyndon_factors_circuit": len(lyndon_factors_circuit),
            "lyndon_factors_mod_3": len(lyndon_factors_mod_3)
        })
    
    mean_lyndon_factors_circuit = sum(result["lyndon_factors_circuit"] for result in results) / len(results)
    mean_lyndon_factors_mod_3 = sum(result["lyndon_factors_mod_3"] for result in results) / len(results)
    
    conjecture_holds = all(result["lyndon_factors_circuit"] <= 2**n / math.sqrt(n) and
                           result["lyndon_factors_mod_3"] >= 2**n / 8 for result in results)
    
    return {
        "metric_name": "Lyndon Factor Count",
        "metric_value": mean_lyndon_factors_circuit,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")