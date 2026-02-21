class Config:
    BASE_URL = "https://stellarburgers.education-services.ru"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    
    # API endpoints
    API_REGISTER = f"{BASE_URL}/api/auth/register"
    API_LOGIN = f"{BASE_URL}/api/auth/login"
    API_USER = f"{BASE_URL}/api/auth/user"
    
    # URLs
    LOGIN_URL = f"{BASE_URL}/login"
    FEED_URL = f"{BASE_URL}/feed"
    