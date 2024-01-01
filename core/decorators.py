import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        
        #FIRST CHECK IF USER HAS THE PERMISSION (EVEN ANONYMOUS USERS)

        if user.groups.filter(name__in=groups).exists():
            return True
        # IN CASETHE 403 HANDLER SHOULD BE CALLED RAISE THE EXCEPTION
        if raise_exception:
            raise PermissionDenied
        # AS THE LAST RESORT
        return False
    return user_passes_test(check_perms )