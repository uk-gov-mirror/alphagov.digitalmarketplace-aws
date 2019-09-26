variable "name" {}
variable "elasticsearch_url" {}
variable "elasticsearch_api_key" {}
variable "alarm_email_topic_arn" {}
variable "alarm_recovery_email_topic_arn" {}

variable "nginx_log_groups" {
  type = "list"
}

variable "application_log_groups" {
  type = "list"
}
