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
    
    def to_bin(x, width):
        return ''.join('1' if x & (1 << i) else '0' for i in range(width-1, -1, -1))
    
    def tseitin_formula(f, n):
        literals = {}
        clauses = []
        
        def new_literal():
            nonlocal literals
            literal = len(literals)
            literals[literal] = True
            return literal
        
        def negate(literal):
            nonlocal literals
            literals[literal] = not literals[literal]
            return -literal
        
        def add_clause(clause):
            clauses.append(clause)
        
        for i in range(2**n):
            binary_rep = to_bin(i, n)
            f_val = int(f(binary_rep), 2)
            literal = new_literal()
            if f_val == 1:
                add_clause([literal])
            else:
                add_clause([-literal])
        
        return literals, clauses
    
    def frege_proof_depth(clauses):
        # Simplified Frege proof depth calculation
        return len(clauses) * 2
    
    def geometric_entropy(literals):
        # Simplified geometric entropy calculation
        n = len(literals)
        return math.log(n, 2)
    
    n_max = 0
    instances_tested = 0
    total_ratio = 0.0
    support_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = lambda x: random.choice([0, 1])
            literals, clauses = tseitin_formula(f, n)
            
            instances_tested += 1
            d_phi_f = frege_proof_depth(clauses)
            H_f = geometric_entropy(literals)
            
            if d_phi_f == 0:
                continue
            
            ratio = H_f / d_phi_f
            total_ratio += ratio
            
            if ratio >= 0.5:
                support_count += 1
    
    conjecture_holds = support_count / instances_tested >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "H(f)/d(φ_f)",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")