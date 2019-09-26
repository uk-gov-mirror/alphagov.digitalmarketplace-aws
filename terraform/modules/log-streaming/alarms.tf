resource "aws_cloudwatch_metric_alarm" "log_stream_lambda_error_alarm" {
  alarm_name        = "${var.name}"
  alarm_description = "Alarms on failure of ${var.name} lambda function."

  // Metric
  namespace   = "Lambda"
  metric_name = "Errors"

  dimensions {
    LogGroupName = "${var.name}"
    Resource     = "${var.name}"
  }

  // For for every 60 seconds
  evaluation_periods = "1"
  period             = "60"

  // If totals 1 or higher
  statistic           = "Sum"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = "1"

  // If there is no data then do not alarm
  treat_missing_data = "notBreaching"

  // Email slack
  alarm_actions = ["${var.alarm_email_topic_arn}"]
  ok_actions    = ["${var.alarm_recovery_email_topic_arn}"]
}
