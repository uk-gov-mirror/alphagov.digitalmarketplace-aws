import deploy_tools.paas_manifest


def test_app_manifest_includes_secrets_by_default(sops_decrypt):
    deploy_tools.paas_manifest.app_manifest("testing", "test-app")
    assert sop_decrypt.call
