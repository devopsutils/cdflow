import unittest
from string import digits, printable

from mock import patch, MagicMock, Mock
from hypothesis import given, assume
from hypothesis.strategies import dictionaries, fixed_dictionaries, text

import yaml

from strategies import image_id

from cdflow import get_account_id, get_image_id, assume_role, CDFLOW_IMAGE_ID


class TestAssumeRole(unittest.TestCase):

    @patch('cdflow.Session')
    def test_assume_role_in_account(self, Session):
        root_session = Mock(region_name='eu-north-1')
        sts_client = Mock()
        sts_client.assume_role.return_value = {
            'Credentials': {
                'AccessKeyId': 'foo',
                'SecretAccessKey': 'bar',
                'SessionToken': 'baz',
            }
        }
        root_session.client.return_value = sts_client

        account_id = '123456789'
        session_name = 'foo@bar.com'

        session = assume_role(root_session, account_id, session_name)

        assert session == Session.return_value

        sts_client.assume_role.assert_called_once_with(
            RoleArn='arn:aws:iam::{}:role/admin'.format(account_id),
            RoleSessionName=session_name,
        )

        Session.assert_called_once_with(
            'foo', 'bar', 'baz', root_session.region_name
        )


class TestGetAccountId(unittest.TestCase):

    @given(text(alphabet=digits))
    def test_get_account_id(self, account_id):
        with patch('cdflow.open') as open_, \
                patch('cdflow.BytesIO') as BytesIO:

            config_file = MagicMock(spec=file)
            config_file.read.return_value = yaml.dump({
                'account_prefix': 'foo',
            })
            open_.return_value.__enter__.return_value = config_file

            s3_bucket = Mock()

            mock_file = Mock()
            mock_file.read.return_value = account_id

            BytesIO.return_value.__enter__.return_value = mock_file

            assert account_id == get_account_id(s3_bucket)
            mock_file.seek.assert_called_once_with(0)
            s3_bucket.download_fileobj.assert_called_once_with(
                'foodev',
                mock_file,
            )


class TestGetReleaseCommandsImage(unittest.TestCase):

    @given(dictionaries(
        keys=text(alphabet=printable), values=text(alphabet=printable)
    ))
    def test_get_default_image_id(self, environment):
        assume('CDFLOW_IMAGE_ID' not in environment)

        image_id = get_image_id(environment)

        assert image_id == CDFLOW_IMAGE_ID

    @given(fixed_dictionaries({
        'environment': dictionaries(
            keys=text(alphabet=printable), values=text(alphabet=printable)
        ),
        'image_id': image_id(),
    }))
    def test_get_image_id_from_environment(self, fixtures):
        environment = fixtures['environment']
        environment['CDFLOW_IMAGE_ID'] = fixtures['image_id']

        image_id = get_image_id(environment)

        assert image_id == fixtures['image_id']
