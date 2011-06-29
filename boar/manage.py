#!/usr/bin/env python
import os
import site

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from django.core.management import execute_manager
import settings

if __name__ == "__main__":
    execute_manager(settings)

