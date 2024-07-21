from django.urls import include
from django.urls import path
from django.urls import re_path

from .views import UserDoneTasks , UserNextTask , UserStatus , CollectTask , payTask , CheckStatus , CheckAllUsersStatus
urlpatterns = [
    path("user-tasks/<int:user_id>/", UserDoneTasks.as_view(), name="user_tasks"),
    path("user-next-task/<int:user_id>/", UserNextTask.as_view(), name="user_next_task"),
    path("user-status/<int:user_id>/", UserStatus.as_view(), name="user_status"),
    path("collect/<int:task_id>/", CollectTask.as_view(), name="collect_task"),
    path("pay/<int:task_id>/", payTask.as_view(), name="pay_task"),
    path("check-status/<int:user_id>/", CheckStatus.as_view(), name="check_status"),
    path("all-users-status/", CheckAllUsersStatus.as_view(), name="check_users_status"),
]