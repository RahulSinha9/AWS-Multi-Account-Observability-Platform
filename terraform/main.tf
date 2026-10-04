data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = ["arn:aws:iam::${var.observability_account_id}:root"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "read_only" {
  statement {
    effect = "Allow"
    actions = ["cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:ListMetrics", "logs:DescribeLogGroups", "logs:DescribeLogStreams", "logs:FilterLogEvents", "ec2:DescribeInstances", "ecs:DescribeServices", "ecs:DescribeTasks", "ecs:ListClusters"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "observability" {
  name = var.role_name
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
resource "aws_iam_role_policy" "read_only" {
  name = "${var.role_name}-policy"
  role = aws_iam_role.observability.id
  policy = data.aws_iam_policy_document.read_only.json
}
