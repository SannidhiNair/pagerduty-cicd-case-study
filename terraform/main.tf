terraform {
  required_providers {
    pagerduty = {
      source  = "PagerDuty/pagerduty"
      version = "~> 2.6"
    }
  }
}

provider "pagerduty" {
  token = var.pd_api_token
}

resource "pagerduty_service" "pd_app" {
  name              = "PD‑App"
  escalation_policy = pagerduty_escalation_policy.sev1.id
  alert_creation    = "create_alerts_and_incidents"
}

resource "pagerduty_escalation_policy" "sev1" {
  name = "PD‑App Sev‑1 Policy"

  rule {
    escalation_timeout = 10
    target {
      type = "user_reference"
      id   = var.oncaller_user_id
    }
  }
}

resource "pagerduty_event_orchestration" "deploys" {
  name = "Deploy change orchestration"
  set  = <<JSON
{
  "rules": [
    {
      "condition": "event_type == \"change\"",
      "actions": [
        { "route_to": "${pagerduty_service.pd_app.id}" }
      ]
    }
  ]
}
JSON
}
