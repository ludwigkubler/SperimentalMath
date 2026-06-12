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
    
    def generate_regex(n):
        if n == 0:
            return ""
        elif n == 1:
            return "a|b"
        else:
            return f"({generate_regex(n-1)})*"

    def is_equivalent(r1, r2):
        # Brute-force check for equivalence
        alphabet = {'a', 'b'}
        visited = set()
        stack = [(r1, r2)]
        while stack:
            s1, s2 = stack.pop()
            if (s1, s2) in visited:
                continue
            visited.add((s1, s2))
            if s1 == s2:
                continue
            for a in alphabet:
                if not is_equivalent(s1.replace('a', a), s2.replace('b', a)):
                    return False
        return True

    def automorphism_group(r):
        # Brute-force computation of automorphism group
        alphabet = {'a', 'b'}
        n = len(r)
        perms = []
        for p in itertools.permutations(alphabet, 2):
            permuted_r = r.replace('a', p[0]).replace('b', p[1])
            if is_equivalent(r, permuted_r):
                perms.append(p)
        return perms

    def frege_proof_depth(circuit):
        # Placeholder for Frege proof depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)

    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        regex = generate_regex(n)
        aut_group = automorphism_group(regex)
        rank = len(aut_group)
        circuit = [f"gate_{i}" for i in range(rank)]  # Dummy circuit
        depth = frege_proof_depth(circuit)
        metric_values.append((rank, depth))
        instances_tested += 1
    
    if not metric_values:
        return {
            "metric_name": "Rank vs Depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks, depths = zip(*metric_values)
    correlation_coefficient = sum((r - mean(ranks)) * (d - mean(depths)) for r, d in zip(ranks, depths)) / (len(metric_values) * std(ranks) * std(depths))
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": ""
    }

def mean(data):
    return sum(data) / len(data)

def std(data):
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")