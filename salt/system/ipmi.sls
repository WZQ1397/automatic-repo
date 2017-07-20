ipmi:
    kmod.present:
        - names:
            - ipmi_devintf
            - ipmi_si
            - ipmi_watchdog
            - ipmi_poweroff
            - acpi_ipmi