locals {
  groups = [
    {
      slug="start-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/responses/start HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Start page"
    }, {
      slug="start-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/responses/start HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Start page submit"
    }, {
      slug="availability-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/availability HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Availability"
    }, {
      slug="availability-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/availability HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Availability submit"
    }, {
      slug="dayRate-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/dayRate HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Day rate"
    }, {
      slug="dayRate-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/dayRate HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Day rate submit"
    }, {
      slug="essentialRequirementsMet-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/essentialRequirementsMet HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Essential requirements met"
    }, {
      slug="essentialRequirementsMet-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/essentialRequirementsMet HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Essential requirements met submit"
    }, {
      slug="essentialRequirements-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/essentialRequirements HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Essential requirements"
    }, {
      slug="essentialRequirements-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/essentialRequirements HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Essential requirements submit"
    }, {
      slug="niceToHaveRequirements-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/niceToHaveRequirements HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Nice-to-have requirements"
    }, {
      slug="niceToHaveRequirements-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/niceToHaveRequirements HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Nice-to-have requirements submit"
    }, {
      slug="respondToEmailAddress-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/respondToEmailAddress HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Respond-to email address"
    }, {
      slug="respondToEmailAddress-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/respondToEmailAddress HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Respond-to email address submit"
    }, {
      slug="application-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/application HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Application"
    }, {
      slug="application-post"
      url_pattern="{$$.request = \"POST /suppliers/opportunities/*\" && $$.request = \"*/application HTTP/1.1\"}"
      status_pattern="$$.status=302"
      name="Application submit"
    }, {
      slug="result-get"
      url_pattern="{$$.request = \"GET /suppliers/opportunities/*\" && $$.request = \"*/responses/result HTTP/1.1\"}"
      status_pattern="$$.status=200"
      name="Result"
    }
  ]
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_0" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-0"

  pattern        = "{$$.requestTime >= 0 && $$.requestTime < 0.025 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-0"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_1" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-1"

  pattern        = "{$$.requestTime >= 0.025 && $$.requestTime < 0.05 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-1"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_2" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-2"

  pattern        = "{$$.requestTime >= 0.05 && $$.requestTime < 0.1 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-2"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_3" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-3"

  pattern        = "{$$.requestTime >= 0.1 && $$.requestTime < 0.25 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-3"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_4" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-4"

  pattern        = "{$$.requestTime >= 0.25 && $$.requestTime < 0.5 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-4"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_5" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-5"

  pattern        = "{$$.requestTime >= 0.5 && $$.requestTime < 1 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-5"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_6" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-6"

  pattern        = "{$$.requestTime >= 1  && $$.requestTime < 2.5 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-6"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_7" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-7"

  pattern        = "{$$.requestTime >= 2.5  && $$.requestTime < 5 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-7"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_8" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-8"

  pattern        = "{$$.requestTime >= 5  && $$.requestTime < 10 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-8"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_log_metric_filter" "SLO_supplier_application_request_time_bucket_9" {
  count = "${length(local.groups)}"
  name  = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-9"

  pattern        = "{$$.requestTime >= 10 && ${lookup(local.groups[count.index], "url_pattern")} && ${lookup(local.groups[count.index], "status_pattern")}"
  log_group_name = "${var.router_log_group_name}"

  metric_transformation {
    name          = "${var.environment}-SLO-supplier-application-${lookup(local.groups[count.index], "slug")}-request-times-9"
    namespace     = "DM-SLO-RequestTimeBuckets"
    value         = "1"
    default_value = "0"
  }
}
