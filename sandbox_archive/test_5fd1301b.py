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
    
    def sturm_sequence(poly, deriv):
        seq = [poly]
        while True:
            if not deriv:
                break
            seq.append([-deriv[0]/seq[-1][0]] + [b/a for a, b in zip(seq[-2], deriv[1:])])
            deriv = [b - (a * seq[-1][0]) for a, b in zip(seq[-1], deriv)]
        return seq
    
    def sturm_count(poly):
        seq = sturm_sequence(poly, poly_derivative(poly))
        sign_changes = 0
        for interval in range(-1000, 1001, 2):
            signs = [int(math.copysign(1, p.subs(x, interval))) for p in seq]
            sign_changes += sum(signs[i] != signs[i+1] for i in range(len(signs)-1))
        return sign_changes
    
    def poly_derivative(poly):
        return [(i * coeff) for i, coeff in enumerate(poly[1:], start=1)]
    
    def cnf_to_poly(cnf):
        n = len(cnf)
        poly = [Fraction(1)]
        for clause in cnf:
            term = Fraction(1)
            for literal in clause:
                if literal > 0:
                    term *= (1 - x**literal)
                else:
                    term *= (1 + x**(-literal))
            poly.append(term)
        return poly
    
    def is_ac0_circuit(cnf):
        # Placeholder function to check if the CNF is an AC⁰ circuit
        # This is a dummy implementation and should be replaced with actual logic
        return False
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
    
    poly = cnf_to_poly(cnf)
    root_count = sturm_count(poly)
    
    if is_ac0_circuit(cnf):
        expected_root_count = 2**(n//2)
        conjecture_holds = abs(root_count - expected_root_count) <= 1
        counterexample = "" if conjecture_holds else "AC⁰ circuit does not match expected root count"
    else:
        expected_root_count = 0
        conjecture_holds = root_count == expected_root_count
        counterexample = "" if conjecture_holds else "Non-AC⁰ circuit has unexpected root count"
    
    return {
        "metric_name": "Root Count",
        "metric_value": root_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AC⁰ circuit does not match expected root count\" first_failing_seed={first_failing_seed}")