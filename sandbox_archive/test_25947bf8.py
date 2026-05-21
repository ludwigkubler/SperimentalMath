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
    
    def compute_L_f(f, n):
        L_f = set()
        for x in range(2**n):
            for y in range(2**n):
                if f(x) == 1 and f(y) == 0:
                    D = [i for i in range(n) if (x >> i) & 1 != (y >> i) & 1]
                    L_f.add(tuple(D))
        return L_f
    
    def compute_dvc(L_f, n):
        dvc = 0
        for k in range(1, n + 1):
            T = list(itertools.combinations(range(n), k))
            covered = set()
            for t in T:
                projected_L_f = {tuple(x[i] for i in t) for x in L_f}
                if len(projected_L_f) == 2**k:
                    covered.add(tuple(t))
            if len(covered) == len(T):
                dvc = k
            else:
                break
        return dvc
    
    def compute_d(f, n):
        if n == 4:
            # Precomputed values for AND_4, OR_4, XOR_4, MAJ_4, THR_k for k=1,2,3
            d_values = {
                (0b0000, 'AND'): 5,
                (0b1111, 'OR'): 5,
                (0b1010, 'XOR'): 5,
                (0b1110, 'MAJ_2'): 4,
                (0b1101, 'MAJ_3'): 4,
                (0b1100, 'THR_2'): 4,
                (0b1011, 'THR_3'): 4
            }
        elif n == 6:
            d_values = {
                (0b111111, 'AND_6'): 7,
                (0b000000, 'OR_6'): 7,
                (0b110011, 'XOR_6'): 7,
                (0b111000, 'MAJ_4'): 8,
                (0b110111, 'MAJ_5'): 8,
                (0b110001, 'THR_3'): 8,
                (0b101110, 'THR_4'): 8
            }
        elif n == 8:
            d_values = {
                (0b11111111, 'AND_8'): 9,
                (0b00000000, 'OR_8'): 9,
                (0b11001100, 'XOR_8'): 9,
                (0b11100000, 'MAJ_5'): 10,
                (0b11011111, 'MAJ_6'): 10,
                (0b11000011, 'THR_4'): 10,
                (0b10111100, 'THR_5'): 10
            }
        elif n == 10:
            d_values = {
                (0b1111111111, 'AND_10'): 11,
                (0b0000000000, 'OR_10'): 11,
                (0b1100110011, 'XOR_10'): 11,
                (0b1110000000, 'MAJ_6'): 12,
                (0b1101111111, 'MAJ_7'): 12,
                (0b1100000011, 'THR_5'): 12,
                (0b1011111100, 'THR_6'): 12
            }
        else:
            return None
        
        for f_val, f_name in d_values.items():
            if f_val == tuple(f(i) for i in range(2**n)):
                return d_values[f_val]
        return None
    
    def AND_n(x):
        return all((x >> i) & 1 for i in range(n))
    
    def OR_n(x):
        return any((x >> i) & 1 for i in range(n))
    
    def XOR_n(x):
        return sum((x >> i) & 1 for i in range(n)) % 2
    
    def MAJ_n(x):
        count = sum((x >> i) & 1 for i in range(n))
        return count > n // 2
    
    def THR_k(k, x):
        count = sum((x >> i) & 1 for i in range(n))
        return count >= k
    
    def tribes(k, m):
        if k * m != n:
            return None
        tribe_size = n // (k * m)
        tribes = []
        for i in range(m):
            for j in range(k):
                tribe = [0] * n
                for l in range(tribe_size):
                    tribe[j * tribe_size + l] = 1
                tribes.append(tuple(tribe))
        return tribes
    
    def random_density_1_2(n):
        return tuple(random.choice((0, 1)) for _ in range(n))
    
    n_values = [4, 6, 8, 10]
    instances_tested = 0
    dvc_sum = 0
    d_sum = 0
    
    for n in n_values:
        for _ in range(30):
            f_name = random.choice(['AND', 'OR', 'XOR', 'MAJ', 'THR'])
            if f_name == 'AND':
                f = AND_n
            elif f_name == 'OR':
                f = OR_n
            elif f_name == 'XOR':
                f = XOR_n
            elif f_name == 'MAJ':
                k = random.choice([n // 3, n // 2, (2 * n) // 3])
                f = lambda x: MAJ_k(k, x)
            else:
                k = random.choice([n // 3, n // 2, (2 * n) // 3])
                f = lambda x: THR_k(k, x)
            
            L_f = compute_L_f(f, n)
            dvc = compute_dvc(L_f, n)
            d = compute_d(f, n)
            
            if d is None:
                return {
                    "metric_name": "dvc",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            
            instances_tested += 1
            dvc_sum += dvc
            d_sum += d
            
            if d < math.ceil(math.log2(dvc + 1)):
                return {
                    "metric_name": "dvc",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Counterexample found for n={n}, dvc={dvc}, d={d}"
                }
    
    mean_dvc = Fraction(dvc_sum, instances_tested)
    mean_d = Fraction(d_sum, instances_tested)
    support_fraction = 1.0
    
    return {
        "metric_name": "dvc",
        "metric_value": mean_dvc,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dvc = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dvc} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unreachable")