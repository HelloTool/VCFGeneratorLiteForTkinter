import json
import os
import pkgutil
import sys
from typing import Optional

from vcf_generator_lite import constants

_APP_MODULE_NAME = "vcf_generator_lite"


def get_asset_data(resource: str) -> Optional[bytes]:
    return pkgutil.get_data(_APP_MODULE_NAME, os.path.join('assets', resource))


def get_asset_scaled_data(resources: list[(float, str)], scale: float) -> Optional[bytes]:
    sorted_resources = sorted(resources, key=lambda x: x[0], reverse=True)
    for resource_scale, resource in sorted_resources:
        if scale >= resource_scale:
            return get_asset_data(resource)
    return get_asset_data(resources[0])


def get_asset_path(file_name: str) -> str:
    """
    Get the path to the file in the assets' folder.
    :param file_name: The name of the file.
    :return: The path to the file.
    """
    return os.path.join(os.path.dirname(sys.modules[_APP_MODULE_NAME].__file__), "assets", file_name)


def _get_os_notice_html() -> str:
    projects = json.loads(get_asset_data('data/os_notice.json'))
    return "<br />".join([
        '<a href="{url}">{name}</a> - <a href="{license_url}">{license}</a>'.format(
            url=item["url"],
            name=item["name"],
            license=item["license"],
            license_url=item["license_url"]
        ) for item in projects
    ])


def get_about_html() -> str:
    about_html = get_asset_data('texts/about.html').decode('UTF-8', 'ignore')
    return about_html.format(
        source_url=constants.URL_SOURCE,
        release_url=constants.URL_RELEASES,
        jesse205_email=constants.EMAIL_JESSE205,
        os_notice_html=_get_os_notice_html()
    )
