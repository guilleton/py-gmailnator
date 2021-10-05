# py-gmailnator
 
An unofficial python wrapper for [gmailnator.com](https://gmailnator.com/), a temp-email site that uses real `@gmail.com` addresses.

# Documentation

## Gmailnator(self, proxy_url=None, timeout=None)
Initializes a Gmailnator session, keep in mind these are not restricted to one address at a time.

### .generate_address(non_gmail=False, plus=True, dot=True)
Returns an email address string from gmailnator's pool.

### .get_inbox(address)
Returns a list of `Message` objects from the address's inbox.

### .wait_for_message(self, address, timeout=60, **match_attributes)

## Message()
Represents an email message from a gmailnator inbox.

### .sender

### .sender_address

### .subject

### .content
