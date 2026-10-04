# Terraform

Creates a cross-account read-only observability role.

Set `observability_account_id` to the central monitoring account.

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan
```

The role only reads CloudWatch, Logs, EC2 and ECS metadata.
