import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from library.models import Group


class Command(BaseCommand):
    help = "Import Steam group into database"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("group_name", type=str)

    def handle(self, *args, **options):
        url = f"https://steamcommunity.com/groups/{options['group_name']}/memberslistxml/?xml=1"
        r = requests.get(url=url)

        site = Site.objects.get(pk=settings.SITE_ID)

        # Steam doesn't return something else than HTTP 200 event if group doesn't exist...
        try:
            payload = ET.fromstring(r.text)

            # Make sure we have a valid XML tree
            assert payload.tag == "memberList"

            group, created = Group.objects.update_or_create(
                group_id=payload.find("groupID64").text,
                defaults={
                    "name": payload.find("./groupDetails/groupName").text,
                    "headline": payload.find("./groupDetails/headline").text,
                    "url": f"https://steamcommunity.com/groups/{options['group_name']}",
                    "avatar_url": payload.find("./groupDetails/avatarIcon").text,
                    "avatar_m_url": payload.find("./groupDetails/avatarMedium").text,
                    "avatar_f_url": payload.find("./groupDetails/avatarFull").text,
                    "site": site,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS("Group imported for default site"))
        except (AssertionError, ET.ParseError):
            self.stderr.write(
                self.style.ERROR(
                    "Could not parse group details. Please check its name."
                )
            )
