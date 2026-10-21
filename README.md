# Sweat Rate & Sodium Electrolyte Dynamic Replenisher Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Sodium loss rate from sweat rate and ambient wet-bulb globe temperature (WBGT), hypotonic vs isotonic electrolyte formulation, and osmolality target. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_sweat_fluid_electrolyte_deficit`: Calculate sweat fluid loss rate (L/hr) and total sodium deficit from pre/post bodyweight change.
- `formulate_hypotonic_electrolyte_dosing`: Formulate targeted hypotonic drink mix (sodium, potassium, magnesium) to optimize gastric emptying rate.

## 🚀 Installation & Usage
```bash
python -m genpark_personal_agent_sweat_sodium_electrolyte_replenisher_skill.server --test
```
