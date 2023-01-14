import json
from io import BytesIO
from types import ModuleType

import avro.io
import avro.schema

from avro_neo_gen.core.driver.apache_avro_binary_driver import ApacheAvroBinaryDriver
from avro_neo_gen.core.driver.driver_proxy import DriverProxy
from avro_neo_gen.core.neo_gen_record import NeoGenRecord


class TestCoreDriverApacheAvroBinaryDriver:
    def test_apache_avro_binary_driver(
        self,
        neo_gen_record_module: ModuleType,
        apache_avro_binary_core_driver_proxy: DriverProxy,
    ) -> None:
        User = neo_gen_record_module.User

        user_schema = avro.schema.parse(json.dumps(User.__canonical_schema__))
        datum = {"name": "alice", "favorite_number": 10, "favorite_color": "red"}

        expected_bytes = BytesIO()
        avro.io.DatumWriter(writers_schema=user_schema).write(
            encoder=avro.io.BinaryEncoder(writer=expected_bytes),
            datum=datum,
        )

        driver = ApacheAvroBinaryDriver()
        generated_bytes = BytesIO()
        driver.write(User(**datum), generated_bytes)
        generated_bytes.seek(0)

        generated_user = User.read(generated_bytes)

        assert isinstance(generated_user, NeoGenRecord)
        assert isinstance(generated_user, User)
        assert expected_bytes.getvalue() == generated_bytes.getvalue()
        assert generated_user._datum == datum
        assert generated_user.encode() == datum

        generated_bytes.seek(0)
        generated_user.write(generated_bytes)
        assert expected_bytes.getvalue() == generated_bytes.getvalue()
