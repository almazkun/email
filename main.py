import imaplib
import logging
import email
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReceivedEmails:
    """Connector to the IMAP server

    Raises:
        self.imap.error: Base IMAP error
        e: Base IMAP Error

    Returns:
        list: ids of all emails

    Yields:
        email: email.message
    """
    LOGIN_ATTEMPTS_LIMIT = 3

    def __init__(self, username: str, password: str, imap_host: str) -> None:
        self.username = username
        self.password = password
        self.imap_host = imap_host


    def _login(self):
        login_attempts = 0
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL(self.imap_host)
                r, d = self.imap.login(self.username, self.password)

                if r == "OK":
                    logger.info(f"Signed in as; {self.username}, {d}")
                    return

                raise self.imap.error

            except self.imap.error as e:
                login_attempts = login_attempts + 1
                logger.error(
                    f"Error occurred, trying again. login_attempts: {login_attempts}"
                )

                if login_attempts < self.LOGIN_ATTEMPTS_LIMIT:
                    continue

                logger.exception(e)
                raise e

    def _inbox(self):
        self._login()
        return self.imap.select("Inbox", readonly=True)

    def all_inbox(self) -> list:
        self._inbox()
        inbox = self.imap.search(None, "ALL")
        return inbox[1][0].decode('utf-8').split(" ")

    def get_email(self, id: str) -> email.message:
        try:
            r, d = self.imap.fetch(id, "(RFC822)")
        except:
            self._inbox()
            r, d = self.imap.fetch(id, "(RFC822)")

        return email.message_from_bytes(d[0][1])

    def all_emails(self) -> email.message:
        for id in self.all_inbox():
            yield self.get_email(id)
