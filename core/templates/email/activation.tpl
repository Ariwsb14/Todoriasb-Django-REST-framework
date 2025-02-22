{% extends "mail_templated/base.tpl" %}

{% block subject %}
Verify your email
{% endblock %}

{% block html %}
<h6>127.0.0.1:8080/accounts/api/v1/activation/confirm/{{token}}</h6>
{% endblock %}