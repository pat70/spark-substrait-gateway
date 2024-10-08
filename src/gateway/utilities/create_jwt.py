# SPDX-License-Identifier: Apache-2.0
"""A utility to create a JWT token for the gateway."""

import logging
import os
import time

import click
import jwt

# Constants
DEFAULT_JWT_LIFETIME: int = 3600 * 24 * 365  # 1 year

_LOGGER = logging.getLogger(__name__)


@click.command()
@click.option(
    "--issuer",
    type=str,
    default=os.getenv("JWT_ISSUER", "spark-substrait-gateway"),
    show_default=True,
    required=True,
    help="The issuer to set within the JWT.",
)
@click.option(
    "--subject",
    type=str,
    default=os.getenv("JWT_SUBJECT", "spark-client-user"),
    show_default=True,
    required=True,
    help="The subject to set within the JWT.",
)
@click.option(
    "--audience",
    type=str,
    default=os.getenv("JWT_AUDIENCE", "spark-client"),
    show_default=True,
    required=True,
    help="The audience to set within the JWT.",
)
@click.option(
    "--lifetime",
    type=int,
    default=DEFAULT_JWT_LIFETIME,
    show_default=True,
    required=True,
    help="The lifetime (in seconds) for the JWT.",
)
@click.option(
    "--secret-key",
    type=str,
    default=os.getenv("SECRET_KEY"),
    required=True,
    help="The secret key used to sign the JWT.",
)
def main(issuer: str, subject: str, audience: str, lifetime: int, secret_key: str):
    """Create a JWT token for the given issuer, subject, audience, lifetime and secret key."""
    iat = time.time()
    exp = iat + lifetime
    payload = {"iss": issuer, "sub": subject, "aud": audience, "iat": iat, "exp": exp}
    signed_jwt = jwt.encode(payload=payload, key=secret_key, algorithm="HS256")

    _LOGGER.info(msg=signed_jwt)


if __name__ == "__main__":
    main()
