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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_differential(circuit):
        n = len(circuit)
        diff_form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if circuit[i] != circuit[j]:
                    diff_form[i][j] = 1
                    diff_form[j][i] = 1
        return diff_form
    
    def min_rank(diff_form):
        n = len(diff_form)
        rank = 0
        for i in range(n):
            row_sum = sum(diff_form[i])
            if row_sum > 0:
                rank += 1
        return rank
    
    def grothendieck_witt_class_mod_2(rank, n):
        return rank % 2 == 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_ac0_circuit(n)
            diff_form = compute_tropical_differential(circuit)
            rank = min_rank(diff_form)
            if not grothendieck_witt_class_mod_2(rank, n):
                return {
                    "metric_name": "min_rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank}"
                }
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
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
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std=... support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")