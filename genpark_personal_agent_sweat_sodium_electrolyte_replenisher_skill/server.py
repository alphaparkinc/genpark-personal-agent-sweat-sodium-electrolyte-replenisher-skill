# -*- coding: utf-8 -*-
"""MCP Server for Sweat Rate & Sodium Electrolyte Dynamic Replenisher Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import SweatRateSodiumElectrolyteReplenisher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_sweat_fluid_electrolyte_deficit",
        "description": "Calculate sweat fluid loss rate (L/hr) and total sodium deficit from pre/post bodyweight change.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pre_exercise_weight_kg": {
                    "type": "number"
                },
                "post_exercise_weight_kg": {
                    "type": "number"
                },
                "fluid_consumed_ml": {
                    "type": "number"
                },
                "duration_minutes": {
                    "type": "number"
                },
                "ambient_temp_c": {
                    "type": "number"
                },
                "relative_humidity_pct": {
                    "type": "number"
                }
            },
            "required": [
                "pre_exercise_weight_kg",
                "post_exercise_weight_kg",
                "duration_minutes"
            ]
        }
    },
    {
        "name": "formulate_hypotonic_electrolyte_dosing",
        "description": "Formulate targeted hypotonic drink mix (sodium, potassium, magnesium) to optimize gastric emptying rate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sodium_loss_mg": {
                    "type": "number"
                },
                "remaining_duration_hours": {
                    "type": "number"
                }
            },
            "required": [
                "sodium_loss_mg"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-sweat-sodium-electrolyte-replenisher-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(SweatRateSodiumElectrolyteReplenisher, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-sweat-sodium-electrolyte-replenisher-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
