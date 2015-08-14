## {{meta.releasename}} ({{meta.date}})

{% if features|length > 0 %}
### Features

{% for issue in features %}
  * [{{issue.key}}]({{meta.jira}}/browse/{{issue.key}}): {{issue.fields.summary}}
{% endfor %}
{% endif %}

{% if bugs|length > 0 %}
### Bug Fixes

{% for issue in bugs %}
  * [{{issue.key}}]({{meta.jira}}/browse/{{issue.key}}): {{issue.fields.summary}}
{% endfor %}
{% endif %}

{% if others|length > 0 %}
### Various

{% for issue in others %}
  * [{{issue.key}}]({{meta.jira}}/browse/{{issue.key}}): {{issue.fields.summary}}
{% endfor %}

{% endif %}
