from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.user_service import UserService
from starlette.responses import HTMLResponse

router = APIRouter()

# Set up Jinja2 template rendering
templates = Jinja2Templates(directory="templates")

# Render the login page
@router.get("/login")
async def get_login_page(request: Request, error: str = None, message: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error, "message": message})

# Handle form submissions to login
@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not UserService.login(username, password):
        # Redirect to the login page with an error message
        return RedirectResponse(url="/auth/login?error=Invalid credentials", status_code=303)
    
    # Redirect to the dashboard with a logout button
    return RedirectResponse(url="/auth/dashboard", status_code=303)

# Render the dummy dashboard page
@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Redirect from dashboard(dummy) to login
@router.get("/logout")
async def logout():
    return RedirectResponse(url="/auth/login", status_code=303)

@router.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    created_user = UserService.signup(username, password)
    if not created_user:
        # Redirect to the login page with an error message
        return RedirectResponse(url="/auth/login?error=Username already taken", status_code=303)
    
    # Redirect to the login page with a success message
    return RedirectResponse(url="/auth/login?message=Registered successfully", status_code=303)
