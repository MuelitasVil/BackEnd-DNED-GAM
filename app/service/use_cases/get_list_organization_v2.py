from typing import List

from app.clients.organization.headquarters_client import HeadquartersClient
from app.clients.organization.school_client import SchoolClient
from app.clients.organization.unit_unal_client import UnitUnalClient
from app.domain.dtos.organization.email_dto import EmailDTO
from app.utils.app_logger import AppLogger


logger = AppLogger("ExportEmailListsService")


# Este método orquesta la ejecución de obtener correos electrónicos
async def generate_for_headquarters(
        cod_headquarters: str,
        cod_period: str,
) -> None:

    logger.info(f"Starting : {cod_headquarters}, period: {cod_period}")

    headquarters_emails = await get_headquarters_emails(
        cod_headquarters, cod_period
        )

    logger.info(
        f"Found {len(headquarters_emails)}"
        f"emails for headquarters {cod_headquarters}"
        )

    school_dict = {}
    for headquarters_email in headquarters_emails:
        school_emails = await get_schools_emails(
            headquarters_email.email, cod_period
        )
        school_dict[headquarters_email.email] = school_emails

        logger.info(
            f"Found {len(school_emails)} emails for school in headquarters"
            f"{headquarters_email.email}"
        )

        # 3. Para cada escuela, obtener los correos de las unidades
        unit_dict = {}
        for school_email in school_emails:
            unit_emails = await get_units_emails(
                school_email.email, cod_period
            )

            unit_dict[school_email.email] = unit_emails
            logger.info(
                f"Found {len(unit_emails)}"
                f"emails for unit in school {school_email.email}"
            )

    return headquarters_emails, school_dict, unit_dict


async def get_headquarters_emails(
        cod_headquarters: str, cod_period: str
) -> List[EmailDTO]:
    return await HeadquartersClient.fetch_email_list_of_headquarters(
        cod_headquarters, cod_period
    )


async def get_schools_emails(
        cod_school: str, cod_period: str
) -> List[EmailDTO]:
    return await SchoolClient.fetch_email_list_of_school(
        cod_school, cod_period
    )


async def get_units_emails(
        cod_unit: str, period: str
) -> List[EmailDTO]:
    return await UnitUnalClient.fetch_email_list_of_unit(
        cod_unit, period
    )
