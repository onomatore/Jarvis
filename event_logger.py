from events import event_bus

# =========================================
# LOGGER
# =========================================

def log_event(data):

    print(
        "[EVENT]",
        data
    )

event_bus.subscribe(
    "tool_start",
    log_event
)

event_bus.subscribe(
    "tool_finish",
    log_event
)

event_bus.subscribe(
    "memory_added",
    log_event
)