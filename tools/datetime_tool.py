from datetime import datetime
import zoneinfo

"""
    Obtiene la fecha y hora actual exacta para cualquier zona horaria estándar IANA.
    No consume APIs, no tiene límite de llamadas y responde en milisegundos.
"""

def get_current_time(timezone_name: str = "America/Lima") -> dict:
    try:
        tz = zoneinfo.ZoneInfo(timezone_name)
        now = datetime.now(tz)
        return {
            "fecha": now.strftime("%Y-%m-%d"),
            "hora": now.strftime("%H:%M:%S"),
            "dia": now.strftime("%A"),
            "zona_horaria": timezone_name,
            "utc_offset": now.strftime("%z")
        }
    except Exception:
        return {"error": f"Zona horaria no válida: {timezone_name}"}