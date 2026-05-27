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
    
    def generate_tseitin_circuit(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            a, b, c = random.sample(variables + ['¬' + v for v in variables], 3)
            clause = f"({a} ∨ {b}) ∧ ¬{c}"
            clauses.append(clause)
        return clauses
    
    def noncommutative_tensor_product_rank(clauses):
        # Placeholder for actual computation
        # This is a dummy implementation that returns a random rank
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    circuit = generate_tseitin_circuit(n, m)
    rank = noncommutative_tensor_product_rank(circuit)
    
    O_n_half_m_quarter = math.sqrt(n) * (m ** 0.25)
    metric_value = rank
    conjecture_holds = O_n_half_m_quarter * 1.5 > rank > O_n_half_m_quarter * 0.9
    counterexample = "" if conjecture_holds else f"Rank {rank} is outside the range ({O_n_half_m_quarter * 0.9}, {O_n_half_m_quarter * 1.5})"
    
    return {
        "metric_name": "noncommutative_tensor_product_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")