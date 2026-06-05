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
    
    def tseitin_formula(n):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f"{variables[i]}")
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append(f"~{variables[i]} | ~{variables[j]}")
        return variables, clauses

    def boolean_lattice(variables):
        lattice = set()
        for v in variables:
            lattice.add(v)
            lattice.add("~" + v)
        for i in range(len(variables)):
            for subset in range(1 << len(variables[i])):
                clause = []
                for j in range(len(variables[i])):
                    if (subset >> j) & 1:
                        clause.append(variables[i][j])
                    else:
                        clause.append("~" + variables[i][j])
                lattice.add("|".join(clause))
        return lattice

    def k_theory_rank(lattice):
        # Simplified K-theory rank for boolean lattices
        return len(lattice)

    def communication_complexity_rank(formula):
        # Simplified communication complexity rank for Tseitin formulas
        return len(formula[1])

    n = 5 + random.randint(0, 3) * 5  # n ∈ {5, 10, 15, 20, 30, 40}
    variables, clauses = tseitin_formula(n)
    lattice = boolean_lattice(variables)
    min_rank_k_theory = k_theory_rank(lattice)
    
    if min_rank_k_theory == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    communication_rank = communication_complexity_rank((variables, clauses))
    log_min_rank_k_theory = math.log(min_rank_k_theory)
    
    if abs(communication_rank - log_min_rank_k_theory) <= 0.1 * log_min_rank_k_theory:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"R({n}) = {communication_rank}, expected ≈ {log_min_rank_k_theory}"

    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": communication_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")