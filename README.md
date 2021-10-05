# py-gmailnator
 
An unofficial python wrapper for [gmailnator.com](https://gmailnator.com/), a temp-email site that uses real `@gmail.com` addresses.

# Documentation

## Gmailnator()
Initializes a Gmailnator session, keep in mind these are not restricted to one address at a time.

### Gmailnator.generate_address(non_gmail=False, plus=True, dot=True)
Returns an email address string from gmailnator's pool.

### Gmailnator.get_inbox(address)
Returns a list of `Message` objects from the address's inbox.

### Gmailnator.wait_for_message(address, sender, timeout=60)

## Message()
Represents an email message from a gmailnator inbox.

### Message.sender

### Message.sender_address

### Message.subject

### Message.content
