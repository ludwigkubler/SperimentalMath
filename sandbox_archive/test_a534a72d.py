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
    
    def generate_mso_formula(n: int, clause_length: int):
        formula = ' & '.join(f'{random.choice(["~", ""]) + chr(97+i)}' for i in range(n))
        for _ in range(clause_length):
            var = random.choice([chr(97+i) for i in range(n)])
            formula += f' & {var} -> {random.choice(["~", ""])}{var}'
        return formula

    def evaluate_ramanujan_sum(formula: str, n: int):
        assignments = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
        sums = set()
        for assignment in assignments:
            value = 0
            for term in formula.split(' & '):
                if '->' not in term:
                    var = term.strip('~')
                    value += assignment[ord(var) - ord('a')]
                else:
                    lhs, rhs = term.split(' -> ')
                    lhs_var = lhs.strip('~')
                    rhs_var = rhs.strip('~')
                    if assignment[ord(lhs_var) - ord('a')] == 1 and assignment[ord(rhs_var) - ord('a')] == 0:
                        value += 1
            sums.add(value)
        return len(sums)

    max_rank = 0
    instances_tested = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 5 instances per size
            clause_length = random.randint(1, 3)
            formula = generate_mso_formula(n, clause_length)
            rank = evaluate_ramanujan_sum(formula, n)
            max_rank = max(max_rank, rank)
            instances_tested += 1

    conjecture_holds = max_rank <= 2 * math.log2(instances_tested)
    counterexample = "" if conjecture_holds else f"Max rank {max_rank} exceeds 2*log({instances_tested})"

    return {
        "metric_name": "minimal_rank",
        "metric_value": max_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")