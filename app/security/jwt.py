from datetime import datetime, timedelta, timezone
import traceback
from app.configs import configs
from fastapi import HTTPException, status
import jwt
from typing import Dict, Any


class JWTManager:
    def __init__(self):
        self.JWT_SECRET = configs.get("SECRET", "secret1234")
        self.JWT_ALGORITHM = configs.get("ALGORITHM", "HS256")
        self.SESSION_TIMEOUT = int(configs.get("SESSION_TIMEOUT", 15))  # in minutes
        self.REFRESH_TIMEOUT = int(
            configs.get("REFRESH_SESSION_TIMEOUT", 60)
        )  # 7 days default

    def signJWT(self, user: dict) -> Dict[str, str]:
        now = datetime.now(timezone.utc)
        access_expire = now + timedelta(minutes=self.SESSION_TIMEOUT)
        refresh_expire = now + timedelta(minutes=self.REFRESH_TIMEOUT)

        access_payload = {
            "user": user,
            "type": "access",
            "exp": access_expire,
        }

        refresh_payload = {
            "user": user,
            "type": "refresh",
            "exp": refresh_expire,
        }

        access_token = jwt.encode(
            payload=access_payload,
            key=self.JWT_SECRET,
            algorithm=self.JWT_ALGORITHM,
        )
        refresh_token = jwt.encode(
            payload=refresh_payload,
            key=self.JWT_SECRET,
            algorithm=self.JWT_ALGORITHM,
        )

        return {
            "access_token": access_token,
            "access_token_expiration": access_expire.strftime("%Y-%m-%d %H:%M:%S"),
            "refresh_token": refresh_token,
            "refresh_token_expiration": refresh_expire.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            decoded = jwt.decode(
                token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM]
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error decoding token",
            )

    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        try:
            decoded = self.decode_token(refresh_token)
            if decoded.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token type for refresh",
                )

            user = decoded.get("user")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User data missing in token",
                )

            return self.signJWT(user)

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


if __name__ == "__main__":
    # Example usage:
    tokens = JWTManager().signJWT({"id": 123, "email": "agent@example.com"})
    print("Generated Tokens:", tokens)

    # Later, to refresh:
    new_tokens = JWTManager().refresh_token(tokens["refresh_token"])
    print("Refreshed Tokens:", new_tokens)

    # uv run -m app.security.jwt
