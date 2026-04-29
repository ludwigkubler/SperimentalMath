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

# Constants
X = [0, 1]
Y = [0, 1]

def g(x, y):
    return (x * y) % 2

def d(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def dist(a, b):
    return max(abs(ai - bi) for ai, bi in zip(a, b))

def is_bi_lipschitz(phi, distortion=2):
    for x1 in X:
        for y1 in Y:
            for x2 in X:
                for y2 in Y:
                    if dist(phi[(x1, y1)], phi[(x2, y2)]) > distortion * d((x1, y1), (x2, y2)):
                        return False
    return True

def generate_bi_lipschitz_permutations():
    perms = []
    for perm in itertools.permutations(X + Y):
        if is_bi_lipschitz({(x, y): perm[i] for i, (x, y) in enumerate(itertools.product(X, Y))}):
            perms.append(perm)
    return perms

def generate_boolean_functions(n):
    return [lambda x: int(x[:n] == '0' * n), lambda x: int(x[:n] == '1' * n)] + [
        lambda x: int(''.join(str(int(xi != yi)) for xi, yi in zip(x[:n], y[:n]))) % 2
        for y in itertools.product(X, repeat=n)
    ]

def protocol_cost(protocol):
    return len(protocol)

def simulate_protocol(protocol, inputs):
    transcripts = {}
    for input_ in inputs:
        transcript = ''.join(str(g(input_[i], protocol[i][input_[i]])) for i in range(len(input_)))
        if transcript not in transcripts:
            transcripts[transcript] = []
        transcripts[transcript].append(input_)
    return transcripts

def cover_multiplicity(transcripts, scale):
    covers = {}
    for transcript, inputs in transcripts.items():
        for input_ in inputs:
            center = tuple((i + scale // 2) % len(X) for i in input_)
            if center not in covers:
                covers[center] = []
            covers[center].append(input_)
    return max(len(covers[center]) for center in covers)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    phi_perms = generate_bi_lipschitz_permutations()
    boolean_funcs = generate_boolean_functions(4)
    n_values = [2, 3, 4]
    
    results = []
    for n in n_values:
        for f in boolean_funcs:
            inputs = list(itertools.product(X, repeat=n))
            cost_limit = protocol_cost(lambda x: f(x)) * 2
            protocols = []
            for depth in range(1, 2*n+3):
                new_protocols = []
                for p in protocols:
                    for i in range(n):
                        for j in X:
                            if protocol_cost(p) + 1 <= cost_limit:
                                new_protocol = [p[:i] + [(j, j)] + p[i+1:], *p]
                                new_protocols.append(new_protocol)
                protocols.extend(new_protocols)
            protocols = [p for p in protocols if protocol_cost(p) <= cost_limit]
            
            for protocol in protocols:
                transcripts = simulate_protocol(protocol, inputs)
                m_Pi_1 = cover_multiplicity(transcripts, 2)
                
                for phi_perm in phi_perms:
                    Pi_2 = [(phi_perm[i], phi_perm[n+i]) for i in range(n)]
                    transcripts_Pi_2 = simulate_protocol(Pi_2, inputs)
                    m_Pi_2 = cover_multiplicity(transcripts_Pi_2, 4)
                    
                    if m_Pi_2 > 2 * m_Pi_1 + 1:
                        return {
                            "metric_name": "Multiplicity Ratio",
                            "metric_value": m_Pi_2 / m_Pi_1,
                            "instances_tested": len(protocols) * len(phi_perms),
                            "conjecture_holds": False,
                            "counterexample": f"n={n}, f=lambda x: {f.__code__.co_consts[0]}, phi_perm={phi_perm}"
                        }
    
    return {
        "metric_name": "Multiplicity Ratio",
        "metric_value": max(m_Pi_2 / m_Pi_1 for n in n_values for f in boolean_funcs for protocol in protocols),
        "instances_tested": len(protocols) * len(phi_perms),
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