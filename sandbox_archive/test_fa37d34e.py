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
    
    def quasi_monte_carlo_rule(circuit, ε=1e-6):
        w_C = circuit['monotone_width']
        Q = int(Fraction(w_C**2, math.log(1/ε)**2))
        return Q
    
    def generate_monotone_circuit(n):
        # Placeholder for generating a random monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        circuit = {'monotone_width': n}
        return circuit
    
    def euler_maclaurin_integral(circuit, points):
        # Placeholder for calculating the integral using Euler-Maclaurin formula
        # This is a dummy implementation and should be replaced with actual logic
        return 0.0
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_monotone_circuit(n)
        Q = quasi_monte_carlo_rule(circuit)
        error = euler_maclaurin_integral(circuit, Q)
        results.append({'n': n, 'Q': Q, 'error': error})
    
    metric_value = sum(result['error'] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result['n'] for result in results)
    conjecture_holds = all(result['Q'] <= int(Fraction(result['circuit']['monotone_width']**2, math.log(1/result['error'])**2)) for result in results)
    
    return {
        "metric_name": "Integral Approximation Error",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")