from rest_framework import serializers

from core.models import Instruments, Repairers, Repairs


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = [
            "id",
            "external_id",
            "name",
            "entry_date",
            "inventory_number",
            "status",
        ]


class RepairersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repairers
        fields = [
            "id",
            "external_id",
            "name",
            "email",
            "contact_person",
            "phone",
            "address",
            "company_details",
        ]


class RepairsSerializer(serializers.ModelSerializer):
    instrument_name = serializers.CharField(source="instrument.name", read_only=True)
    repairer_name = serializers.CharField(source="repairer.name", read_only=True)

    instrument_external_id = serializers.CharField(
        source="instrument.external_id", read_only=True
    )
    repairer_external_id = serializers.CharField(
        source="repairer.external_id", read_only=True
    )

    class Meta:
        model = Repairs
        fields = [
            "id",
            "external_id",
            "instrument",
            "instrument_name",
            "instrument_external_id",
            "repairer",
            "repairer_name",
            "repairer_external_id",
            "failure_date",
            "date_of_delivery_for_repair",
            "date_of_receipt_from_repair",
            "repair_cost",
            "comment",
        ]
