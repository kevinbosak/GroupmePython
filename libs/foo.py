#!/usr/bin/env python

def foo(bar='bar'):
    print(bar)

foo(bar = 'BAR')

baz = {'bar': 'BAZ'}
foo(**baz)
