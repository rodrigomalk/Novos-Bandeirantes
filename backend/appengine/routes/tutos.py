# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

@login_not_required
@no_csrf
def jogando():
    return TemplateResponse(template_path="/jogando.html")

@login_not_required
@no_csrf
def criando():
    return TemplateResponse(template_path="/tutos/criando.html")

@login_not_required
@no_csrf
def aprendendo():
    return TemplateResponse(template_path="/aprendendo.html")