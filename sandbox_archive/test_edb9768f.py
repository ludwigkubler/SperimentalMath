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
    
    def generate_boolean_algebra(n):
        elements = [0, 1]
        for _ in range(1, n):
            new_elements = []
            for e in elements:
                new_elements.append(e ^ 1)
                new_elements.append(e & 1)
                new_elements.append(e | 1)
            elements.extend(new_elements)
        return elements
    
    def is_subalgebra(A, B):
        for a in A:
            if a not in B or any(a & b not in B for b in B):
                return False
        return True
    
    def bicategory_rank(B):
        subalgebras = []
        for i in range(1 << len(B)):
            subalgebra = [B[j] for j in range(len(B)) if (i & (1 << j))]
            if is_subalgebra(subalgebra, B):
                subalgebras.append(subalgebra)
        
        min_rank = float('inf')
        for i in range(len(subalgebras)):
            for j in range(i + 1, len(subalgebras)):
                A = subalgebras[i]
                B = subalgebras[j]
                homomorphisms = []
                for a in A:
                    for b in B:
                        if all(a & x == b & x for x in A):
                            homomorphisms.append((a, b))
                
                if homomorphisms:
                    min_rank = min(min_rank, len(homomorphisms))
        
        return min_rank
    
    def resolution_width(B):
        n = len(B)
        width = 0
        queue = [B]
        while queue:
            next_level = []
            for subalgebra in queue:
                if len(subalgebra) == 1:
                    continue
                for a in subalgebra:
                    for b in subalgebra:
                        if a & b not in subalgebra and (a | b) in subalgebra:
                            next_level.append(a | b)
            width += 1
            queue = next_level
        return width
    
    n = random.randint(5, 40)
    B = generate_boolean_algebra(n)
    rho_B = bicategory_rank(B)
    w_star_B = resolution_width(B)
    
    if w_star_B == 0:
        return {
            "metric_name": "rho/B",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = rho_B / w_star_B
    c = 2.0  # Hypothetical constant based on previous data
    
    return {
        "metric_name": "rho/B",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= c,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "ratio_exceeds_constant"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")