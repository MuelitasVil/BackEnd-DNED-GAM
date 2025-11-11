# app/service/use_cases/export_email_lists.py
import asyncio
import csv
import os
from typing import Iterable, List

from app.clients.organization.headquarters_client import HeadquartersClient
from app.clients.organization.school_client import SchoolClient
from app.clients.organization.school_headquarters_associate_client import (
    SchoolHeadquartersAssociateClient as SchHqClient,
)
from app.clients.organization.unit_school_associate_client import (
    UnitSchoolAssociateClient as UsaClient,
)
from app.clients.organization.unit_unal_client import UnitUnalClient


# --------- utilidades de E/S (no bloqueantes) ----------
async def _async_write_csv(path: str, rows: Iterable[Iterable[str]]) -> None:
    # Escritura CSV simple en threadpool para no bloquear el event loop
    os.makedirs(os.path.dirname(path), exist_ok=True)

    def _write():
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for r in rows:
                w.writerow(r)

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _write)


def _to_rows_from_email_dtos(items: List) -> List[List[str]]:
    # items: lista de DTOs con atributos .email y .role
    rows = [["email", "role"]]
    for it in items:
        email = getattr(it, "email", "")
        role = getattr(it, "role", "")
        rows.append([email, role])
    return rows


async def _fetch_all_paginated(fetch_page_fn, *, page_size: int = 200) -> list:
    start = 0
    all_items = []
    while True:
        page = await fetch_page_fn(start=start, limit=page_size)
        if not page:
            break
        all_items.extend(page)
        if len(page) < page_size:
            break
        start += page_size
    return all_items


# --------- Servicio principal ----------
class ExportEmailListsService:
    """
    Genera CSVs por entidad:
      - headquarters/<cod_headquarters>__<period>.csv
      - schools/<cod_school>__<period>.csv
      - units/<cod_unit>__<period>.csv
    Recorre asociaciones School<->Headquarters y Unit<->School,
    y para cada entidad descarga su lista de emails.
    """

    def __init__(self, out_dir: str = "exports"):
        self.out_dir = out_dir
        self.dir_hq = os.path.join(out_dir, "headquarters")
        self.dir_school = os.path.join(out_dir, "schools")
        self.dir_unit = os.path.join(out_dir, "units")

    async def generate_for_headquarters(
        self,
        cod_headquarters: str,
        cod_period: str,
    ) -> None:
        # 1) HEADQUARTERS -> CSV
        hq_emails = await HeadquartersClient.fetch_email_list_of_headquarters(
            cod_headquarters, cod_period
        )
        hq_rows = _to_rows_from_email_dtos(hq_emails)
        hq_path = os.path.join(
            self.dir_hq, f"{cod_headquarters}__{cod_period}.csv"
        )

        # 2) SCHOOLS asociados a ese HQ (filtrando por periodo)
        all_sch_hq = await _fetch_all_paginated(SchHqClient.fetch_associations)
        sch_for_hq = [
            a for a in all_sch_hq
            if (
                a.cod_headquarters == cod_headquarters
                and a.cod_period == cod_period
            )
        ]
        # Extraemos códigos de escuela únicos
        school_codes = sorted({a.cod_school for a in sch_for_hq})

        """
        3) Para cada SCHOOL: CSV + buscar sus UNITS por asociaciones Unit<->School  # noqa: E501
        """
        async def process_school(cod_school: str):
            # CSV de la escuela
            school_emails = await SchoolClient.fetch_email_list_of_school(
                cod_school, cod_period
            )
            school_rows = _to_rows_from_email_dtos(school_emails)
            school_path = os.path.join(
                self.dir_school, f"{cod_school}__{cod_period}.csv"
            )

            # Asociaciones Unit<->School de esa escuela y periodo
            all_usa = await _fetch_all_paginated(UsaClient.fetch_associations)
            usa_for_school = [
                u
                for u in all_usa
                if (
                    u.cod_school == cod_school
                    and u.cod_period == cod_period
                )
            ]
            unit_codes = sorted({u.cod_unit for u in usa_for_school})

            # Para cada UNIT: CSV
            sem_units = asyncio.Semaphore(10)

            async def process_unit(cod_unit: str):
                async with sem_units:
                    unit_emails = await UnitUnalClient.fetch_email_list_of_unit(  # noqa: E501
                        cod_unit,
                        cod_period,
                    )
                    unit_rows = _to_rows_from_email_dtos(unit_emails)
                    unit_path = os.path.join(
                        self.dir_unit, f"{cod_unit}__{cod_period}.csv"
                    )
                    await _async_write_csv(unit_path, unit_rows)

            await asyncio.gather(*(process_unit(u) for u in unit_codes))
            await _async_write_csv(school_path, school_rows)

        # Concurrency control para escuelas
        sem_schools = asyncio.Semaphore(8)

        async def guarded_process_school(code: str):
            async with sem_schools:
                await process_school(code)

        # Lanzar todo concurrente: HQ CSV + (todas las escuelas y sus units)
        await asyncio.gather(
            _async_write_csv(hq_path, hq_rows),
            *(guarded_process_school(s) for s in school_codes),
        )
