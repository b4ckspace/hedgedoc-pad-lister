from base64 import urlsafe_b64encode

from flask import Flask, render_template
from sqlalchemy import func

from .db import SCHEMA_VERSION, Note, Permission, Revision, SequelizeMeta, db


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_prefixed_env()
    else:
        app.config.from_mapping(config)

    db.init_app(app)

    base_url = app.config["BASE_URL"].rstrip("/")

    @app.route("/")
    def index():
        if (
            db.session.execute(db.select(func.max(SequelizeMeta.name))).scalar()
            != SCHEMA_VERSION
        ):
            return render_template(
                "error.html",
                message="Database schema is possibly outdated; please check and update if required.",
            )

        print(db.select(Note).join(Note.revisions).order_by(Note.lastchangeAt))

        pads = []
        for note in db.session.execute(
            db.select(Note).order_by(Note.lastchangeAt.desc())
        ).scalars():
            if (
                note.permission not in (Permission.editable, Permission.freely)
                or not note.lastchangeAt
            ):
                continue

            note_id = (
                note.alias
                if note.alias
                else urlsafe_b64encode(note.id.bytes).decode("utf-8").rstrip("=")
            )
            pads.append(
                {
                    "last_change": note.lastchangeAt.isoformat(" ", timespec="seconds"),
                    "name": (
                        note.title
                        if note.title != "Untitled"
                        else note.alias or note_id
                    ),
                    "revision": len(note.revisions),
                    "url": f"{base_url}/{note_id}",
                }
            )
        return render_template("index.html", pads=pads)

    return app
