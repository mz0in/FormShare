import os
import time
import uuid

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from .sql import get_form_details


def t_e_s_t_json_logs_4(test_object):
    # Adds a mimic2 project
    json4_project = "json4"
    json4_project_id = str(uuid.uuid4())
    mimic_res = test_object.testapp.post(
        "/user/{}/projects/add".format(test_object.randonLogin),
        {
            "project_id": json4_project_id,
            "project_code": json4_project,
            "project_name": "Test project",
            "project_abstract": "",
            "project_icon": "",
            "project_hexcolor": "",
            "project_formlist_auth": 1,
        },
        status=302,
    )
    assert "FS_error" not in mimic_res.headers
    # Add the mimic form
    mimic_paths = ["resources", "forms", "complex_form", "B.xlsx"]
    resource_file = os.path.join(test_object.path, *mimic_paths)
    mimic_res = test_object.testapp.post(
        "/user/{}/project/{}/forms/add".format(test_object.randonLogin, json4_project),
        {"form_pkey": "I_D"},
        status=302,
        upload_files=[("xlsx", resource_file)],
    )
    assert "FS_error" not in mimic_res.headers
    json4_form = "LB_Sequia_MAG_20190123"

    # Uploads a file to the form
    paths = ["resources", "forms", "complex_form", "cantones.csv"]
    resource_file = os.path.join(test_object.path, *paths)
    res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/upload".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        status=302,
        upload_files=[("filetoupload", resource_file)],
    )
    assert "FS_error" not in res.headers

    # Uploads a file to the form
    paths = ["resources", "forms", "complex_form", "distritos.csv"]
    resource_file = os.path.join(test_object.path, *paths)
    res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/upload".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        status=302,
        upload_files=[("filetoupload", resource_file)],
    )
    assert "FS_error" not in res.headers

    mimic_res = test_object.testapp.post(
        "/user/{}/project/{}/assistants/add".format(
            test_object.randonLogin, json4_project
        ),
        {
            "coll_id": "json4001",
            "coll_name": "json4001",
            "coll_password": "123",
            "coll_password2": "123",
            "coll_prjshare": 1,
        },
        status=302,
    )
    assert "FS_error" not in mimic_res.headers

    # Add an assistant to a form succeeds
    mimic_res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/assistants/add".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        {
            "coll_id": "{}|{}".format(json4_project_id, "json4001"),
            "coll_can_submit": "1",
            "coll_can_clean": "1",
        },
        status=302,
    )
    assert "FS_error" not in mimic_res.headers

    # Generate the repository using celery
    res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/repository/create".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        {"form_pkey": "I_D", "start_stage1": ""},
        status=302,
    )
    assert "FS_error" not in res.headers

    time.sleep(60)  # Wait for Celery to finish

    # Upload submission 1
    paths = [
        "resources",
        "forms",
        "complex_form",
        "submissions_logs2",
        "submission001.xml",
    ]
    submission_file = os.path.join(test_object.path, *paths)
    paths = ["resources", "forms", "complex_form", "image001.png"]
    image_file = os.path.join(test_object.path, *paths)

    paths = ["resources", "forms", "complex_form", "sample.mp3"]
    sound_file = os.path.join(test_object.path, *paths)

    test_object.testapp.post(
        "/user/{}/project/{}/push".format(test_object.randonLogin, json4_project),
        status=201,
        upload_files=[
            ("filetoupload", submission_file),
            ("image", image_file),
            ("sound", sound_file),
        ],
        extra_environ=dict(FS_for_testing="true", FS_user_for_testing="json4001"),
    )
    time.sleep(5)  # Wait for ElasticSearch to store this

    # Upload submission 2 goes to logs
    paths = [
        "resources",
        "forms",
        "complex_form",
        "submissions_logs2",
        "submission003.xml",
    ]
    submission_file = os.path.join(test_object.path, *paths)
    paths = ["resources", "forms", "complex_form", "image001.png"]
    image_file = os.path.join(test_object.path, *paths)

    paths = ["resources", "forms", "complex_form", "sample.mp3"]
    sound_file = os.path.join(test_object.path, *paths)

    test_object.testapp.post(
        "/user/{}/project/{}/push".format(test_object.randonLogin, json4_project),
        status=201,
        upload_files=[
            ("filetoupload", submission_file),
            ("image", image_file),
            ("sound", sound_file),
        ],
        extra_environ=dict(FS_for_testing="true", FS_user_for_testing="json4001"),
    )
    time.sleep(5)  # Wait for ElasticSearch to store this

    form_details = get_form_details(
        test_object.server_config, json4_project_id, json4_form
    )
    print("Wait a bit longer for slower machines")
    time.sleep(10)  # Wait a bit longer for slower machines
    engine = create_engine(
        test_object.server_config["sqlalchemy.url"], poolclass=NullPool
    )
    sql = "SELECT rowuuid FROM {}.maintable WHERE i_d = '109750690'".format(
        form_details["form_schema"]
    )
    res = engine.execute(sql).first()
    row_uuid = res[0]

    sql = (
        "SELECT submission_id FROM formshare.submission "
        "WHERE submission_status = 2 AND sameas IS NULL AND project_id = '{}' AND form_id = '{}'".format(
            json4_project_id, json4_form
        )
    )
    res = engine.execute(sql).fetchall()
    duplicated_ids = []
    for a_duplicate in res:
        duplicated_ids.append(a_duplicate[0])
    engine.dispose()

    test_object.testapp.post(
        "/user/{}/project/{}/form/{}/submissions/delete".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        {
            "move_submission": "",
            "rowuuid": row_uuid,
            "coll_id": "{}|{}".format(json4_project_id, "json4001"),
        },
        status=302,
    )

    res = test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/login".format(
            test_object.randonLogin, json4_project
        ),
        {"login": "json4001", "passwd": "123"},
        status=302,
    )
    assert "FS_error" not in res.headers

    test_object.testapp.get(
        "/user/{}/project/{}/assistantaccess/form/{}/errors".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        status=200,
    )

    test_object.testapp.get(
        "/user/{}/project/{}/assistantaccess/form/{}/errors?status=error".format(
            test_object.randonLogin, json4_project, json4_form
        ),
        status=200,
    )

    # Change the assistant to submit only
    res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/assistant/{}/{}/edit".format(
            test_object.randonLogin,
            json4_project,
            json4_form,
            json4_project_id,
            "json4001",
        ),
        {"coll_can_submit": "1"},
        status=302,
    )
    assert "FS_error" not in res.headers

    test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/form/{}/{}/push".format(
            test_object.randonLogin, json4_project, json4_form, duplicated_ids[0]
        ),
        status=403,
    )

    # Change the assistant to both
    res = test_object.testapp.post(
        "/user/{}/project/{}/form/{}/assistant/{}/{}/edit".format(
            test_object.randonLogin,
            json4_project,
            json4_form,
            json4_project_id,
            "json4001",
        ),
        {"coll_can_submit": "1", "coll_can_clean": "1"},
        status=302,
    )
    assert "FS_error" not in res.headers

    test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/form/{}/{}/push".format(
            test_object.randonLogin, json4_project, json4_form, "Not_exist"
        ),
        status=404,
    )

    test_object.testapp.get(
        "/user/{}/project/{}/assistantaccess/form/{}/{}/push".format(
            test_object.randonLogin, json4_project, json4_form, duplicated_ids[0]
        ),
        status=404,
    )

    res = test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/form/{}/{}/push".format(
            test_object.randonLogin, json4_project, json4_form, duplicated_ids[0]
        ),
        status=302,
    )
    assert "FS_error" not in res.headers

    test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/form/{}/{}/push".format(
            test_object.randonLogin, json4_project, json4_form, duplicated_ids[0]
        ),
        status=404,
    )

    res = test_object.testapp.post(
        "/user/{}/project/{}/assistantaccess/logout".format(
            test_object.randonLogin, json4_project
        ),
        status=302,
    )
    assert "FS_error" not in res.headers
