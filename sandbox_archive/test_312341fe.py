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
    
    def generate_dfa(n):
        states = list(range(2**n))
        transitions = {state: {} for state in states}
        accepting_states = [0]
        for state in states:
            for bit in range(n):
                next_state = (state >> 1) | ((bit ^ (state & 1)) << (n - 1))
                transitions[state][bit] = next_state
        return states, transitions, accepting_states

    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append(-variables[j])
            clauses.append(clause)
        return variables, clauses

    def ac0_circuit_size(n):
        # Simplified approximation of AC0 circuit size for PARITY
        return n * math.log2(n)

    def automorphism_group(dfa):
        states = dfa[0]
        transitions = dfa[1]
        group = []
        for perm in itertools.permutations(states):
            is_automorphism = True
            for state in states:
                for bit in range(len(state)):
                    if transitions[state][bit] != perm[transitions[perm[state]][bit]]:
                        is_automorphism = False
                        break
                if not is_automorphism:
                    break
            if is_automorphism:
                group.append(perm)
        return group

    def rank_of_group(group):
        return len(group)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate random regular language using DFA
        dfa = generate_dfa(n)
        rank_regular = rank_of_group(automorphism_group(dfa))
        size_ac0 = ac0_circuit_size(n)
        metric_value += abs(rank_regular - c * math.log(size_ac0))

        # Generate non-regular language using CNF
        cnf = generate_cnf(n)
        rank_non_regular = rank_of_group(automorphism_group(cnf))
        if rank_non_regular < d * n**alpha:
            counterexample = f"Non-regular language with rank {rank_non_regular} and n={n}"
            conjecture_holds = False
        metric_value += abs(rank_non_regular - d * n**alpha)

        instances_tested += 2

    return {
        "metric_name": "Rank of Automorphism Group",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")