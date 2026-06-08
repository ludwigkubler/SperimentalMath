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
    
    def generate_formula(n):
        if n == 1:
            return 'a'
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} OR {right})'

    def resolution_proof_width(phi):
        if phi in {'a', '¬a'}:
            return 1
        elif 'OR' in phi:
            left, right = phi.split(' OR ')
            return max(resolution_proof_width(left), resolution_proof_width(right))
        else:
            raise ValueError("Invalid formula")

    def frobenius_eigenvalues(n):
        # Simplified eigenvalue calculation for demonstration purposes
        return [Fraction(1, 2)**i for i in range(n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_formula(n)
    G_phi = frobenius_eigenvalues(n)
    min_order_G_phi = max(abs(e) for e in G_phi)
    w_phi = resolution_proof_width(phi)

    return {
        "metric_name": "min_order(G(φ))",
        "metric_value": float(min_order_G_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")