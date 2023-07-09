import logging

import graphene
from django.apps import apps
from graphene import Enum

logger = logging.getLogger(__name__)


class StatusCode(Enum):
    success = 'SUCCESS'
    not_found = 'NOT_FOUND'
    error = 'ERROR'


class MutationBase:
    message = graphene.String(required=True)
    status_code = StatusCode(required=True)


class MutationMethods:
    @classmethod
    def create_object(cls, klass, owner, **kwargs):
        obj = None
        message = None
        status_code = None

        try:
            model = apps.get_model(app_label="screenshots", model_name=klass)
            obj, _ = model.objects.get_or_create(
                owner=owner,
                **kwargs
            )

            message = f"Successfully created {klass} #{obj.id}."
            status_code = StatusCode.success

        except Exception as e:
            logger.exception(e)
            tag = None
            message = f"Error while creating {klass}, please double-check sent data."
            status_code = StatusCode.error

        finally:
            return obj, message, status_code

    @classmethod
    def update_object(cls, klass, id, owner, include_deleted=False, **kwargs):
        obj = None
        message = None
        status_code = None

        try:
            args = {"owner": owner}

            if not include_deleted:
                args["deleted_at"] = None

            model = apps.get_model(app_label="screenshots", model_name=klass)

            obj = model.objects.get(id=id, **args)

            if obj:
                for key, value in kwargs.items():
                    setattr(obj, key, value)

                obj.save()

                message = f"Successfully updated {klass} #{obj.id}."
                status_code = StatusCode.success

            else:
                message = f"{klass} #{obj.id} not found."
                status_code = StatusCode.not_found

        except Exception as e:
            logger.exception(e)
            message = f"Error while updating {klass}, please double-check sent data."
            status_code = StatusCode.error

        finally:
            return obj, message, status_code

    @classmethod
    def delete_object(cls, klass, id, owner):
        message = None
        status_code = None

        try:
            model = apps.get_model(app_label="screenshots", model_name=klass)
            obj = model.objects.get(id=id)

            if obj:
                obj.delete()

                message = f"Successfully deleted {klass} #{obj.id}."
                status_code = StatusCode.success

            else:
                message = f"{klass} #{obj.id} not found."
                status_code = StatusCode.not_found

        except Exception as e:
            logger.exception(e)
            message = f"Error while deleting {klass} #{id}."
            status_code = StatusCode.error

        finally:
            return message, status_code
