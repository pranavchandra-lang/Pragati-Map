"""
Google OAuth 2.0 authentication
Restricted to @wiom.in and @i2e1.com domains
"""
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth

router = APIRouter()

ALLOWED_DOMAINS = [d.strip() for d in os.getenv("ALLOWED_DOMAINS", "wiom.in,i2e1.com").split(",")]
ADMIN_EMAILS = [e.strip() for e in os.getenv("ADMIN_EMAILS", "").split(",") if e.strip()]

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

_LOGIN_HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wiom Talent — Login</title>
  <style>
    :root {{
      --pink: #D9008D; --purple: #443152; --dark: #161021;
      --card: #1E1530; --border: #2E2245; --text: #F0EAF8; --muted: #9B89B0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--dark); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: var(--card); border: 1px solid var(--border);
      border-radius: 16px; padding: 48px 40px; width: 100%; max-width: 400px;
      text-align: center;
    }}
    .logo {{ font-size: 28px; font-weight: 800; color: var(--pink); margin-bottom: 8px; }}
    .tagline {{ color: var(--muted); font-size: 14px; margin-bottom: 32px; }}
    h1 {{ font-size: 22px; margin-bottom: 8px; }}
    .sub {{ color: var(--muted); font-size: 14px; margin-bottom: 32px; line-height: 1.5; }}
    .btn-google {{
      display: flex; align-items: center; justify-content: center; gap: 12px;
      width: 100%; padding: 14px 20px; border-radius: 10px;
      background: var(--pink); color: white; text-decoration: none;
      font-weight: 600; font-size: 15px; border: none; cursor: pointer;
      transition: opacity 0.2s;
    }}
    .btn-google:hover {{ opacity: 0.88; }}
    .domain-note {{
      margin-top: 20px; font-size: 12px; color: var(--muted);
    }}
    {error_style}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">Wiom</div>
    <div class="tagline">Talent Intelligence Platform</div>
    <h1>अपने Wiom account से login करें</h1>
    <p class="sub">@wiom.in या @i2e1.com email से sign in करें<br>3 मिनट में अपना Skill Map देखें</p>
    {error_block}
    <a href="/auth/google" class="btn-google">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
        <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#fff"/>
        <path d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z" fill="#fff" opacity=".85"/>
        <path d="M3.964 10.707A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 000 9c0 1.452.348 2.827.957 4.039l3.007-2.332z" fill="#fff" opacity=".7"/>
        <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.961L3.964 7.293C4.672 5.166 6.656 3.58 9 3.58z" fill="#fff" opacity=".55"/>
      </svg>
      Sign in with Google
    </a>
    <p class="domain-note">केवल Wiom team के लिए · @wiom.in · @i2e1.com</p>
  </div>
</body>
</html>"""

_ERROR_STYLE = ".error-box { background: #2a1a1a; border: 1px solid #E01E00; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px; color: #ff6b6b; font-size: 13px; }"
_ERROR_BLOCK = '<div class="error-box">{msg}</div>'


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    error_style = _ERROR_STYLE if error else ""
    error_block = _ERROR_BLOCK.format(msg=error) if error else ""
    return _LOGIN_HTML.format(error_style=error_style, error_block=error_block)


@router.get("/auth/google")
async def auth_google(request: Request):
    redirect_uri = str(request.url_for("auth_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        return RedirectResponse("/login?error=Google+login+failed.+Please+try+again.")

    user_info = token.get("userinfo") or {}
    email = user_info.get("email", "")
    domain = email.split("@")[-1] if "@" in email else ""

    if domain not in ALLOWED_DOMAINS:
        return RedirectResponse(
            f"/login?error=Access+denied.+Only+@wiom.in+and+@i2e1.com+accounts+allowed."
        )

    role = "admin" if email in ADMIN_EMAILS else "employee"

    request.session["user"] = {
        "email": email,
        "name": user_info.get("name", email.split("@")[0]),
        "role": role,
        "picture": user_info.get("picture"),
    }

    return RedirectResponse("/")


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
