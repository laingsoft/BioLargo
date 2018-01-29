from django.contrib.auth.mixins import UserPassesTestMixin


class ManagerTestMixin(UserPassesTestMixin):
    """
    mixin used to limit access to managers and admin only. To check for
    class based permissions, add test_func method to view with condition.
    """
    login_url = "/management/login"

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_manager or self.request.user.is_admin)
