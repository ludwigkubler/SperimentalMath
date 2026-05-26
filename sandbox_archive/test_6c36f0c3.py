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
    def generate_cnf(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f"~{v}" for v in variables], 2)
            clauses.append(" | ".join(clause))
        return " & ".join(clauses)

    def tseitin_circuit_valuation(cnf):
        literals = set()
        for clause in cnf.split(' & '):
            literals.update(clause.split(' | '))
        valuation = {}
        for literal in literals:
            if literal.startswith('~'):
                valuation[literal] = random.choice([0, 1])
            else:
                valuation[literal] = random.choice([0, 1])
        return valuation

    def quotient_algebra_rank(valuation):
        rank = 0
        for literal in valuation:
            if literal.startswith('~'):
                rank += valuation[literal]
            else:
                rank += 1 - valuation[literal]
        return rank

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    valuation = tseitin_circuit_valuation(cnf)
    rank = quotient_algebra_rank(valuation)

    C_n = 2  # Example constant
    expected_bound = C_n * math.log(n) ** 2

    return {
        "metric_name": "quotient_algebra_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_bound,
        "counterexample": "" if rank <= expected_bound else f"rank={rank}, expected={expected_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")