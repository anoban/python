#include <assert.h>
#include <Python.h>
#include <stdlib.h>

static __declspec(noinline) long double __stdcall factorial(_In_ const unsigned n) {
    if (!n || n == 1) return 1.0000;
    long double result = n;
    for (long long i = n - 1; i > 1; --i) result *= i; // NOLINT(cppcoreguidelines-narrowing-conversions)
    return result;
}

static __declspec(noinline) long double __stdcall fact(_In_ const unsigned n) { // NOLINT(misc-no-recursion)
    if (!n || n == 1) return 1.0000;
    return n * fact(n - 1);
}

int main(void) {
    assert(fact(0) == 1.0000);
    assert(fact(1) == 1.0000);
    assert(fact(4) == 24.0000);
    assert(fact(6) == 720.0000);
    assert(fact(7) == 5040.0000);
    assert(fact(10) == 3'628'800.0000);
    assert(fact(23) == 25'852'016'738'884'976'640'000.0000);

    assert(factorial(0) == 1.0000);
    assert(factorial(1) == 1.0000);
    assert(factorial(4) == 24.0000);
    assert(factorial(6) == 720.0000);
    assert(factorial(7) == 5040.0000);
    assert(factorial(10) == 3'628'800.0000);
    assert(factorial(23) == 25'852'016'738'884'976'640'000.0000);

    return EXIT_SUCCESS;
}
