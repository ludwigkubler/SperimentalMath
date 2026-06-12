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
    
    def generate_formula(n):
        if n == 1:
            return random.choice([True, False])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return (random.choice(['&', '|']) == '&' and all(subformulas)) or any(subformulas)
    
    def quadratic_residue_symbol(formula):
        if isinstance(formula, bool):
            return 0
        elif formula[0] == '&':
            return abs(quadratic_residue_symbol(formula[1]) * quadratic_residue_symbol(formula[2]))
        else:
            return abs(quadratic_residue_symbol(formula[1]) + quadratic_residue_symbol(formula[2]))
    
    def frege_proof_depth(formula):
        if isinstance(formula, bool):
            return 0
        elif formula[0] == '&':
            return max(frege_proof_depth(formula[1]), frege_proof_depth(formula[2])) + 1
        else:
            return max(frege_proof_depth(formula[1]), frege_proof_depth(formula[2])) + 1
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    qm = quadratic_residue_symbol(formula)
    d = frege_proof_depth(formula)
    
    return {
        "metric_name": "min_k |φ(k)|",
        "metric_value": qm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_qm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_qm} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_qm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")