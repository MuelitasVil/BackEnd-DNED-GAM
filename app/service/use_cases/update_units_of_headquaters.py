import asyncio
from typing import List
from app.utils.app_logger import AppLogger
from fastapi import BackgroundTasks

from app.domain.dtos.organization.headquarters_dto import HeadquartersDTO
from app.domain.dtos.organization.school_headquarters_associate_dto import (
    SchoolHeadquartersAssociateDTO as schClientDTO,
)
from app.domain.dtos.organization.unit_school_associate_dto import (
    UnitSchoolAssociateDTO as unitSchoolDTO,
)
from app.domain.dtos.organization.email_dto import (
    EmailDTO as Email,
)

from app.clients.organization.headquarters_client import (
    HeadquartersClient as HqClient
)
from app.clients.organization.school_headquarters_associate_client import (
    SchoolHeadquartersAssociateClient as SchHqClient,
)
from app.clients.organization.unit_school_associate_client import (
    UnitSchoolAssociateClient as UnitSchClient,
)
from app.clients.organization.unit_unal_client import (
    UnitUnalClient as UnitUnalClient,
)
from app.service.gam.gam_group_service import (
    GamGroupService
)

logger = AppLogger(__file__, "update_unis_of_headquaters.log")
semaphore = asyncio.Semaphore(10)


async def update_units_of_headquarters(name: str, period: str) -> None:
    background_tasks: BackgroundTasks = BackgroundTasks()

    headquarters: List[HeadquartersDTO] = await (
        HqClient.fetch_headquarters_by_name(name)
    )

    logger.info(f"Period: {period}")
    logger.info(f"Found {len(headquarters)} headquarters with name {name}")
    background_tasks.add_task(_loggerHeadQuarters, headquarters)

    schools_in_headquarters: List[schClientDTO] = []
    schools_in_headquarters = await _get_schools_in_headquarters(
        period, headquarters
    )
    background_tasks.add_task(
        _loggerSchoolsInHeadquarters,
        schools_in_headquarters
    )

    logger.info(
        f"Found {len(schools_in_headquarters)} schools in headquarters"
    )

    unit_in_schools: List[unitSchoolDTO] = []
    unit_in_schools = await _get_units_in_schools(
        period, schools_in_headquarters
    )
    background_tasks.add_task(_loggerUnitsInSchools, unit_in_schools)

    logger.info(f"Found {len(unit_in_schools)} units in schools")

    units_email_senders: dict[str, List[Email]] = {}
    units_email_senders = await _get_email_senders_by_units(
        unit_in_schools, period
    )
    background_tasks.add_task(_loggerEmailsByUnits, units_email_senders)

    for unit_email_sender in units_email_senders:
        GamGroupService.update_group(
            unit_email_sender,
            units_email_senders[unit_email_sender]
        )

    return {
            "detail": f"Update of units for headquarters "
            f"{name} in period {period} attempted",
            "cant of updaated units": len(unit_in_schools)
            }


async def _get_schools_in_headquarters(
    period: str,
    headquarters: List[HeadquartersDTO],
) -> List[schClientDTO]:
    tasks = []
    for hq in headquarters:
        tasks.append(_fetch_schools_for_headquarter(hq, period))

    all_schools = await asyncio.gather(*tasks)
    schools_in_headquarters = [
        school for sublist in all_schools for school in sublist
    ]
    return schools_in_headquarters


async def _fetch_schools_for_headquarter(
    hq: HeadquartersDTO,
    period: str,
) -> List[schClientDTO]:
    try:
        temp_schools: List[schClientDTO] = await (
            SchHqClient.fetch_associations_by_headquarters(
                cod_headquarters=hq.cod_headquarters,
                period=period,
            )
        )
        return temp_schools
    except Exception as e:
        logger.error(
            f"Failed fetching associations for headquarters"
            f"  {hq.cod_headquarters}: {e}"
            )
        return []


async def _get_units_in_schools(
    period: str,
    schools_in_headquarters: List[schClientDTO],
) -> List[unitSchoolDTO]:
    tasks = [
        fetch_units_for_school(sch, period)
        for sch in schools_in_headquarters
    ]
    all_units = await asyncio.gather(*tasks)
    unit_in_schools = [
        unit for sublist in all_units for unit in sublist
    ]
    return unit_in_schools


async def fetch_units_for_school(
        sch: schClientDTO, period: str
) -> List[unitSchoolDTO]:
    try:
        temp_units: List[unitSchoolDTO] = await (
            UnitSchClient.fetch_associations_by_school(
                cod_school=sch.cod_school,
                period=period,
            )
        )
        return temp_units
    except Exception as e:
        logger.error(
            f"Failed fetching associations for school"
            f" {sch.cod_school}: {e}")
        return []


async def _get_email_senders_by_units(
    unit_in_schools: List[unitSchoolDTO],
    period: str,
) -> dict[str, List[Email]]:
    tasks = [fetch_emails_for_unit(unit, period) for unit in unit_in_schools]
    all_emails = await asyncio.gather(*tasks)
    units_email_senders = {
        unit.cod_unit: emails
        for unit, emails
        in zip(unit_in_schools, all_emails)
    }
    return units_email_senders


async def fetch_emails_for_unit(
        unit: unitSchoolDTO,
        period: str
) -> List[Email]:
    try:
        temp_emails: List[Email] = (
            await UnitUnalClient.fetch_email_list_of_unit(
                cod_unit=unit.cod_unit,
                period=period
            )
        )
        return temp_emails
    except Exception as e:
        logger.error(
            f"Failed fetching email senders for unit"
            f" {unit.cod_unit}: {e}")
        return []


def _loggerHeadQuarters(headquarters: List[HeadquartersDTO]) -> None:
    for hq in headquarters:
        logger.info(f"Headquarters Code: {hq.cod_headquarters}")


def _loggerSchoolsInHeadquarters(
        schools_in_headquarters: List[schClientDTO]
) -> None:
    for sch in schools_in_headquarters:
        logger.info(
            f"School Code: {sch.cod_school}, "
            f"Headquarters Code: {sch.cod_headquarters}"
        )


def _loggerUnitsInSchools(unit_in_schools: List[unitSchoolDTO]) -> None:
    for unit in unit_in_schools:
        logger.info(
            f"Unit Code: {unit.cod_unit}, School Code: {unit.cod_school}"
        )


def _loggerEmailsByUnits(units_email_senders: dict[str, List[Email]]) -> None:
    for cod_unit in units_email_senders.keys():
        logger.info(f"Emails for Unit Code: {cod_unit}")
        emails = units_email_senders[cod_unit]
        for email in emails:
            logger.info(f" - Email: {email.email}, Role: {email.role}")
