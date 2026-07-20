from fastapi import Depends

from repositories.customer_repository import CustomerRepository
from repositories.project_repository import ProjectRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from repositories.rbac_repository import RBACRepository
from services.project_service import ProjectService
from services.rbac_service import RBACService
from services.task_service import TaskService
from services.auth_service import AuthService
from services.customer_service import CustomerService


# CUSTOMER
def get_customer_repository():
    return CustomerRepository()


def get_customer_service(repo: CustomerRepository = Depends(get_customer_repository)):
    return CustomerService(repo)

    # TASK


def get_task_repository():
    return TaskRepository()


def get_task_service(repo: TaskRepository = Depends(get_task_repository)):
    return TaskService(repo)

    # AUTH / USER


def get_user_repository():
    return UserRepository()


def get_refresh_token_repository():
    return RefreshTokenRepository()


def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
    refresh_repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
):
    return AuthService(repo, refresh_repo)

    # PROJECT


def get_project_repository():
    return ProjectRepository()


def get_project_service(
    repo: ProjectRepository = Depends(get_project_repository),
    user_repo: UserRepository = Depends(get_user_repository),
):
    return ProjectService(repo, user_repo)


# RBAC


def get_rbac_repository():
    return RBACRepository()


def get_rbac_service(repo: RBACRepository = Depends(get_rbac_repository)):
    return RBACService(repo)
