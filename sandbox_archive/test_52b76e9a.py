# auto-injected by SEC sandbox
import math
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

import random, math, json, sys, itertools, collections, fractions


# ---------------------------------------------------------------------------
# Finite geometry helpers
# ---------------------------------------------------------------------------

def next_power_of_two(n):
    """Smallest power of 2 >= n (n >= 1)."""
    if n <= 1:
        return 1
    return 1 << math.ceil(math.log2(n))


def lines_in_pg2q(n):
    """
    Number of lines in PG(2, q) where q = 2**ceil(log2(n)).
    Formula: L = q**2 + q + 1
    """
    q = next_power_of_two(n)
    return q * q + q + 1


# ---------------------------------------------------------------------------
# NW seed length (theoretical bound for k-CNF)
# ---------------------------------------------------------------------------

def nw_seed_length(k, n):
    """
    Standard NW PRG seed length for a k-CNF on n variables:
        s = 2 * k * ceil(log2(n))
    """
    log2n = math.ceil(math.log2(n)) if n > 1 else 1
    return 2 * k * log2n


# ---------------------------------------------------------------------------
# Random CNF generation
# ---------------------------------------------------------------------------

def random_cnf(n_vars, n_clauses, max_width, rng):
    """
    Generate a random CNF as a list of tuples of literals.
    Variables: 1..n_vars; negated literal = negative int.
    Clause width ~ Uniform[1, max_width].
    """
    clauses = []
    for _ in range(n_clauses):
        width = rng.randint(1, max_width)
        width = min(width, n_vars)
        chosen = rng.sample(range(1, n_vars + 1), width)
        lits = [v if rng.random() < 0.5 else -v for v in chosen]
        clauses.append(tuple(sorted(set(lits))))
    return clauses


def max_clause_width(clauses):
    """Maximum clause width k in the formula."""
    if not clauses:
        return 1
    return max(len(c) for c in clauses)


# ---------------------------------------------------------------------------
# Core trial
# ---------------------------------------------------------------------------

def run_trial(seed):
    """
    Test the Nisan-Wigderson / PG(2,q) conjecture over 150 random CNF instances.

    Parameters
    ----------
    seed : int

    Returns
    -------
    dict with keys:
        metric_name      : str   - always "mean_L_minus_s"
        metric_value     : float - mean of (L - s) across all instances
        instances_tested : int
        conjecture_holds : bool  - True iff no violations detected
        counterexample   : str   - empty string if none found
    """
    rng = random.Random(seed)

    n_values = [4, 8, 12, 16, 20]
    formulas_per_n = 30        # 30 * 5 = 150 instances per trial
    clauses_per_formula = 20
    max_width = 3              # 3-CNF is the canonical NW setting

    diffs = []
    violations = []

    for n in n_values:
        L = lines_in_pg2q(n)
        for _ in range(formulas_per_n):
            clauses = random_cnf(n, clauses_per_formula, max_width, rng)
            k = max_clause_width(clauses)
            s = nw_seed_length(k, n)
            diff = L - s
            diffs.append(diff)
            # Violation: seed length exceeds line count + tolerance of 2
            if s > L + 2:
                violations.append((n, k, s, L, diff))

    mean_diff = sum(diffs) / len(diffs) if diffs else 0.0
    holds = (len(violations) == 0)

    counterexample = ""
    if violations:
        n_v, k_v, s_v, L_v, d_v = violations[0]
        excess = s_v - L_v - 2
        counterexample = (
            "n=" + str(n_v) + ", k=" + str(k_v) + ", s=" + str(s_v)
            + ", L=" + str(L_v) + ", diff=" + str(d_v)
            + " (s > L+2 by " + str(excess) + ")"
        )

    result = dict()
    result["metric_name"] = "mean_L_minus_s"
    result["metric_value"] = float(mean_diff)
    result["instances_tested"] = len(diffs)
    result["conjecture_holds"] = holds
    result["counterexample"] = counterexample
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Seeds from argv, or defaults
    if len(sys.argv) > 1:
        seeds = [int(a) for a in sys.argv[1:]]
    else:
        seeds = [11, 23, 37, 53, 71]

    results = []

    for seed in seeds:
        trial = run_trial(seed)
        row = dict()
        row["seed"] = seed
        row.update(trial)
        # Required: one TRIAL line per seed, unconditionally inside the loop
        print("TRIAL: " + json.dumps(row))
        sys.stdout.flush()
        results.append(trial)

    # Aggregate statistics
    total = len(results)
    hold_count = sum(1 for r in results if r["conjecture_holds"])
    has_counterexample = any(r["counterexample"] for r in results)
    vals = [r["metric_value"] for r in results]
    mean_v = sum(vals) / total if total else 0.0
    var_v = sum((v - mean_v) ** 2 for v in vals) / total if total else 0.0
    std_v = math.sqrt(var_v)
    hold_fraction = hold_count / total if total else 0.0

    # Find first failing seed and its counterexample
    first_failing_seed = None
    first_ce = ""
    for seed, r in zip(seeds, results):
        if r["counterexample"]:
            first_failing_seed = seed
            first_ce = r["counterexample"]
            break

    # Final verdict — must be the very last line printed
    if has_counterexample and hold_fraction < 0.90:
        print(
            'RESULT: FALSIFIED counterexample="' + first_ce + '"'
            + " first_failing_seed=" + str(first_failing_seed)
        )
    elif hold_fraction >= 0.80 and mean_v >= 0:
        print(
            "RESULT: SUPPORTED"
            + " mean=" + str(round(mean_v, 4))
            + " std=" + str(round(std_v, 4))
            + " support_fraction=" + str(round(hold_fraction, 4))
        )
    else:
        print(
            "RESULT: INCONCLUSIVE"
            + " support_fraction=" + str(round(hold_fraction, 4))
            + " mean=" + str(round(mean_v, 4))
        )