# -*- coding: utf-8 -*-

EMAIL_TEMPLATE="""
<ul>
    {% for issue in issues %}
        <li>
            <a href="{{ issue.link }}">{{ issue.key }}</a>: {{ issue.summary }}
        </li>
    {% endfor %}
</ul>

"""
