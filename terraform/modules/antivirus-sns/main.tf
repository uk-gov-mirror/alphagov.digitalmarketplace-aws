provider "aws" {
  region  = "eu-west-1"
}

resource "aws_sns_topic" "s3_file_upload_notification" {
  name                              = "s3_file_upload_notification_${var.environment}"
  http_success_feedback_role_arn    = aws_iam_role.sns_success_feedback.arn
  http_success_feedback_sample_rate = 100
  http_failure_feedback_role_arn    = aws_iam_role.sns_failure_feedback.arn

  delivery_policy = <<EOF
{
  "http": {
    "defaultHealthyRetryPolicy": {
      "minDelayTarget": 1,
      "maxDelayTarget": 2399,
      "numRetries": ${var.topic_num_retries},
      "numMaxDelayRetries": 0,
      "numNoDelayRetries": 1,
      "numMinDelayRetries": 0,
      "backoffFunction": "linear"
    },
    "disableSubscriptionOverrides": true
  }
}
EOF

}

resource "aws_sns_topic_policy" "s3_file_upload_notification_policy_attachment" {
  arn    = aws_sns_topic.s3_file_upload_notification.arn
  policy = data.aws_iam_policy_document.s3_file_upload_notification_topic_policy.json
}

