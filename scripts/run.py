import sys
import time
from aws_services import AWS
from file_functions import read_json_file, save_json


def get_current_spot_price(instance_type: str) -> list:
    aws_obj = AWS()
    ec2_client = aws_obj.get_ec2_client()
    response = ec2_client.describe_spot_price_history(
        StartTime=time.time(),
        InstanceTypes=[instance_type],
        ProductDescriptions=["Linux/UNIX"]
    )
    if response:
        response = [{"az": obj["AvailabilityZone"], "spot_price": float(obj["SpotPrice"])} for obj in
                    response.get("SpotPriceHistory")]
    return response


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


def get_lowest_spot_price(spot_prices: list) -> float:
    max_spot_price = max(spot_prices, key=lambda x: [x.get("spot_price")])
    return max_spot_price.get("spot_price")


def compare_with_previous_spot_price(previous_spot_price, lowest_spot_price) -> bool:
    if not previous_spot_price:
        return False
    elif previous_spot_price == lowest_spot_price:
        return True
    return False


def update_config_file(config_file_path, az, spot_price):
    config_file = read_json_file(config_file_path)
    config_file["spot_config"]["previous_price"] = spot_price
    config_file["spot_config"]["instance_price"] = str(spot_price)
    config_file["spot_config"]["auto_scaling_group"]["availability_zones"] = az
    save_json(config_file_path, config_file)


def get_public_subnets_for_vpc(vpc_id: str) -> list[str]:
    ...


if __name__ == "__main__":
    config_file_path = "./../enviroments/dev/us-east-1/config.json"
    config_file = read_json_file(config_file_path)

    aws_region = config_file.get("aws_region")
    spot_instance_type = config_file.get("spot_config", {}).get("instance_type")
    previous_spot_price = config_file.get("spot_config", {}).get("previous_price")
    add_spot_price_percentage = config_file.get("spot_config", {}).get("add_percentage")

    latest_spot_prices_per_az = get_current_spot_price(spot_instance_type)
    lowest_spot_price = get_lowest_spot_price(latest_spot_prices_per_az)

    if compare_with_previous_spot_price(previous_spot_price, lowest_spot_price):
        print("Current SPOT price is equal to Previous SPOT price. No Action needs to be performed!")
        sys.exit(0)

    new_spot_price = add_percentage_increase_to_spot_price(lowest_spot_price, add_spot_price_percentage)
    availability_zones = get_availability_zones(aws_region)

    update_config_file(config_file_path, availability_zones, new_spot_price)
