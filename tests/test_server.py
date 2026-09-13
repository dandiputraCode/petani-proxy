import unittest
from core.server import ProxyPoolManager

class TestServerPool(unittest.TestCase):
    def setUp(self):
        self.mock_proxies = [
            {"proxy": "1.1.1.1:8080", "protocol": "http", "latency_ms": 120},
            {"proxy": "2.2.2.2:1080", "protocol": "socks5", "latency_ms": 250},
        ]
        self.pool = ProxyPoolManager(self.mock_proxies)

    def test_round_robin_rotation(self):
        p1 = self.pool.get_next()
        p2 = self.pool.get_next()
        p3 = self.pool.get_next()
        
        self.assertEqual(p1["proxy"], "1.1.1.1:8080")
        self.assertEqual(p2["proxy"], "2.2.2.2:1080")
        self.assertEqual(p3["proxy"], "1.1.1.1:8080")  # Wrapped around

    def test_pool_stats(self):
        self.pool.mark_result(True)
        self.pool.mark_result(False)
        self.assertEqual(self.pool.successful_requests, 1)
        self.assertEqual(self.pool.failed_requests, 1)

if __name__ == "__main__":
    unittest.main()
