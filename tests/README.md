# Userverse Testing

## Database

Unit testing for db models

```bash
# User Model testing
(userverse) $: pytest -v tests/database/user.py -s

```

## HTTP integration testing

TODO: Setup a testing config, to avoid comflicts with dev db

```bash

# Main route testing
(userverse) $: pytest -v tests/http/test_main.py
# Security testing
(userverse) $: pytest -v tests/http/test_security.py
# Create user testing
(userverse) $: pytest -v tests/http/user/test_a_create_user_api.py
# User login testing
(userverse) $: pytest -v tests/http/user/test_b_user_login_api.py
# Get user testing
(userverse) $: pytest -v tests/http/user/test_c_get_user.py
# Update user testing
(userverse) $: pytest -v tests/http/user/test_d_update_user_api.py

```