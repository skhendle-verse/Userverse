# Userverse Testing

    -   To run the first suite 
    ```bash
    
    ```

## Database

Unit testing for db models

```bash

# User Model testing, tests/database/test_b_company.py
(userverse) $: pytest -v tests/database/test_a_user.py -s

# company tests
(userverse) $: pytest -v tests/database/test_b_company.py -s

# role tests
(userverse) $: pytest -v tests/database/test_c_role.py -s

# association
(userverse) $: pytest -v tests/database/test_e_association.py -s

```

## HTTP integration testing

TODO: Setup a testing config, to avoid comflicts with dev db

```bash
# assign a value to TEST_ENVIRONMENT, which help trigger creation of testing.db
(userverse) $: export TEST_ENVIRONMENT=True
#
# Main route testing
(userverse) $: pytest -v tests/http/test_main.py
# Security testing
(userverse) $: pytest -v tests/http/test_security.py
# Create user testing
(userverse) $: pytest -v tests/http/a_user/test_a_create_user_api.py
# User login testing
(userverse) $: pytest -v tests/http/a_user/test_b_user_login_api.py
# Get user testing
(userverse) $: pytest -v tests/http/a_user/test_c_get_user.py
# Update user testing
(userverse) $: pytest -v tests/http/a_user/test_d_update_user_api.py
# Reset Password: Get OTP
(userverse) $: pytest -v tests/http/a_user/test_e_password_reset_request.py
# Validate OTP
(userverse) $: pytest -v tests/http/a_user/test_f_password_otp_verify.py
# testing company routes
(userverse) $: pytest -v tests/http/b_company/test_a_create_company.py
# testing company routes
(userverse) $: pytest -v tests/http/b_company/test_b_get_company.py
# Update company
(userverse) $: pytest -v tests/http/b_company/test_c_update_company.py
# Create role
(userverse) $: pytest -v tests/http/b_company/test_d_create_role.py
# Update role
(userverse) $: pytest -v tests/http/b_company/test_e_update_role.py
# Delete role
(userverse) $: pytest -v tests/http/b_company/test_f_delete_role.py
# Get roles
(userverse) $: pytest -v tests/http/b_company/test_g_get_roles.py
# Get roles
(userverse) $: pytest -v tests/http/b_company/test_h_get_company_users.py
# Get roles
(userverse) $: pytest -v tests/http/b_company/test_i_get_user_companies.py


```

## Utils

Unit testing for app Utils

```bash
# Render templates testing
(userverse) $: pytest -v tests/utils/email/test_renderer.py -s

# Send email testing
(userverse) $: pytest -v tests/utils/email/test_sender.py -s

```
