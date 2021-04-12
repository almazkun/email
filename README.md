# email
Emails downloader


## Usage example: 
* Print "From" and "To" of all email in Inbox folder:

```python
from main import ReceivedEmails


username = "my_email@address.com"
password = "my_very_string_password"
imap_host = "imap.gmail.com"

m = ReceivedEmails(username, password, imap_host)

for msg in m.all_emails():
    print(msg["From"], msg["To"])
```