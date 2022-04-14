"""Telemetry models."""

from django.db import models


class BuildDataManager(models.Manager):

    """Manager for the BuildData model."""

    def collect(self, build, data):
        """
        Save the collected information from a build.

        We fill other fields from data we have access to
        before saving it, like the project, version, organization, etc.
        """
        data["build"] = {
            "id": build.id,
            "start": build.date.isoformat(),
            "length": build.length,
            "commit": build.commit,
            "success": build.success,
        }
        data["project"] = {"id": build.project.id, "slug": build.project.slug}
        data["version"] = {
            "id": build.version.id,
            "slug": build.version.slug,
        }
        org = build.project.organizations.first()
        if org:
            data["organization"] = {
                "id": org.id,
                "slug": org.slug,
            }
        data["config"]["final"] = build.config
        return self.create(data=data)


class BuildData(models.Model):

    data = models.JSONField()
    objects = BuildDataManager()
