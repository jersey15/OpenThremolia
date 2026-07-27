import pytest

from thremolia.threat import Report, Threat


@pytest.fixture(scope="module")
def threat_factory() -> Threat:
    def _create(**overrides):
        return Threat(
            id=overrides.get("id", 1),
            element=overrides.get("element", ""),
            threat_description=overrides.get("threat_description", ""),
            element_type=overrides.get("element_type", ""),
            stride=overrides.get("stride", ""),
            **{"Mitre ATT&CK": overrides.get("mitre_attack")},
            **{"OWASP Top 10 2025": overrides.get("owasp_top_10_2025")},
            mitre_atlas=overrides.get("mitre_atlas"),
            owasp_top_10_for_llm=overrides.get("owasp_top_10_for_llm"),
            linddun=overrides.get("linddun"),
            owasp_ml_sec_top_10_2023=overrides.get("owasp_ml_sec_top_10_2023"),
            mitigation=overrides.get("mitigation", ""),
            SDL_stage=overrides.get("SDL_stage", "Design"),
            cvss_vector=overrides.get("cvss_vector", ""),
            cvss_score=overrides.get("cvss_score"),
        )

    return _create


@pytest.fixture(scope="module")
def report_factory(threat_factory) -> Report:
    def _create(**overrides):
        return Report(
            message=overrides.get("message", "Test Message"),
            threats=[
                threat_factory(**override) for override in overrides.get("threats", [])
            ],
            is_final=overrides.get("is_final", True),
        )

    return _create
