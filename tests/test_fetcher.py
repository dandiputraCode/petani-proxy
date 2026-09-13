import unittest
from core.fetcher import PROXY_REGEX, load_sources_config

class TestFetcher(unittest.TestCase):
    def test_regex_matching(self):
        sample = """
        192.168.1.1:8080
        http://10.0.0.1:3128
        socks5://1.2.3.4:1080
        invalid_ip:9999
        256.0.0.1:80
        """
        matches = [m.group(0) for m in PROXY_REGEX.finditer(sample)]
        self.assertIn("192.168.1.1:8080", matches)
        self.assertIn("http://10.0.0.1:3128", matches)
        self.assertIn("socks5://1.2.3.4:1080", matches)
        self.assertNotIn("invalid_ip:9999", matches)
        self.assertNotIn("256.0.0.1:80", matches)

    def test_sources_config(self):
        sources = load_sources_config()
        self.assertIn("http", sources)
        self.assertIn("socks4", sources)
        self.assertIn("socks5", sources)
        self.assertGreater(len(sources["http"]), 0)

if __name__ == "__main__":
    unittest.main()
