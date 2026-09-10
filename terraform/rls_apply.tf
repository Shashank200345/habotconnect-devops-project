# Applies the row access policy in schemas/bigquery_row_access_policy.sql
# after the table is created. This uses PowerShell because the supported
# operator environment for this project is Windows; bq must be authenticated.
resource "null_resource" "apply_row_access_policy" {
  depends_on = [google_bigquery_table.student_onboarding]

  triggers = {
    # Re-apply whenever the policy file changes, not just on first create.
    policy_sha = filesha256("${path.module}/schemas/bigquery_row_access_policy.sql")
  }

  provisioner "local-exec" {
    interpreter = ["PowerShell", "-NoProfile", "-Command"]
    command     = <<-EOT
      $policy = @'
      ${replace(replace(file("${path.module}/schemas/bigquery_row_access_policy.sql"), "$${project_id}", var.project_id), "$${staged_reader_sa}", var.staged_reader_sa)}
      '@
      $policy = $policy -replace '\s+', ' '
      bq query --use_legacy_sql=false --project_id=${var.project_id} $policy
    EOT
  }
}
