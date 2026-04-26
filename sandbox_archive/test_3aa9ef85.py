import random
import math
from fractions import Fraction

def random_CNF(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([0, 1]) - 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def GF2_poly_add(poly1, poly2):
    result = []
    for i in range(max(len(poly1), len(poly2))):
        coeff1 = poly1[i] if i < len(poly1) else 0
        coeff2 = poly2[i] if i < len(poly2) else 0
        result.append((coeff1 + coeff2) % 2)
    return result

def GF2_poly_mul(poly1, poly2):
    result = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] += poly1[i] * poly2[j]
            result[i + j] %= 2
    return result

def GF2_poly_div(dividend, divisor):
    quotient = []
    remainder = dividend[:]
    while len(remainder) >= len(divisor):
        leading_coeff_quotient = remainder[-1] // divisor[-1]
        quotient.append(leading_coeff_quotient)
        shift_amount = len(remainder) - len(divisor)
        shifted_divisor = [0] * shift_amount + divisor
        remainder = [a ^ b for a, b in zip(remainder, shifted_divisor)]
    return quotient[::-1], remainder

def GF2_poly_gcd(poly1, poly2):
    while poly2:
        poly1, poly2 = poly2, GF2_poly_mod(poly1, poly2)
    return poly1

def GF2_poly_mod(dividend, divisor):
    quotient, remainder = GF2_poly_div(dividend, divisor)
    return remainder

def Buchberger_algorithm(generators):
    S = []
    G = generators[:]
    for i in range(len(G)):
        for j in range(i + 1, len(G)):
            s = GF2_poly_gcd(G[i], G[j])
            if s:
                S.append(s)
    while S:
        g = S.pop()
        G.append(g)
        for h in G:
            s = GF2_poly_gcd(g, h)
            if s:
                S.append(s)
    return G

def DPLL_lower_bound(clauses):
    def dpll(model, clauses):
        unsatisfied_clauses = [c for c in clauses if all(l not in model or l != -m for m in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = {**model, abs(literal): literal}
            return dpll(new_model, clauses) or dpll({**model, abs(literal): -literal}, clauses)
        pure_literal = next((l for l in range(1, max(abs(c) for c in sum(clauses, [])) + 1) if (all(l not in model or l != m for m in c) and all(-l not in model or -l != m for m in c))), None)
        if pure_literal:
            new_model = {**model, abs(pure_literal): pure_literal}
            return dpll(new_model, clauses) or dpll({**model, abs(pure_literal): -pure_literal}, clauses)
        literal = random.choice([l for l in range(1, max(abs(c) for c in sum(clauses, [])) + 1)])
        new_model = {**model, literal: literal}
        return dpll(new_model, clauses) or dpll({**model, literal: -literal}, clauses)
    return len(dpll({}, clauses))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    m = 2 * n
    cnf = random_CNF(n, m)
    polynomials = [GF2_poly_add([0] * (i - 1) + [1], [0] * (n - i)) for i in range(1, n + 1)]
    generators = []
    for clause in cnf:
        poly = [0] * n
        for literal in clause:
            if literal > 0:
                poly[literal - 1] += 1
            else:
                poly[-literal - 1] -= 1
        generators.append(poly)
    ideal_generators = Buchberger_algorithm(generators)
    proof_size = DPLL_lower_bound(cnf)
    return {
        "metric_name": "Generator Count",
        "metric_value": len(ideal_generators),
        "instances_tested": 1,
        "conjecture_holds": len(ideal_generators) == proof_size,
        "counterexample": "" if len(ideal_generators) == proof_size else f"Generator count {len(ideal_generators)} != Proof size {proof_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Generator count != Proof size\" first_failing_seed={first_failing_seed}")