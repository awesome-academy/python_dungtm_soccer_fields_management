from soccer.utils import user_in_group
from soccer.constants import GROUP_ADMIN
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not user_in_group(request.user, GROUP_ADMIN):
            return HttpResponseForbidden(_("You do not have permission to perform this action."))
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)