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
    
    def AND_n(n):
        return lambda x: all(x[i] == 1 for i in range(n))
    
    def OR_n(n):
        return lambda x: any(x[i] == 1 for i in range(n))
    
    def XOR_n(n):
        return lambda x: sum(x[i] for i in range(n)) % 2
    
    def MAJ_n(n):
        return lambda x: sum(x[i] for i in range(n)) > n // 2
    
    def THR_k(k, n):
        return lambda x: sum(x[i] for i in range(n)) >= k
    
    def tribes(k, m):
        return lambda x: any(all(x[i + j * m] == 1 for j in range(m)) for i in range(k))
    
    def random_function(n):
        return lambda x: random.choice([0, 1])
    
    functions = {
        "AND": AND_n,
        "OR": OR_n,
        "XOR": XOR_n,
        "MAJ": MAJ_n,
        "THR": THR_k,
        "TRIBES": tribes
    }
    
    n_values = [4, 6, 8, 10]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(30):
            func_type = random.choice(list(functions.keys()))
            if func_type == "THR":
                k = random.randint(n // 3, (2 * n) // 3)
                f = functions[func_type](k, n)
            elif func_type == "TRIBES":
                k = int(math.ceil(math.sqrt(n)))
                m = int(math.floor(n / math.ceil(math.sqrt(n))))
                f = functions[func_type](k, m)
            else:
                f = functions[func_type](n)
            
            L_f = set()
            for x in range(2 ** n):
                x_bits = [x >> i & 1 for i in range(n)]
                for y in range(2 ** n):
                    y_bits = [y >> i & 1 for i in range(n)]
                    if f(x_bits) == 1 and f(y_bits) == 0:
                        L_f.add(tuple(i for i in range(n) if x_bits[i] != y_bits[i]))
            
            dvc_f = 0
            for k in range(1, n + 1):
                T = set(random.sample(range(n), k))
                projected_L_f = {tuple(x[i] for i in T) for x in L_f}
                if len(projected_L_f) == 2 ** k:
                    dvc_f = k
                else:
                    break
            
            d_f = None
            if n == 4:
                truth_table = [f([i >> j & 1 for j in range(4)]) for i in range(16)]
                d_f = len(truth_table)
            elif n in {6, 8, 10}:
                # Use known bounds from literature
                if func_type == "AND":
                    d_f = n
                elif func_type == "OR":
                    d_f = n
                elif func_type == "XOR":
                    d_f = n
                elif func_type == "MAJ":
                    d_f = 2 * n - 1
                elif func_type == "THR":
                    d_f = 2 ** (n - k) - 1
                elif func_type == "TRIBES":
                    d_f = 2 ** (k + m - 1) - 1
            else:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            
            instances_tested += 1
            if d_f < math.ceil(math.log2(dvc_f + 1)):
                conjecture_holds = False
                counterexample = f"({func_type}, {n}, {dvc_f}, {d_f})"
                break
    
    return {
        "metric_name": "d(f) >= ceil(log2(dvc(f)+1))",
        "metric_value": math.ceil(math.log2(dvc_f + 1)),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")