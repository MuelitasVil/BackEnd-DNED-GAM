import subprocess

from fastapi import HTTPException
from app.utils.app_logger import AppLogger

logger = AppLogger(__file__, "gam_client.log")


class GamClient:
    @staticmethod
    def call_gam_command(command: list) -> subprocess.CompletedProcess:
        """Método interno para ejecutar un comando GAM"""
        try:
            logger.info(f"Executing GAM command: {' '.join(command)}")
            result = subprocess.run(
                command, text=True, capture_output=True, check=True
            )
            logger.info(f"GAM command succeeded: {result.stdout}")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"GAM command failed: {e.stderr}")
            raise HTTPException(
                status_code=400,
                detail=f"GAM command failed: {e}"
            )

    @staticmethod
    def test_connection() -> bool:
        """Verifica la conexión con GAM ejecutando el comando 'gam version'"""
        command = ['gam', 'version']
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info("GAM connection is successful.")
            return True
        else:
            logger.error("Failed to connect to GAM.")
            return False
