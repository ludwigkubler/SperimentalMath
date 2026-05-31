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
    
    def truth_table(cnf, n):
        tt = {}
        for assignment in product([0, 1], repeat=n):
            tt[assignment] = any(all(assignment[int(l[1:]) - 1] == (l[0] == '~') for l in clause) for clause in cnf)
        return tt

    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        clauses = [set(clause.split()) for clause in cnf]
        resolvents = set()
        while True:
            new_resolvents = []
            for i, clause1 in enumerate(clauses):
                for j, clause2 in enumerate(clauses):
                    if i == j:
                        continue
                    common_lits = [lit for lit in clause1 if lit[0] != '~' and f"~{lit}" in clause2]
                    if common_lits:
                        new_resolvent = set(clause1) | set(clause2)
                        for lit in common_lits:
                            new_resolvent.remove(lit)
                            new_resolvent.add(f"~{lit}")
                        if new_resolvent not in resolvents:
                            new_resolvents.append(new_resolvent)
            if not new_resolvents:
                break
            clauses.extend(new_resolvents)
        return len(resolvents)

    def min_lattice_dimension(tt):
        # Brute-force algorithm to find the minimal lattice dimension
        n = len(next(iter(tt)))
        for dim in range(1, 2**n + 1):
            if can_represent_with_lattice(tt, dim):
                return dim

    def can_represent_with_lattice(tt, dim):
        # Check if a lattice of given dimension can represent the truth table
        lattices = generate_lattices(dim)
        for lattice in lattices:
            if represents_truth_table(lattice, tt):
                return True
        return False

    def generate_lattices(n):
        # Generate all possible lattices of dimension n (simplified version)
        if n == 1:
            return [{0}, {1}]
        lattices = []
        for sublattice in generate_lattices(n-1):
            lattices.append(sublattice | {n-1})
            lattices.append(sublattice)
        return lattices

    def represents_truth_table(lattice, tt):
        # Check if a lattice can represent the truth table
        for assignment, value in tt.items():
            if not (value == 0 and n in lattice) and not (value == 1 and n-1 in lattice):
                return False
        return True

    def product(iterables, repeat=1):
        # Cartesian product of input iterables
        pools = [iterable for iterable in iterables] * repeat
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        return result

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = [''.join(random.choice(['x', '~x']) + str(i+1) for i in range(n)) for _ in range(10)]
        tt = truth_table(cnf, n)
        width = resolution_width(cnf)
        dim = min_lattice_dimension(tt)
        results.append({"n": n, "width": width, "dim": dim})

    mean_dim = sum(result["dim"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    correlation_coefficient = (sum((result["dim"] - mean_dim) * (result["width"] - mean_width) for result in results) /
                               math.sqrt(sum((result["dim"] - mean_dim)**2 for result in results) *
                                         sum((result["width"] - mean_width)**2 for result in results)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.7 else "correlation_coefficient=<{}>".format(correlation_coefficient)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] < 0.7) / len(results)
    
    if all(0.5 <= r["metric_value"] < 0.7 for r in results):
        print("RESULT: SUPPORTED mean={:.2f} std=0 support_fraction={:.2f}".format(mean_value, 0, support_fraction))
    elif any(r["metric_value"] < 0.5 or r["metric_value"] >= 0.7 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if r["metric_value"] < 0.5 or r["metric_value"] >= 0.7)
        print("RESULT: FALSIFIED counterexample='correlation_coefficient=<{}>' first_failing_seed={}".format(result["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_metric")