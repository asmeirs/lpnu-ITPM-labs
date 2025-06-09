import pytest
import numpy as np
import sympy as sp
from core import x, parse_function, get_domain_and_range, get_safe_numeric_domain


@ pytest.mark.parametrize("expr, expected_sym_str, test_val, expected_val", [
    ("x**2 + 1", "x**2 + 1", 2.0, 5.0),
    ("2x + 3", "2*x + 3", -1.0, 1.0),  # implicit multiplication
    ("x^2 - x", "x**2 - x", 3.0, 6.0),   # convert XOR
    ("5", "5", 0.0, 5.0),               # constant
    ("e * x", "E*x", 2.0, 2.0 * float(sp.E)),  # Euler's number
    ("pi*x", "pi*x", 0.5, 0.5 * float(sp.pi)), # pi constant
])
def test_parse_valid_expressions(expr, expected_sym_str, test_val, expected_val):
    func_sym, f_lambdified, deriv_sym, deriv_lambdified = parse_function(expr)
    assert str(func_sym) == expected_sym_str
    val = f_lambdified(test_val)
    assert np.isclose(val, expected_val)
    expected_deriv = sp.diff(func_sym, x)
    deriv_val = deriv_lambdified(test_val)
    assert str(expected_deriv) == str(deriv_sym)
    assert np.isclose(deriv_val, float(expected_deriv.subs(x, test_val)))


@ pytest.mark.parametrize("bad_expr", [
    "y + 1",          # unrecognized symbol
    "x + ",           # syntax error
    "((x+1)",         # unclosed parenthesis
    "",               # empty string
    None,              # non-string input
])
def test_parse_invalid_expressions(bad_expr):
    with pytest.raises(ValueError):
        parse_function(bad_expr)


#########################################################################################
@pytest.mark.parametrize("func, expected_domain_subset, expected_range, expected_note", [
    (x**2 + 1, sp.S.Reals, sp.Interval(1, sp.oo), None),
    (sp.sqrt(x), sp.Interval(0, sp.oo), sp.Interval(0, sp.oo), None),
    (1/(x-2), sp.S.Reals - sp.FiniteSet(2), sp.Union(sp.Interval.open(-sp.oo, 0), sp.Interval.open(0, sp.oo)), None),
    (sp.tan(x)+sp.cot(x), sp.S.Reals, sp.Union(sp.Interval(-sp.oo, -2), sp.Interval(2, sp.oo)), 'Domain cannot be fully defined.')
])
def test_non_trig_domains_and_ranges(func, expected_domain_subset, expected_range, expected_note):
    domain, range_y, note = get_domain_and_range(func)
    # domain should at least contain expected subset
    assert expected_domain_subset == domain or expected_domain_subset.subset(domain)
    assert range_y == expected_range
    assert note == expected_note


#########################################################################################
@ pytest.mark.parametrize("domain, expected", [
    (sp.Interval(-10, 10), (-10.0, 10.0)),
    (sp.S.Reals, (-20.0, 20.0)),
    (sp.Interval(10, 30), (10.0, 20.0)),
    (sp.Interval(-30, -10), (-20.0, -10.0)),
    (sp.Interval(5, 5), (5.0, 5.0)),
])
def test_safe_numeric_domain_valid(domain, expected):
    result = get_safe_numeric_domain(domain)
    assert result == expected

@ pytest.mark.parametrize("bad_domain", [
    sp.Interval(100, 200),
    sp.EmptySet,
])

def test_safe_numeric_domain_empty(bad_domain):
    with pytest.raises(ValueError):
        get_safe_numeric_domain(bad_domain)
