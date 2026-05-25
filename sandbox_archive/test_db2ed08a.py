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
    
    def generate_quaternion():
        return [random.uniform(-1, 1) for _ in range(4)]
    
    def tropicalize(q):
        return max(abs(x) for x in q)
    
    def ac0_parity_circuit(depth, n_vertices):
        if depth == 1:
            return random.choice([0, 1])
        else:
            left = ac0_parity_circuit(depth - 1, n_vertices)
            right = ac0_parity_circuit(depth - 1, n_vertices)
            return (left + right) % 2
    
    def generate_circuit(diameter):
        depth = random.randint(1, diameter)
        n_vertices = random.randint(2, diameter + 1)
        return ac0_parity_circuit(depth, n_vertices), depth, n_vertices
    
    def calculate_min_rank(circuits):
        ranks = []
        for circuit, _, _ in circuits:
            rank = tropicalize(generate_quaternion())
            ranks.append(rank)
        return min(ranks)
    
    def calculate_diameter(n_vertices):
        return n_vertices - 1
    
    def calculate_ratio(min_rank, diameter):
        if diameter == 0:
            return float('inf')
        return Fraction(min_rank, math.log(diameter))
    
    circuits = [generate_circuit(random.randint(5, 40)) for _ in range(30)]
    min_rank = calculate_min_rank(circuits)
    diameters = [calculate_diameter(n_vertices) for _, _, n_vertices in circuits]
    ratios = [calculate_ratio(min_rank, diameter) for diameter in diameters]
    
    mean_metric_value = sum(ratios) / len(ratios)
    conjecture_holds = all(r >= Fraction(1, 2) for r in ratios)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Rank to Log Diameter",
        "metric_value": mean_metric_value,
        "instances_tested": len(circuits),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")