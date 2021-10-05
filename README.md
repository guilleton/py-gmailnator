# py-gmailnator
 
An unofficial python wrapper for [gmailnator.com](https://gmailnator.com/), a temp-email site that uses real `@gmail.com` addresses.

# Usage
```python
from gmailnator import Gmailnator

gtor = Gmailnator()
address = gtor.generate_address()
# send email to <address> ..
try:
    message = gtor.wait_for_message(address, timeout=120, sender_address="something@somewhere.org")
    print(message.subject, "\n", message.content)
except TimeoutError:
    print("Didn't receive email in time :(")
```

# Documentation

## Gmailnator(self, proxy_url=None, timeout=30)
Initializes a Gmailnator session, keep in mind these are not restricted to one address at a time.

### .generate_address(non_gmail=False, plus=True, dot=True)
Returns an email address string from gmailnator's pool.

### .get_inbox(address)
Returns a list of `Message` objects from the address's inbox.

### .wait_for_message(self, address, timeout=60, ignore_existing=False, **match_attributes)
Values for `match_attributes` can literals or callables (first parameter being the value of the attr.). `ignore_existing` will ignore emails that are present at the time of calling the method.

## Message()
Represents an email message from a gmailnator inbox.

### .sender

### .sender_address

### .subject

### .content
