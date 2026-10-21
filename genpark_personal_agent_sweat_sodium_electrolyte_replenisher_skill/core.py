# -*- coding: utf-8 -*-
"""Sweat Rate & Sodium Electrolyte Replenisher for GenPark Personal Agent."""
import json
from typing import Dict, Any

class SweatRateSodiumElectrolyteReplenisher:
    @staticmethod
    def calculate_sweat_fluid_electrolyte_deficit(pre_exercise_weight_kg: float, post_exercise_weight_kg: float, duration_minutes: float, fluid_consumed_ml: float = 0.0, ambient_temp_c: float = 22.0, relative_humidity_pct: float = 50.0) -> Dict[str, Any]:
        weight_loss_kg = max(0.0, pre_exercise_weight_kg - post_exercise_weight_kg)
        fluid_loss_liters = weight_loss_kg + (fluid_consumed_ml / 1000.0)
        hours = max(0.1, duration_minutes / 60.0)
        sweat_rate_l_hr = round(fluid_loss_liters / hours, 2)
        
        # Mean sodium sweat concentration ~900 mg / Liter (range 500-1500)
        heat_factor = 1.0 + max(0.0, (ambient_temp_c - 20.0) * 0.02)
        sodium_concentration_mg_l = round(900.0 * heat_factor, 0)
        total_sodium_deficit_mg = round(fluid_loss_liters * sodium_concentration_mg_l, 0)
        
        dehydration_pct = round((weight_loss_kg / pre_exercise_weight_kg) * 100.0, 1)
        
        return {
            "sweat_rate_liters_per_hour": sweat_rate_l_hr,
            "total_fluid_loss_liters": round(fluid_loss_liters, 2),
            "estimated_sodium_deficit_mg": total_sodium_deficit_mg,
            "acute_dehydration_loss_pct": dehydration_pct,
            "deficit_severity": "SEVERE_DEHYDRATION_PERFORMANCE_DROP" if dehydration_pct > 2.0 else "MILD_TOLERABLE_DEFICIT"
        }

    @staticmethod
    def formulate_hypotonic_electrolyte_dosing(sodium_loss_mg: float, remaining_duration_hours: float = 1.0) -> Dict[str, Any]:
        hourly_sodium_intake = round(min(1000.0, sodium_loss_mg / max(1.0, remaining_duration_hours) * 0.8), 0)
        hourly_potassium_mg = round(hourly_sodium_intake * 0.25, 0)
        hourly_magnesium_mg = round(hourly_sodium_intake * 0.08, 0)
        
        return {
            "target_hourly_fluid_ml": 750,
            "sodium_target_mg": hourly_sodium_intake,
            "potassium_target_mg": hourly_potassium_mg,
            "magnesium_glycinate_mg": hourly_magnesium_mg,
            "osmolality_target": "200-250 mOsm/kg (Hypotonic for rapid gastric absorption)",
            "carbohydrate_co_transport": "Add 2-3% maltodextrin/glucose to trigger active SGLT1 intestinal transport."
        }
