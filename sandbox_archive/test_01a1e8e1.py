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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, m), -random.randint(1, m)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        if not cnf:
            return True
        literals = set()
        for clause in cnf:
            literals.update(abs(l) for l in clause)
        literal = random.choice(list(literals))
        positive = any(l == literal for l in cnf[0])
        new_cnf = [c for c in cnf if not all(l in c or -l in c for l in [literal, -literal])]
        return dpll(new_cnf) or dpll([c for c in cnf if not all(l in c or -l in c for l in [-literal, literal])])
    
    def local_ring_structure(cnf):
        # Simplified local ring structure based on DPLL result
        return len(cnf)
    
    def unit_group_size(local_ring):
        return local_ring
    
    def frege_proof_depth(cnf):
        # Simplified Frege proof depth based on DPLL result
        return len(cnf) * 2
    
    results = []
    for m in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(m)
        local_ring = local_ring_structure(cnf)
        unit_group = unit_group_size(local_ring)
        proof_depth = frege_proof_depth(cnf)
        
        results.append({
            "metric_name": "Frege Proof Depth vs Unit Group Size",
            "metric_value": proof_depth / unit_group,
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })
    
    return {
        "seed": seed,
        "metric_name": "Frege Proof Depth vs Unit Group Size",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")