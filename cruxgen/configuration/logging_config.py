from pyfuncmonitor import FunctionMonitor, MonitorConfig, set_config

custom_config = MonitorConfig(
        log_level=10,  # DEBUG
        log_to_file=True,
        log_file_path="custom_monitor.log",
        enable_memory_monitoring=True,
        enable_cpu_monitoring=True,
        default_return_raw_result=False,
    )

set_config(custom_config)

monitor = FunctionMonitor(
    validate_input=True,
    validate_output=True,
    log_level="DEBUG",  # DEBUG
    log_execution=True,
)