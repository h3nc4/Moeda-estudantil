#  Copyright 2023 Henrique Almeida, Gabriel Dolabela, João Pauletti
# 
# This file is part of Moeda estudantil.
# 
# Moeda estudantil is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# 
# Moeda estudantil is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
# 
# You should have received a copy of the GNU Affero
# General Public License along with Moeda estudantil. If not, see
# <https://www.gnu.org/licenses/>.

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime
from threading import Thread
import six  

# Gerador de tokens para ativação de conta
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active))
account_activation_token = AccountActivationTokenGenerator()

# Envia um email assíncrono
def mail(subject, template_name, context, to_email):
    def send_email():
        try:
            email = EmailMessage(subject, render_to_string(template_name, context), to=[to_email])
            email.send()
            print(datetime.now().strftime("[%d/%b/%Y %H:%M:%S] Email sent to " + to_email))
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    email_thread = Thread(target=send_email)
    email_thread.start()
