#include <openamr_nav_msgs/msg/navigation_status.hpp>
#include <openamr_nav_msgs/msg/docking_status.hpp>
#include <openamr_nav_msgs/msg/parking_status.hpp>
#include <rclcpp/serialization.hpp>
#include <rclcpp/serialized_message.hpp>
#include <stdexcept>

template<class Message> void round_trip(const Message & input) {
  rclcpp::Serialization<Message> serializer;
  rclcpp::SerializedMessage bytes;
  serializer.serialize_message(&input, &bytes);
  Message output;
  serializer.deserialize_message(&bytes, &output);
  if (input != output) throw std::runtime_error("Serialization mismatch");
}

int main() {
  using openamr_nav_msgs::msg::NavigationStatus;
  static_assert(NavigationStatus::CONTRACT_VERSION == EXPECTED_CONTRACT, "Contract changed");
  NavigationStatus status;
  status.contract_version = NavigationStatus::CONTRACT_VERSION;
  status.profile_id = "clean-install-consumer";
  status.sensors.emplace_back();
  status.constraints.emplace_back();
#if EXPECTED_CONTRACT == 2
  status.site_config.state = status.site_config.STATE_MATCHED;
  status.site_config.floor_coverage = status.site_config.COVERAGE_FULL;
  status.site_config.reason = NavigationStatus::NONE;
  status.site_config.map_id = "install-test-map";
  status.site_config.map_version = "test-map-content-hash";
  status.site_config.config_id = "install-test-config";
  status.site_config.config_version = "test-config-content-hash";
#endif
  round_trip(status);
  round_trip(openamr_nav_msgs::msg::DockingStatus{});
  round_trip(openamr_nav_msgs::msg::ParkingStatus{});
}
