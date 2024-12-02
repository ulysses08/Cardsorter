# Cardsorter
Automated sorting of MTG cards using raspberry pi and camera

Idea is based on OCR of only the bottom corner of the card to recognize the ID number, Set, Type, Rarity and Language rather than trying to recognize the whole card in one go.

Modern card id layout started in VMA (Vintage Masters June 16 2014).

System will not initially work for any cards from prior to that.

I have ideas but nothing concrete to fix that.


I don't think foil recognition will work initially either. Starting points though.



Roadmap:

a0.1:
Software:
-OCR working and outputting the base variables for base card format.
  Card Type - Single Character - type_line - contains converted full word
  Card Number - String - collector_number - Need to trim leading zeros
  Set - String - set
  Language - String - lang
  
a0.2:
Software:
-Use Json from scryfall to pull additional variables and print to terminal
  Scryfall ID - String - id
  Card Name - String - name
  Release Date - String - released_at
  Converted Mana cost - String - cmc
  Set Name - Bloomburrow
  Object type - String - object
  Small Scan URL - String
  Normal Scan URL - String

a0.3:
Software:
-Connect to SQL database locally to store currently held cards. Store all generated variables locally. Store duplicates as incrementing qty variable.
  Card Type - Single Character - type_line - contains converted full word
  Card Number - String - collector_number - Need to trim leading zeros
  Set - String - set
  Language - String - lang
  Scryfall ID - String - id
  Card Name - String - name
  Release Date - String - released_at
  Converted Mana cost - String - cmc
  Set Name - Bloomburrow
  Object type - String - object
  Small Scan URL - String
  Normal Scan URL - String
  Quantity - Int
  Is foil - Bool
  Special Type - String (no or name the type)

a0.4:
Software:
-Web interface to:
  control the scanner
  View cards in database
  
Hardware:
Zero impact moving cards around. Need to research the safest way so cards wont be damaged.

Prior to 0.8 manual moving of cards will be needed.

a0.5:

-SQL updates
  Add options to place cards in seperate collections.
  Add sql variable for location (ie, In Box #, In bulk box, In this deck, enter your own) This variable needs to be an array so multiple copies can be stored in seperate places/in decks for better tracking.

Ready for testing by others. Currently relying on moving cards by hand.

Expecting a long time at this step.

Hardware:

Work on the automatic card movement, multiple bins and sorting rules set manually.

a0.6:

Need to be able to recognize Foil copies properly.

Hardware:
First hardware proto ready for testing.

a0.7:

Add option to web interface to connect to external SQL

a0.8:

Ideas for recognizing pre VMA Cards / Specialty cards

1.0:
Software ready
Hardware ready
