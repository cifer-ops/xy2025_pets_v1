#!/usr/bin/env python
"""Run a script to test the unit, using simplified test settings"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Use simplified test setup
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
    django.setup()
    
    # Run the test
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Prepare the test parameters
    test_args = sys.argv[1:] or ['accounts', 'pets']
    
    print(f"Running tests: {', '.join(test_args)}")
    failures = test_runner.run_tests(test_args)
    
    # Exit code - Returns a non-zero value if there is a failed test
    sys.exit(bool(failures)) 