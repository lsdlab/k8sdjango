from django.contrib.auth.models import UserManager as AbstractUserManager


class UserManager(AbstractUserManager):
    def get_by_natural_key(self, username):
        """
        邮箱/手机号都能登录
        """
        if '@' in username:
            return self.get(email=username)
        elif username.isdigit() and len(username) == 11:
            return self.get(mobile=username)
        else:
            user = self.get(username__iexact=username)
        return user
