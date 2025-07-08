from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _
import os

def send_activation_email(request, user):
    current_site = get_current_site(request)
    subject = _("Account activation confirmation")   
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"
    message = render_to_string("activation_email.html", {
        "user": user,
        "activation_link": activation_link,
        "current_site": current_site,   
    })
    send_mail(subject, message, os.environ.get("EMAIL_HOST_ADDRESS"), [user.email])
