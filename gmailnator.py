from html import unescape
from ssl import create_default_context
from requests.adapters import HTTPAdapter
import time
import requests

class CertVerifyFixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_default_context()
        kwargs["ssl_context"] = context
        return super(CertVerifyFixAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_default_context()
        kwargs["ssl_context"] = context
        return super(CertVerifyFixAdapter, self).proxy_manager_for(*args, **kwargs)

class Message:
    def __init__(self, sender, sender_address, subject, url, session=None):
        self.sender = sender
        self.sender_address = sender_address
        self.subject = subject
        self.url = url
        self._session = session
        self._content = None

    def __repr__(self):
        return f"<Message from {self.sender}: {self.subject}>"

    def __hash__(self):
        return hash(self.url.lower())

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    @property
    def content(self):
        if self._content is not None:
            return self._content

        if not self.url.lower().startswith(self._session.base_url.lower()):
            return ""

        address_id = self.url.split("://", 1)[1]\
                             .split("/", 2)[1]
        message_id = self.url.split("#", 1)[1]
        self._content = self._session.get_message_content(address_id, message_id)
        return self._content

class Gmailnator:
    base_url = "https://www.gmailnator.com"
    inbox_refresh_delay = 15
    request_retry_delay = 2
    max_request_retries = 3
    retry_status_codes = (500, 501, 502, 503)
    user_agent = requests.get(
                    "https://jnrbsn.github.io/user-agents/user-agents.json"
                    ).json()[0]

    def __init__(self, proxy_url=None, timeout=30):
        self._http = requests.Session()
        self._http.mount("https://", CertVerifyFixAdapter())
        self._http.headers["User-Agent"] = self.user_agent
        self._http.proxies = {"http": proxy_url, "https": proxy_url}
        self._http.timeout = timeout
        self._csrf_token = None
        self._update_csrf_token()
    
    def _request(self, method, url, _retry=0, **kwargs):
        resp = self._http.request(method, url, **kwargs)
        if not resp.ok:
            if not resp.status_code in self.retry_status_codes \
                or _retry >= self.max_request_retries:
                resp.raise_for_status()
            time.sleep(self.request_retry_delay)
            return self._request(method, url, _retry=_retry+1, **kwargs)
        return resp

    def _update_csrf_token(self):
        resp = self._request("GET", f"{self.base_url}/")
        self._csrf_token = unescape(resp.text\
            .split('<meta name="csrf-token" id="csrf-token" content="', 1)[1]\
            .split('">', 1)[0])
    
    def generate_address(self, non_gmail=False, plus=True, dot=True):
        options = []
        if non_gmail: options.append(1)
        if plus: options.append(2)
        if dot: options.append(3)

        resp = self._request(
            method="POST", 
            url=f"{self.base_url}/index/indexquery",
            data={
                "csrf_gmailnator_token": self._csrf_token,
                "action": "GenerateEmail",
                "data[]": options
            }
        )
        return resp.text.strip()

    def get_inbox(self, address):
        resp = self._request(
            method="POST", 
            url=f"{self.base_url}/mailbox/mailboxquery",
            data={
                "csrf_gmailnator_token": self._csrf_token,
                "action": "LoadMailList",
                "Email_address": address
            }
        )

        messages = []
        for info in resp.json():
            html = info["content"].strip()
            url, html = unescape(html.split('<a href="', 1)[1]\
                                     .split('"', 1))
            sender, html = unescape(html.split("<td>", 1)[1]\
                                        .split("</td>", 1))
            sender, _, sender_address = sender.partition("<")
            if sender_address:
                sender = sender.rstrip()
                sender_address = sender_address.split(">", 1)[0]
            subject, html = unescape(html.split("<td>", 1)[1]\
                                         .split("</td>", 1))
            message = Message(sender, sender_address, subject, url, self)
            messages.append(message)

        return messages

    def get_message_content(self, address_id, message_id):
        resp = self._request(
            method="POST",
            url=f"{self.base_url}/mailbox/get_single_message/",
            data={
                "csrf_gmailnator_token": self._csrf_token,
                "action": "get_message",
                "message_id": message_id,
                "email": address_id
            }
        )
        return resp.json()["content"].strip()
    
    def wait_for_message(self, address, timeout=60, ignore_existing=False, **match_attributes):
        cache = self.get_inbox(address) if ignore_existing else []
        
        for _ in range(int(timeout/self.inbox_refresh_delay)):
            time.sleep(self.inbox_refresh_delay)
            for message in self.get_inbox(address):
                if message in cache:
                    continue
                if not match_attributes \
                    or all((matcher(getattr(message, attr))
                            if callable(matcher)
                            else getattr(message, attr) == matcher)
                            for attr, matcher in match_attributes.items()):
                    return message
        
        raise TimeoutError