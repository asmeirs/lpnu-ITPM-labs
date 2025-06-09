import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)
import numpy as np
import tokenize
from io import BytesIO

x = sp.symbols('x')
ALLOWED_SYMBOLS = {'x': x, 'e': sp.E, 'pi': sp.pi}
TRANSFORMATIONS = (
        standard_transformations
        + (implicit_multiplication_application, convert_xor)
)

def parse_function(func_str):
    if not isinstance(func_str, str) or not func_str.strip():
        raise ValueError("Function expression must be a non-empty string")

    try:
        _ = list(tokenize.tokenize(BytesIO(func_str.encode('utf-8')).readline))

        func_sym = parse_expr(
            func_str,
            local_dict=ALLOWED_SYMBOLS,
            transformations=TRANSFORMATIONS,
            evaluate=True
        )
    except (tokenize.TokenError, sp.SympifyError, SyntaxError, TypeError) as e:
        raise ValueError(f"Invalid function expression: {e}")

    extra = func_sym.free_symbols - {x}
    if extra:
        names = ', '.join(str(s) for s in extra)
        raise ValueError(f"Unrecognized symbols in expression: {names}")

    f_lambdified = sp.lambdify(x, func_sym, modules=["numpy"])
    deriv_sym = sp.diff(func_sym, x)
    deriv_lambdified = sp.lambdify(x, deriv_sym, modules=["numpy"])

    return func_sym, f_lambdified, deriv_sym, deriv_lambdified


def get_domain_and_range(func_sym):
    note = None
    try:
        if func_sym.has(sp.tan) and func_sym.has(sp.cot):
            domain = sp.solve_univariate_inequality(sp.cos(x) != 0 and sp.sin(x) != 0, x)
        elif func_sym.has(sp.tan):
            domain = sp.solve_univariate_inequality(sp.cos(x) != 0, x)
        elif func_sym.has(sp.cot):
            domain = sp.solve_univariate_inequality(sp.sin(x) != 0, x)
        else:
            domain = sp.calculus.util.continuous_domain(func_sym, x, sp.S.Reals)
    except Exception:
        domain = sp.S.Reals
        note = (f"Domain cannot be fully defined.")

    range_y = sp.calculus.util.function_range(func_sym, x, domain)
    return domain, range_y, note


def get_safe_numeric_domain(domain, default_min=-20.0, default_max=20.0):
    safe_domain = domain.intersect(sp.Interval(default_min, default_max))
    if safe_domain.is_empty:
        raise ValueError("Empty domain in default range")
    return float(safe_domain.inf), float(safe_domain.sup)

def evaluate_function(f_lambdified, x_vals):
    result = f_lambdified(x_vals)
    if np.isscalar(result):
        result = np.full_like(x_vals, result)
    return result

def evaluate_derivative(deriv_lambdified, x_vals):
    result = deriv_lambdified(x_vals)
    if np.isscalar(result):
        return np.full_like(x_vals, result, dtype=np.float64)
    return np.array(result)

def compute_tangent_line(f_lambdified, deriv_lambdified, x_vals, x0):
    f_x0 = f_lambdified(x0)
    slope = deriv_lambdified(x0)

    if not np.isfinite(f_x0):
        raise ValueError(f"f(x₀) is not finite at x₀ = {x0}")
    if not np.isfinite(slope):
        raise ValueError(f"f′(x₀) is not finite at x₀ = {x0}")

    tangent_line = slope * (x_vals - x0) + f_x0
    return tangent_line, f_x0, slope

def compute_definite_integral(func_sym, a, b):
    singularities = sp.singularities(func_sym, x)
    interval = sp.Interval(a, b)

    for s in singularities:
        if s in interval:
            raise ValueError(f"Function has a discontinuity at x = {s} in the interval [{a}, {b}]")

    return sp.N(sp.integrate(func_sym, (x, a, b)))
