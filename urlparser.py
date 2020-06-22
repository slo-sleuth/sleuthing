from urllib.parse import parse_qs, unquote, unquote_plus
from base64 import b64decode
import sys
import json

class URL:
    """Class to read a URL and parse its components."""

    def __init__(self, url: str):
        """Initialize URL object from url string and populate attributes from 
        the url string components."""

        self.url = url
        self.parsed         = urlparse(url)
        self.fragment       = self.parsed.fragment
        self.hostname       = self.parsed.hostname
        self.netlocation    = self.parsed.netloc
        self.path           = self.parsed.path
        self.parameters     = self.parsed.params
        self.password       = self.parsed.password
        self.port           = self.parsed.port
        self.query          = self.parsed.query
        self.scheme         = self.parsed.scheme
        self.username       = self.parsed.username

    def _decodeB64(self, obj: str):
        """Returns a decoded base64 obj.  Throws an exception on error."""
        return b64decode(obj).decode()

    def split_query(self):
        """Returns the split the query dictionary element, decoding any
        detected base64 strings.  Does not attempt to correct poorly 
        constructed base64 strings."""
        parsed = parse_qs(self.query)
        for key, value in parsed.items():
            try:
                parsed[key] = self._decodeB64(value[0])
            except:
                pass
        return parsed

    def unquote(self, obj: str):
        """Returns the unquoted obj string, tries to autodetect "%" quoting and "+" quoting."""
        try: 
            obj = unquote(obj)
        except:
            obj = unquote_plus(obj)
        return unquote(obj)

    def __repr__(self):
        """Returns the URL string."""
        return f"URL: {vars(self)}"
    
    def __len__(self):
        """Returns the URL length."""
        return len(self.url)


def pprint_url(url: str) -> None:
    """Pretty prints url components to stdout."""

    u = URL(url)

    components = (
        ("Scheme", u.scheme, False),
        ("Network Location", u.netlocation, False),
        ("Username", u.username, True),
        ("Hostname", u.hostname, True),
        ("Port", u.port, True),
        ("Password", u.password, True),
        ("Path", u.path, False),
        ("Parameters", u.parameters, False),
        ("Query", u.query[:50] + '[...]', False)
        )

    # print components
    for component in components:
        label, value, indent = component
        if not value:
            value = ''
        if not indent:
            print(f'{label:25}: {value}')
        else:
            print(f'  {label:23}: {value:}')

    # loop through the query and print, unquoting special characters
    for key, value in u.split_query().items():
        if isinstance(value, list):
            value = ', '.join(i for i in value)
            print(f'  {key:23}: {value}')
        else:
            try:
                j = json.loads(value)
                print(f'  {key:23}: {value[:50]}[...]', )
                for k, v in j.items():
                    v = v.replace('\n', '; ')
                    print(f'{" ":25}: {k}: {v}')
            except:
                pass

    # print fragment
    fragment = unquote(u.fragment)
    if not fragment:
        fragment = "None"
    print(f'{"Fragment":25}: {fragment}')
    return

def main():
    print(sys.argv[1])
    pprint_url(sys.argv[1])

if __name__ == "__main__":
    main()
