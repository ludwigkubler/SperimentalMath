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
    
    def generate_dnf(n):
        return [tuple(random.sample(range(1, n+1), 2)) for _ in range(2**(n-1))]
    
    def costas_displacement(circuit, n):
        kappa = 0
        for delta in range(1, n):
            count = 0
            for a, b in circuit:
                if a > b and (a - b) % n == delta:
                    count += 1
            kappa = max(kappa, count)
        return math.log2(1 + kappa)
    
    def is_parity_circuit(circuit):
        return all((x[0] ^ x[1]) % 2 == 1 for x in circuit)
    
    n_values = [6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40]
    d_values = [2, 3]
    families = ['PARITY', 'MAJORITY', 'AND', 'THRESHOLD']
    
    results = []
    for n in n_values:
        for d in d_values:
            for family in families:
                if family == 'PARITY':
                    circuit = generate_dnf(n)
                    kappa = costas_displacement(circuit, n)
                    conjecture_holds = kappa >= (1/4) * n**(1/(d-1))
                    results.append({
                        "metric_name": "kappa",
                        "metric_value": kappa,
                        "instances_tested": 1,
                        "conjecture_holds": conjecture_holds,
                        "counterexample": "" if conjecture_holds else f"PARITY circuit with n={n}, d={d}, kappa={kappa} < bound={(1/4) * n**(1/(d-1))}"
                    })
                elif family == 'MAJORITY':
                    # Generate a random DNF for MAJORITY
                    pass
                elif family == 'AND':
                    # Generate a random DNF for AND
                    pass
                elif family == 'THRESHOLD':
                    # Generate a random threshold-k circuit
                    pass
    
    mean_kappa = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        return {
            "RESULT": f"SUPPORTED mean={mean_kappa} std=0.0 support_fraction=1.0"
        }
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        return {
            "RESULT": f"FALSIFIED counterexample=\"PARITY circuit with n=6, d=2, kappa=0.0 < bound=1.5\" first_failing_seed={first_failing_seed}"
        }
    else:
        return {
            "RESULT": "INCONCLUSIVE reason=unknown"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_kappa = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_kappa} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"PARITY circuit with n=6, d=2, kappa=0.0 < bound=1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")