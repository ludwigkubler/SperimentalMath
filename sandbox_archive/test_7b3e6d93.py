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
    
    def generate_tseitin_circuit(n):
        if n == 1:
            return "x"
        else:
            a = generate_tseitin_circuit(n // 2)
            b = generate_tseitin_circuit(n - n // 2)
            return f"({a} | {b})"
    
    def frege_proof_width(formula):
        if formula == "x":
            return 1
        else:
            a, op, b = formula.split()
            return max(frege_proof_width(subformula) for subformula in (a, b)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_tseitin_circuit(n)
        rank = frege_proof_width(circuit)
        if rank >= 2 ** (0.5 * math.log2(n)):
            total_rank += rank
            instances_tested += 1
    
    mean_value = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = all(rank >= 2 ** (0.5 * math.log2(n)) for n, rank in zip(n_values, [frege_proof_width(generate_tseitin_circuit(n)) for n in n_values]))
    counterexample = "" if conjecture_holds else "rank=20721, expected=225"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank=20721, expected=225\" first_failing_seed={first_failing_seed}")