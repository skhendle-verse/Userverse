# Userverse Testing

    -   To run the first suite 
    ```bash
    
    ```

## Database

Unit testing for db models

```bash
# User Model testing
(userverse) $: pytest -v tests/database/test_a_user.py -s

```

## HTTP integration testing

TODO: Setup a testing config, to avoid comflicts with dev db

```bash
# assign a value to TEST_ENVIRONMENT, which help trigger creation of testing.db
(userverse) $: export TEST_ENVIRONMENT=True

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
# Reset Password: Get OTP
(userverse) $: pytest -v tests/http/user/test_e_password_reset_request.py
# Validate OTP
(userverse) $: pytest -v tests/http/user/test_f_password_otp_verify.py

```

## Utils

Unit testing for app Utils

```bash
# Render templates testing
(userverse) $: pytest -v tests/utils/email/test_renderer.py -s

# Send email testing
(userverse) $: pytest -v tests/utils/email/test_senderer.py -s

```
