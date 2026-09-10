CREATE ROW ACCESS POLICY IF NOT EXISTS lsa_support_only
ON `${project_id}.d1_staged_enforced.student_onboarding`
GRANT TO ('serviceAccount:${staged_reader_sa}')
FILTER USING (requires_lsa_support = TRUE);
