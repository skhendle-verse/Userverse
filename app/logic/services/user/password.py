class UserPasswordService:
    def __init__(self, user_repository, password_hash_service):
        self.user_repository = user_repository
        self.password_hash_service = password_hash_service

    def update_password(self, user_id, new_password):
        hashed_password = self.password_hash_service.hash_password(new_password)
        self.user_repository.update_user_password(user_id, hashed_password)

    def verify_password(self, user_id, password):
        user = self.user_repository.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        return self.password_hash_service.verify_password(password, user.password)

    def reset_password(self, user_id, new_password):
        hashed_password = self.password_hash_service.hash_password(new_password)
        self.user_repository.update_user_password(user_id, hashed_password)

    def change_password(self, user_id, old_password, new_password):
        if not self.verify_password(user_id, old_password):
            raise ValueError("Old password is incorrect")
        self.update_password(user_id, new_password)
