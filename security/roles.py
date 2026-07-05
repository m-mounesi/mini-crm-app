ROLE_PERMISSIONS = {
    "admin": [
        "customer:read",
        "customer:write",
        "customer:delete",
        "project:read",
        "project:write",
        "project:delete",
        "task:read",
        "task:write",
        "task:delete",
    ],
    "manager": [
        "customer:read",
        "project:read",
        "project:write",
        "task:read",
        "task:write",
    ],
    "user": [
        "task:read",
        "task:write",
    ],
}
