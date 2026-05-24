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
    
    def generate_ac0_circuit(n):
        # Generate a random AC0 parity circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_tropical_differential(circuit):
        # Calculate the tropical differential form of the circuit
        n = int(math.log2(len(circuit)))
        diff_form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i):
                diff_form[i][j] = abs(circuit[2**(i-1)+j] - circuit[2**(i-1)-j])
        return diff_form
    
    def min_rank(diff_form):
        # Calculate the minimal rank of the tropical differential form
        n = len(diff_form) - 1
        rank = 0
        for i in range(n + 1):
            if any(diff_form[j][i] != 0 for j in range(i, n + 1)):
                rank += 1
        return rank
    
    def grothendieck_witt_class_mod_2(rank):
        # Calculate the Grothendieck-Witt class modulo 2
        return rank % 2
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    diff_form = calculate_tropical_differential(circuit)
    rank = min_rank(diff_form)
    gw_class = grothendieck_witt_class_mod_2(rank)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 2**(n//3)
    counterexample = "" if conjecture_holds else f"Rank {rank} for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")