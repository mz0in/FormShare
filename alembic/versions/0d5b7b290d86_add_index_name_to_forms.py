"""Add index name to forms

Revision ID: 0d5b7b290d86
Revises: 389ebd4096fc
Create Date: 2020-04-20 15:08:24.264749

"""
import time

import requests
import sqlalchemy as sa
from alembic import context
from alembic import op
from formshare.models.formshare import Odkform, Project, Userproject
from formshare.processes.elasticsearch.repository_index import create_connection
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision = "0d5b7b290d86"
down_revision = "389ebd4096fc"
branch_labels = None
depends_on = None


def upgrade():
    config_uri = context.config.get_main_option("formshare.ini.file", None)
    if config_uri is None:
        print(
            "This migration needs parameter 'formshare.ini.file' in the alembic ini file."
        )
        print(
            "The parameter 'formshare.ini.file' must point to the full path of the FormShare ini file"
        )
        exit(1)

    setup_logging(config_uri)
    settings = get_appsettings(config_uri, "formshare")

    es_host = settings.get("elasticsearch.repository.host", "localhost")
    es_port = settings.get("elasticsearch.repository.port", 9200)
    use_ssl = settings.get("elasticsearch.repository.use_ssl", "False")

    op.add_column("odkform", sa.Column("form_index", sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###
    session = Session(bind=op.get_bind())
    forms = session.query(Odkform.project_id, Odkform.form_id).all()
    if forms:
        ready = False
        print("Waiting for ES to be ready")
        while not ready:
            if use_ssl == "False":
                resp = requests.get(
                    "http://{}:{}/_cluster/health".format(es_host, es_port)
                )
            else:
                resp = requests.get(
                    "https://{}:{}/_cluster/health".format(es_host, es_port)
                )
            data = resp.json()
            if data["status"] == "yellow" or data["status"] == "green":
                ready = True
            else:
                time.sleep(30)
        print("ES is ready")

        es_connection = create_connection(settings)
        if es_connection is None:
            print("Cannot connect to ElasticSearch")
            exit(1)
        for a_form in forms:
            project_code = (
                session.query(Project.project_code)
                .filter(Project.project_id == a_form.project_id)
                .first()
            )
            project_owner = (
                session.query(Userproject.user_id)
                .filter(Userproject.project_id == a_form.project_id)
                .filter(Userproject.access_type == 1)
                .first()
            )
            index_name = (
                project_owner.user_id.lower()
                + "_"
                + project_code.project_code.lower()
                + "_"
                + a_form.form_id.lower()
            )
            session.query(Odkform).filter(
                Odkform.project_id == a_form.project_id
            ).filter(Odkform.form_id == a_form.form_id).update(
                {"form_index": index_name}
            )
            if es_connection.indices.exists(index_name):
                es_connection.indices.put_mapping(
                    {"properties": {"_geolocation": {"type": "geo_point"}}},
                    index_name,
                    "dataset",
                    request_timeout=1200,
                )
                time.sleep(
                    10
                )  # Allow ElasticSearch to replicate the mappings across shards

    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("odkform", "form_index")
    # ### end Alembic commands ###
