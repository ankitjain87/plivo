from app import app

from base64 import b64encode

import json
import unittest


data = {
    "from": "91983435345",
    "to": "4924195509198",
    "text": "Hi How r u"
}

data1 = {
    "to": "91983435345",
    "from": "4924195509198",
    "text": "Hi How r u"
}

data2 = {
    "to": "9198343534512345",
    "from": "4924195509198",
    "text": "Hi How r u"
}

class TestViews(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_inbound_pass(self):
        test_client = app.test_client(self)
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "",
            "message": "inbound sms ok"
        })

    def test_inbound_fail(self):
        test_client = app.test_client(self)
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "unknown failure",
            "message": ""
        })

    def test_inbound_1(self):
        test_client = app.test_client(self)
        data = {
            "from": "91983435345",
            "to": "4924195509198",
            "text": ""
        }
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "text is missing",
            "message": ""
        })

    def test_inbound_2(self):
        test_client = app.test_client(self)
        data = {
            "from": "919834353451234321",
            "to": "4924195509198",
            "text": "Hi"
        }
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "from is invalid",
            "message": ""
        })

    def test_inbound_3(self):
        test_client = app.test_client(self)
        data = {
            "from": "91983435345",
            "to": "49241509198",
            "text": "Hi"
        }
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "to parameter not found",
            "message": ""
        })

    def test_inbound_3(self):
        test_client = app.test_client(self)
        data = {
            "from": "91983435345",
            "to": "49241509198",
            "text": "Hi"
        }
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "to parameter not found",
            "message": ""
        })

    def test_inbound_4(self):
        test_client = app.test_client(self)
        data = {
            "from": "91983435345",
            "to": "4924195509198",
            "text": "STOP"
        }
        response = test_client.post(
            '/inbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "",
            "message": "inbound sms ok"
        })

    def test_outbound_pass(self):
        test_client = app.test_client(self)
        response = test_client.post(
            '/outbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data2)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "",
            "message": "outbound sms ok"
        })

    def test_outbound_fail(self):
        test_client = app.test_client(self)
        response = test_client.post(
            '/outbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "from parameter not found",
            "message": ""
        })

    def test_outbound_1(self):
        test_client = app.test_client(self)
        response = test_client.post(
            '/outbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data1)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "sms from 4924195509198 to 91983435345 blocked by STOP request",
            "message": ""
        })

    def test_outbound_2(self):
        test_client = app.test_client(self)
        data1 = {
            "from": "4924195509198123432",
            "to": "123454321234",
            "text": "Hi How r u"
        }
        response = test_client.post(
            '/outbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data1)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "from is invalid",
            "message": ""
        })

    def test_outbound_3(self):
        test_client = app.test_client(self)
        data1 = {
            "to": "91983435345",
            "from": "4924195509198",
            "text": "Hi How r u"
        }
        response = test_client.post(
            '/outbound/sms/',
            content_type='application/json',
            headers={"Authorization": "Basic {user}".format(
                user=b64encode(b"plivo1:20S0KPNOIM"))},
            data=json.dumps(data1)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "to is missing",
            "message": ""
        })

    def test_outbound_4(self):
        test_client = app.test_client(self)
        data1 = {
            "to": "919834351234567",
            "from": "4924195509198",
            "text": "Hi How r u"
        }
        for i in range(50):
            response = test_client.post(
                '/outbound/sms/',
                content_type='application/json',
                headers={"Authorization": "Basic {user}".format(
                    user=b64encode(b"plivo1:20S0KPNOIM"))},
                data=json.dumps(data1)
            )
        print response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "error": "limit reached for from 4924195509198",
            "message": ""
        })


if __name__ == '__main__':
    unittest.main()

