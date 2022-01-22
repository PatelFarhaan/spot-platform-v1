import sys
from aws_services import AWS
from file_functions import read_json_file, save_json


def add_percentage_increase_to_spot_price(spot_price: float, _add_spot_price_percentage: float) -> float:
    _new_spot_price = spot_price + (spot_price * _add_spot_price_percentage/100)
    return _new_spot_price


def get_availability_zones(region: str):
    aws_obj = AWS()
    ec2_client = aws_obj.get_ec2_client()
    response = ec2_client.describe_availability_zones(
        Filters=[
            {
                "Name": "region-name",
                "Values": [
                    region
                ]
            }
        ]
    )
    if response:
        az = [az_config.get("ZoneName") for az_config in response["AvailabilityZones"]]
        return az


def update_config_file(config_file_path, az, spot_price):
    config_file = read_json_file(config_file_path)
    config_file["spot_config"]["previous_price"] = spot_price
    config_file["spot_config"]["instance_price"] = str(spot_price)
    config_file["spot_config"]["auto_scaling_group"]["availability_zones"] = az
    save_json(config_file_path, config_file)


def get_public_subnets_for_vpc(vpc_id: str) -> list[str]:
    ...


if __name__ == "__main__":
    # config_file_path = "./../enviroments/dev/us-east-1/config.json"
    # config_file = read_json_file(config_file_path)

    aws_region = "us-east-1"

    availability_zones = get_availability_zones(aws_region)
    print(availability_zones)

    # update_config_file(config_file_path, availability_zones, new_spot_price)
