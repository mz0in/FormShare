import gettext
import multiprocessing
import os
import time
import uuid
from subprocess import Popen, PIPE

from celery.utils.log import get_task_logger
from formshare.config.celery_app import celeryApp
from formshare.config.celery_class import CeleryTask
from formshare.processes.email.send_async_email import send_async_email

log = get_task_logger(__name__)


class BuildFileError(Exception):
    """
    Exception raised when there is an error while creating the repository.
    """


class SheetNameError(Exception):
    """
    Exception raised when there is an error while creating the repository.
    """


def internal_build_xlsx(
    settings,
    odk_dir,
    form_schema,
    create_xml,
    encryption_key,
    xlsx_file,
    protect_sensitive,
    locale,
    options=1,
    include_multiselect=False,
    include_lookups=False,
):
    if (
        os.environ.get("FORMSHARE_PYTEST_RUNNING", "false") == "true"
        and protect_sensitive
    ):
        print("In testing. Waiting 10 seconds so we can test cancelling the task")
        time.sleep(10)
    parts = __file__.split("/products/")
    this_file_path = parts[0] + "/locale"
    es = gettext.translation("formshare", localedir=this_file_path, languages=[locale])
    es.install()
    _ = es.gettext

    mysql_user = settings["mysql.user"]
    mysql_password = settings["mysql.password"]
    mysql_host = settings["mysql.host"]
    mysql_port = settings["mysql.port"]
    odk_tools_dir = settings["odktools.path"]

    paths = [odk_tools_dir, "utilities", "MySQLToXLSX", "mysqltoxlsx"]
    mysql_to_xlsx = os.path.join(odk_dir, *paths)

    uid = str(uuid.uuid4())

    paths = ["tmp", uid]
    temp_dir = os.path.join(odk_dir, *paths)
    os.makedirs(temp_dir)

    num_workers = (
        multiprocessing.cpu_count() - int(settings.get("server:threads", "1")) - 1
    )
    if num_workers <= 0:
        num_workers = 1

    args = [
        mysql_to_xlsx,
        "-H " + mysql_host,
        "-P " + mysql_port,
        "-u " + mysql_user,
        "-p " + mysql_password,
        "-s " + form_schema,
        "-x " + create_xml,
        "-o " + xlsx_file,
        "-T " + temp_dir,
        "-e " + encryption_key,
        "-r {}".format(options),
        "-w {}".format(num_workers),
    ]
    if protect_sensitive:
        args.append("-c")
    if include_multiselect:
        args.append("-m")
    if include_lookups:
        args.append("-l")

    log.info(" ".join(args))

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        return True, xlsx_file
    else:
        email_from = settings.get("mail.from", None)
        email_to = settings.get("mail.error", None)
        send_async_email(
            settings,
            email_from,
            email_to,
            "MySQLToXLSX Error",
            "Error: "
            + stderr.decode("utf-8")
            + "-"
            + stdout.decode("utf-8")
            + ":"
            + " ".join(args),
            None,
            locale,
        )
        log.error(
            "MySQLToXLSX Error: "
            + stderr.decode()
            + "-"
            + stdout.decode()
            + ". Args: "
            + " ".join(args)
        )
        error = stdout.decode() + stderr.decode()
        if error.find("Worksheet name is already in use") >= 0:
            raise SheetNameError(
                _(
                    "A worksheet name has been repeated. Excel only allow 30 characters in the worksheet name. "
                    "You can fix this by editing the dictionary and change the description of the tables "
                    "to a maximum of "
                    "30 characters."
                )
            )
        else:
            raise BuildFileError(
                _(
                    "Unknown error while creating the XLSX. Sorry about this. "
                    "Please report this error as an issue on https://github.com/qlands/FormShare"
                )
            )


@celeryApp.task(bind=True, base=CeleryTask)
def build_xlsx(
    self,
    settings,
    odk_dir,
    form_schema,
    create_xml,
    encryption_key,
    xlsx_file,
    protect_sensitive,
    locale,
    options=1,
    include_multiselect=False,
    include_lookups=False,
):
    internal_build_xlsx(
        settings,
        odk_dir,
        form_schema,
        create_xml,
        encryption_key,
        xlsx_file,
        protect_sensitive,
        locale,
        options,
        include_multiselect,
        include_lookups,
    )
